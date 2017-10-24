import falcon
import json
import textacy
from spacy.en import English
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class NLP(object):
    sid = SentimentIntensityAnalyzer()
    spc = English()

    def on_post(self, req, resp):
        try:
            raw_json = req.stream.read()
            input = json.loads(raw_json, encoding='utf-8')['sentence']
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Error',
                                   ex.message)
        resp.status = falcon.HTTP_200
        op = self.sid.polarity_scores(input)
        op['subjects'] = [t.text for t in self.spc(unicode(input)) if (t.dep_ in ["nsubj", "nsubjpass", "dobj", "iobj", "pobj"])]
        resp.media = op

        # Future Batch processing function
        # print [x for x in textacy.keyterms.singlerank(textacy.Doc(unicode(input), lang=u'en'))]

api = falcon.API()
api.add_route('/parse', NLP())
