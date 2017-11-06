# MSNGA-ML    
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

REQUEST
POST http://localhost:8000/enrich
{
	"sentence": "Koenigsegg Agera RS hits 284 mph on way to new land speed record"
}

RESPONSE
{
    "svo": [
        "Koenigsegg",
        "Agera RS"
    ],
    "bigrams": [
        "Koenigsegg Agera",
        "Agera RS",
        "RS hits",
        "hits 284",
        "284 mph",
        "new land",
        "land speed",
        "speed record"
    ],
    "singlerank": [
        [
            "rs",
            0.11111111111111113
        ],
        [
            "land",
            0.11111111111111113
        ]
    ],
    "textrank": [
        "speed",
        "agera",
        "land",
        "rs",
        "mph",
        "new",
        "way",
        "koenigsegg",
        "record"
    ]
}
```
