from codecs import decode
from django.http import JsonResponse, HttpResponse, response
import requests, logging, json, urllib
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import BadRequest
from .models import peaccmiddle
# import logging
from .MiddleWare import analize





# Create instatnce of logger
log = logging.getLogger("django")
# logging.basicConfig(level=logging.DEBUG)


def test(req):
    return HttpResponse('Hello World!')

class Analize(TemplateView):

    @csrf_exempt
    def TwitterSearch(req):
        if req.method == "POST":
            #get the query from the request
            query = decode(req.body, 'utf-8')
            #web encode the search term i.e replace spaces with %20
            query_P = urllib.parse.quote(query)
            print(f"Search Query: {query}")
            #first env 'dev' for 30day search
            recent = "https://api.twitter.com/1.1/tweets/search/30day/dev.json?query={} lang:en".format(query_P)
            #second env 'twitterReviews' for full archive search
            fullarchive = "https://api.twitter.com/1.1/tweets/search/fullarchive/twitterReviews.json?query={} lang:en".format(query_P)
            #search for popular tweet
            popular = 'https://api.twitter.com/1.1/search/tweets.json?q={}&lang=en&result_type=popular&tweet_mode=extended'.format(query_P)
            #Twitter api v2 recent search 
            apiV2 = 'https://api.twitter.com/2/tweets/search/recent?query={} lang:en&tweet.fields=id,text,lang,public_metrics&max_results=10&user.fields=id,description,created_at,username,profile_image_url,verified'.format(query_P)
            
            # first env 'dev' Bearer Token
            headers = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAACsx%2BQAAAAAA2%2F9Onm5ZIzMJotHeoJQpCFtJV10%3DSK9tQfBsNZirwauxiFzDXl80sB7M0xMGLaAbtGZkhReYFBA1Rz',
            "Cookie" : "guest_id=v1%3A163404759089649456; personalization_id=\"v1_mWi0bYRg8/9gZ1RFNq6UhQ==\""
            }
            # second env 'twitterReviews' Bearer Token
            headers1 = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAJKAVgEAAAAAlJpPjhiR6zoOkW9kX4Z3mybV568%3DZUS51isbSfpuSiLJGFDXY0woi6sXyRDiCQCeIOhoxfwzcFhGNS',
            "Cookie" : "guest_id=v1%3A163404759089649456; personalization_id=\"v1_mWi0bYRg8/9gZ1RFNq6UhQ==\""
            }

            #make recent and full archive search
            # fetchTwitter = []
            popularSearch = requests.request("GET", popular, headers=headers1)
            # fetchTwitter.append(requests.request("GET", url, headers=headers))
            # tweets = []
            tweets = json.loads(HttpResponse(popularSearch).content)
            #check if the request went through 
            if hasattr(tweets, 'error'):
                return HttpResponse(tweets)
            #check if the response has 'next' hash if so append it to the url
            # if hasattr(tweets, 'next'):
            #     for i in range(1, 5):
            #         new_req = requests.request("GET", url+"&next={}".format(tweets[i-1]['next']), headers=headers)
            #         tweets['results'].append(new_req['results'])
            #         if hasattr(new_req, 'next'):
            #             #request the next page
            #             continue
            #         else: 
            #             break

            # for response in fetchTwitter: 
            #     results = json.loads(HttpResponse(response).content)
            #     tweets['results'].append(results['results'])
            #popular Search
            print(len(tweets['statuses'])) 
            #recent Search
            # print(len(tweets['results'])) 
            calssify = {}
            calssify['sentimment'] = analize.SNL_Twitter.analyze(query, tweets)
            calssify['content']= tweets
            
            

            # print(calssify)
            # response = {tweets:calssify}
            # for item in json.loads(HttpResponse(fetchTwitter).content): 
            
            return HttpResponse(json.dumps(calssify), content_type='application/json')
            
        raise BadRequest('Invalid Request!')


    def first(req):
        # log.warning("Wrong URL")
        # data = 'oc2093'
        return render(req, 'first.html', {'name': 'Ahmed'})
        # return HttpResponse('Hello World!')

    



##new APP
# Bearer AAAAAAAAAAAAAAAAAAAAAJKAVgEAAAAAlJpPjhiR6zoOkW9kX4Z3mybV568%3DZUS51isbSfpuSiLJGFDXY0woi6sXyRDiCQCeIOhoxfwzcFhGNS
## key I1OTsG6u3zD1jrP3s32AgHuAH
### sec O8bk3Dc3XbxjPBgj2VZK4JTIQeyVj7ME4mli3wAFI4JC7cGvvm