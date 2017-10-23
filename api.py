import falcon
import json
from nltk import tokenize
from spacy.en import English
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class NLP(object):
    def on_post(self, req, resp):
        sid = SentimentIntensityAnalyzer()
        spc = English()
        try:
            raw_json = req.stream.read()
            input = json.loads(raw_json, encoding='utf-8')
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Error',
                                   ex.message)
        resp.status = falcon.HTTP_200
        op = sid.polarity_scores(tokenize.sent_tokenize(input['sentence'])[0])
        op['subjects'] = [t.text for t in spc(unicode(input['sentence'])) if (t.dep_ == "nsubj")]
        resp.media = op
api = falcon.API()
api.add_route('/parse', NLP())
