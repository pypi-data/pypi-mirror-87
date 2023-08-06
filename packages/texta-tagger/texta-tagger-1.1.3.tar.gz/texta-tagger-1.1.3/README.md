# TEXTA Tagger Python Package

This package is for using text classification models exported from TEXTA Toolkit 2.

## Installation

### Using built package

`pip install texta-tagger`

### Using Git (for development)

`pip install git+https://git.texta.ee/texta/texta-tagger.git`

## Usage

### Predicting Using Zipped Model

**Predicting without MLP & lemmatization**
```
>>> from texta_tagger.tagger import Tagger
>>>
>>> t = Tagger()
>>> t.load_zip('test_data/tagger.zip')
True
>>> print('Tagger:', t)
Tagger: Eesti
>>> t.tag_text('eesti keel ja eesti meel')
{'prediction': True, 'probability': 0.9999999322365133}
```

**Predicting with MLP & lemmatization**

Predicting with lemmatization requires either a running MLP server or MLP Python package installed. In following example MLP from package is used:
```
>>> from texta_tagger.tagger import Tagger
>>> from texta_mlp.mlp import MLP
>>>
>>> mlp = MLP()
>>>
>>> t = Tagger(mlp=mlp)
>>> t.load_zip('test_data/tagger.zip')
True
>>> print('Tagger:', t)
Tagger: Eesti
>>> t.tag_text('eesti keel ja eesti meel')
{'prediction': True, 'probability': 0.9999999322365133}
```

In following example MLP server version is used:
```
>>> from texta_tagger.tagger import Tagger
>>> from texta_tagger.mlp_analyzer import get_mlp_analyzer
>>>
>>> mlp = get_mlp_analyzer(mlp_host="http://my-mlp-server:5000")
>>>
>>> t = Tagger(mlp=mlp)
>>> t.load_zip('test_data/tagger.zip')
True
>>> print('Tagger:', t)
Tagger: Eesti
>>> t.tag_text('eesti keel ja eesti meel')
{'prediction': True, 'probability': 0.9999999322365133}
```

### Training
TODO

### Environment Variables

* TEXTA_TAGGER_MLP_URL - MLP host used for lemmatization (e.g. http://mlp-dev.texta.ee:5000)
* TEXTA_TAGGER_MLP_MAJOR_VERSION - MLP major version (2/3).