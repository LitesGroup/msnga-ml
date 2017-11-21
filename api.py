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
        op['subjects'] = [t.text for t in self.spc(input.decode('utf-8', 'ignore')) if (t.dep_ in ["nsubj", "nsubjpass", "dobj", "iobj", "pobj"])]
        resp.media = op

        # Future Batch processing function
        # print [x for x in textacy.keyterms.singlerank(textacy.Doc(unicode(input), lang=u'en'))]


class Enrich(object):
    spc = English()

    def on_post(self, req, resp):
        try:
            raw_json = req.stream.read()
            ip = textacy.Doc(unicode(json.loads(raw_json, encoding='utf-8')['sentence']), lang=u'en')
            print ip
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Error',
                                   ex.message)
        out = {}
        if len(textacy.keyterms.textrank(ip)) > 0:
            out["textrank"] = [x[0] for x in textacy.keyterms.textrank(ip)]
        if len(textacy.keyterms.singlerank(ip)) > 0:
            out["singlerank"] = [x for x in textacy.keyterms.singlerank(ip)]
        if textacy.extract.subject_verb_object_triples(ip):
            out["svo"] = [str(x[0]) for x in textacy.extract.subject_verb_object_triples(ip)]
        if textacy.extract.ngrams(ip, 2):
            out["bigrams"] = [str(x) for x in textacy.extract.ngrams(ip, 2)]

        resp.status = falcon.HTTP_200
        resp.media = out

api = falcon.API()
api.add_route('/parse', NLP())
api.add_route('/enrich', Enrich())
