# TEXTA Torch Tagger Python Package

## Installation

### From Git
`pip install git+https://git.texta.ee/texta/texta-torch-tagger-python.git`

## Testing
`python -m pytest -v tests`

# Usage
```
>>>  from texta_tools.embedding import W2VEmbedding
>>>  from texta_torch_tagger.tagger import TorchTagger
>>>  
>>>  data = {"good": ["Täna on ilus ilm.", "Kuidas käsi käib?"], "bad": ["Arno on loll.", "ei"]}
>>>  
>>>  embedding = W2VEmbedding()
>>>  embedding.train([y for x in data.values() for y in x])
>>>  
>>>  tagger = TorchTagger(embedding, model_arch="TextRNN")
>>>  
>>>  report = t.train(data, num_epochs=3)
>>>  
>>>  tagger.tag_text("Ei hooli.")
"bad"
```
