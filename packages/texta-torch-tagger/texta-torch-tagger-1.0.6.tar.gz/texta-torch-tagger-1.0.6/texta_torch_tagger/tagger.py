import json
import dill
import numpy as np
import pandas as pd
import torch
import torch.optim as optim
from torch import nn, FloatTensor
from torchtext import data

from texta_tools.text_processor import TextProcessor

from .models.models import TORCH_MODELS
from .tagging_report import TaggingReport
from . import exceptions


class TorchTagger:

    def __init__(self, embedding, model_arch="fastText", tokenizer=None):
        # retrieve model and initial config
        self.description = None
        self.config = TORCH_MODELS[model_arch]["config"]()
        self.model_arch = TORCH_MODELS[model_arch]["model"]
        # output size & max epochs
        self.config.output_size = None
        self.config.max_epochs = None
        # statistics report for each epoch
        self.epoch_reports = []
        # model
        self.model = None
        self.text_field = None
        # indices to save label to int relations
        self.label_index = None
        self.label_reverse_index = None
        # load tokenizer and embedding for the model
        self.tokenizer = self._get_tokenizer()
        self.embedding = embedding
        # text processor
        self.text_processor = TextProcessor(phraser=embedding.phraser, remove_stop_words=False, tokenizer=tokenizer)


    @staticmethod
    def _get_tokenizer():
        """
        Retrieves simple tokenizer. As we are using MLP to tokenize texts, let's split only on whitespace.
        :return: Tokenizer as a lambda function.
        """
        return lambda sent: [x.strip() for x in sent.split(" ")]


    @staticmethod
    def _tensorize_embedding(embedding):
        """
        Returns vectors as FloatTensor and word2index dict for torchtext Vocab object.
        https://torchtext.readthedocs.io/en/latest/vocab.html
        """
        word2index = {token: token_index for token_index, token in enumerate(embedding.model.wv.index2word)}
        return FloatTensor(embedding.model.wv.vectors), word2index


    @staticmethod
    def evaluate_model(model, iterator):
        """
        Evaluates the model using evaluation set & Tagging Report.
        :param: iterator: Instance of TorchText BucketIterator.
        :return: Instance of Tagging Report containing the results.
        """
        all_preds = []
        all_y = []
        all_logprobs = []

        for idx, batch in enumerate(iterator):
            if torch.cuda.is_available():
                x = batch.text.cuda()
            else:
                x = batch.text
            y_pred = model(x)
            probabilities, predictions = torch.max(y_pred.cpu().data, 1)
            all_preds.extend(predictions.numpy())
            all_y.extend(batch.label.numpy())
            all_logprobs.extend(probabilities.numpy())
        
        # flatten predictions
        all_preds = np.array(all_preds).flatten()
        all_logprobs = np.array(all_logprobs).flatten()

        #add small epsilon to probabilities to prevent log(0) in loss calulation
        all_probs = np.exp(all_logprobs)
        all_probs = np.clip(all_probs, 1e-5, 1-1e-5)

        all_y = np.array(all_y)
        classes = list(set(all_y))
        # report
        report = TaggingReport(all_y, all_preds, all_probs, classes)
        report.val_loss = -np.sum(all_y*np.log(all_probs) + (1-all_y)*np.log(1-all_probs))/len(all_y)
        return report

    def train(self, data_sample, num_epochs=5):
        """
        Trains model based on data sample.
        :param: dict data_sample: Dictonary containing class labels as keys and lists of examples as values.
        :return: TaggingReport object.
        """
        # set max epochs
        self.config.max_epochs = num_epochs
        # clear old epoch reports
        self.epoch_reports = []
        # prepare data
        train_iterator, val_iterator, test_iterator, text_field = self._prepare_data(data_sample)
        # declare model
        model = self.model_arch(self.config, len(text_field.vocab), text_field.vocab.vectors, self.evaluate_model)
        # check cuda
        if torch.cuda.is_available():
            print("GPU available. Using GPU.")
            model.cuda()
            # clear cuda cache prior to training
            torch.cuda.empty_cache()
        else:
            print("No GPU available. Are you sure you want to train the tagger using CPU?")
        # train
        model.train()
        optimizer = optim.SGD(model.parameters(), lr=self.config.lr)
        NLLLoss = nn.NLLLoss()
        model.add_optimizer(optimizer)
        model.add_loss_op(NLLLoss)
        # run epochs
        for i in range(self.config.max_epochs):
            report = model.run_epoch(train_iterator, val_iterator, i)
            # update class names
            report.classes = [self.label_reverse_index[cl] for cl in report.classes]
            self.epoch_reports.append(report)
        # set model
        self.model = model
        # set vocab
        self.text_field = text_field
        # return report for last epoch
        return report


    def save(self, path):
        """Saves model on disk."""
        to_save = {
            "torch_tagger": self.model,
            "text_field": self.text_field,
            "label_reverse_index": self.label_reverse_index
        }
        with open(path, 'wb') as file:
            dill.dump(to_save, file)
        return True
    

    def load(self, path):
        """Loads model from disk."""
        with open(path, 'rb') as file:
            loaded = dill.load(file)
        # set class variables
        self._set_loaded_values(loaded)
        self.text_processor.phraser = self.embedding.phraser
        return True


    def load_django(self, tagger_object):
        """Loads model from Django object."""
        # set tagger description & model
        self.description = tagger_object.description
        tagger_path = tagger_object.model.path
        # load model
        return self.load(tagger_path)
    

    def _set_loaded_values(self, loaded):
        """
        Sets values for following class variables:
            * model,
            * text_field,
            * label_reverse_index.
        """
        # eval model
        loaded["torch_tagger"].eval()
        # set values
        self.model = loaded["torch_tagger"]
        self.text_field = loaded["text_field"]
        self.label_reverse_index = loaded["label_reverse_index"]


    def _get_examples_and_labels(self, data_sample):
        # lists for examples and labels
        examples = []
        labels = []
        # retrieve examples for each class
        for label, class_examples in data_sample.items():
            for example in class_examples:
                example = self.text_processor.process(example)
                examples.append(example)
                labels.append(self.label_index[label])
        return examples, labels


    def _get_datafields(self):
        # Creating blank Fields for data
        text_field = data.Field(sequential=True, tokenize=self.tokenizer, lower=True)
        label_field = data.Field(sequential=False, use_vocab=False)
        # create Fields based on field names in document
        datafields = [("text", text_field), ("label", label_field)]
        return datafields, text_field


    def _prepare_data(self, data_sample):
        """
        Prepares training and validation iterators.
        :param: dict data_sample: Dictonary containing class labels as keys and lists of examples as values.
        """
        if not self.embedding:
            raise exceptions.NoEmbeddingError("Training requires embedding. Include one while initializing the object.")
        # retrieve vectors and vocab dict from embedding
        embedding_matrix, word2index = self._tensorize_embedding(self.embedding)
        # set embedding size according to the dimensionality embedding model
        embedding_size = len(embedding_matrix[0])
        self.config.embed_size = embedding_size
        # create label dicts for later lookup
        self.label_index = {a: i for i, a in enumerate(data_sample.keys())}
        self.label_reverse_index = {b: a for a, b in self.label_index.items()}
        # update output size to match number of classes
        self.config.output_size = len(list(data_sample.keys()))
        # retrieve examples and labels from data sample
        examples, labels = self._get_examples_and_labels(data_sample)
        # create datafields
        datafields, text_field = self._get_datafields()
        # create pandas dataframe and torchtext dataset
        train_dataframe = pd.DataFrame({"text": examples, "label": labels})
        train_examples = [data.Example.fromlist(i, datafields) for i in train_dataframe.values.tolist()]
        train_data = data.Dataset(train_examples, datafields)
        # split data for training and testing
        train_data, test_data = train_data.split(split_ratio=self.config.split_ratio)
        # split training data again for validation during training
        train_data, val_data = train_data.split(split_ratio=self.config.split_ratio)
        # build vocab (without vectors)
        text_field.build_vocab(train_data)
        # add word vectors to vocab
        text_field.vocab.set_vectors(word2index, embedding_matrix, embedding_size)
        # training data iterator
        train_iterator = data.BucketIterator(
            (train_data),
            batch_size=self.config.batch_size,
            sort_key=lambda x: len(x.text),
            repeat=False,
            shuffle=True
        )
        # validation and test data iterator
        val_iterator, test_iterator = data.BucketIterator.splits(
            (val_data, test_data),
            batch_size=self.config.batch_size,
            sort_key=lambda x: len(x.text),
            repeat=False,
            shuffle=False)
        return train_iterator, val_iterator, test_iterator, text_field


    def tag_text(self, text, get_label=True):
        """
        Predicts on raw text.
        :param: str text: Input text to be classified.
        :return: class number, class probability
        """
        # process text with our text processor
        text = self.text_processor.process(text)
        # process text with torchtext processor
        processed_text = self.text_field.process([self.text_field.preprocess(text)])
        # check cuda
        if torch.cuda.is_available():
            processed_text = processed_text.to('cuda')
        # predict
        prediction = self.model(processed_text)
        prediction_item = prediction.argmax().item()
        prediction_prob = np.exp(prediction[0][prediction_item].item())
        # get class label if asked
        if get_label:
            prediction_item = self.label_reverse_index[prediction_item]
        # TODO: should use some other metric for prob
        # because prob depends currently on number of classes
        return self._process_prediction_output(prediction_item, prediction_prob)


    def tag_doc(self, doc):
        """
        Predicts on document.
        :param: dict doc: Input document to be classified.
        :return: dict containing class number, class probability
        """
        # TODO: redo this function to use multiple fields correctly
        combined_text = []
        for v in doc.values():
            combined_text.append(v)
        combined_text = " ".join(combined_text)
        prediction_item, prediction_prob = self.tag_text(combined_text)
        return self._process_prediction_output(prediction_item, prediction_prob)


    @staticmethod
    def _process_prediction_output(predicted_label, probability):
        return {
            "prediction": predicted_label,
            "probability": probability
        }
