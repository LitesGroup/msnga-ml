#MSNGA-ML
<i> An attempt to make social networking great again </i>

requires Spacy, NLTK, gunicorn and falcon

```javascript
gunicorn api:api
REQUEST
POST http://localhost:8000/parse
{
	"sentence": "The quick brown fox jumped over the lazy dog."
}

RESPONSE
{
    "neg": 0.238,
    "subjects": [
        "fox"
    ],
    "neu": 0.762,
    "pos": 0,
    "compound": -0.3612
}
```