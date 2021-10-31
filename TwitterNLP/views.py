from codecs import decode
from django.http import JsonResponse
import requests
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
import logging
import pickle
import json
# import nltk
import re, string, random
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from django.views.decorators.csrf import csrf_exempt


# Create instatnce of logger
log = logging.getLogger('django')


def test(req):
    return HttpResponse('Hello World!')

class Analize(TemplateView):

    @csrf_exempt
    def TwitterSearch(req):

        #get the query from the request
        query = decode(req.body, 'utf-8')
        # log.error(query)

        url = "https://api.twitter.com/1.1/tweets/search/30day/dev.json?query={}".format(query)

        payload={}
        headers = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAACsx%2BQAAAAAA2%2F9Onm5ZIzMJotHeoJQpCFtJV10%3DSK9tQfBsNZirwauxiFzDXl80sB7M0xMGLaAbtGZkhReYFBA1Rz',
        "Cookie" : "guest_id=v1%3A163404759089649456; personalization_id=\"v1_mWi0bYRg8/9gZ1RFNq6UhQ==\""
        }

        fetchTwitter = requests.request("GET", url, headers=headers)
        
        #response = JsonResponse(fetchTwitter) #json.loads(req.body)
        log.error(fetchTwitter)
        return HttpResponse(fetchTwitter)

    def first(req):
        # log.warning("Wrong URL")
        # data = 'oc2093'
        return render(req, 'first.html', {'name': 'Ahmed'})
        # return HttpResponse('Hello World!')

    def remove_noise(tweet_tokens, stop_words = ()):
        cleaned_tokens = []
        for token, tag in pos_tag(tweet_tokens):
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
            '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
            token = re.sub("(@[A-Za-z0-9_]+)","", token)

            if tag.startswith("NN"):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'

            lemmatizer = WordNetLemmatizer()
            token = lemmatizer.lemmatize(token, pos)

            if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())
        return cleaned_tokens

    @staticmethod
    def analyze(req):
        if req.method == 'GET':   
            body = json.loads(req.body)
            data = body['data']

            # load the model from disk
            filename = 'TwitterNLP/MLmodel/NPL_initModel.sav'
            NLPmodel = pickle.load(open(filename, 'rb'))
            #classiy the tweet
            custom_tokens = Analize.remove_noise(word_tokenize(data))
            result = NLPmodel.classify(dict([token, True] for token in custom_tokens))
            
            log.error(result)

            return HttpResponse(result)
        HttpResponse(404)

