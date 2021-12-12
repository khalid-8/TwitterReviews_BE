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
            request = decode(req.body, 'utf-8')
            request = json.loads(request)

            lang = request['lan']
            query = request['query']
            print(f"Search Query: {query}")
            #if query is empty
            if query.isspace(): 
                return HttpResponse("Bad Request!", status=400, content_type='text/plain')
            #web encode the search term i.e replace spaces with %20
            query_P = urllib.parse.quote(query)
            #web encode the search term i.e replace spaces with %20
            query_P = urllib.parse.quote(query)
            # print(f"Search Query: {query}")
            #first env 'dev' for 30day search
            recentURL = f"https://api.twitter.com/1.1/tweets/search/30day/dev.json?query={query_P} lang:{lang}"
            #second env 'twitterReviews' for full archive search
            fullarchiveURL = f"https://api.twitter.com/1.1/tweets/search/fullarchive/twitterReviews.json?query={query_P} lang:{lang}" #&next=eyJtYXhJZCI6MTQ2MjA2NDQwMDE1MjY0NTYzNH0=
            #search for popular tweet
            popularURL = f'https://api.twitter.com/1.1/search/tweets.json?q={query_P}&lang={lang}&result_type=popular&tweet_mode=extended'
            #Twitter api v2 recent search 
            apiV2URL = f'https://api.twitter.com/2/tweets/search/recent?query={query_P} lang:{lang}&tweet.fields=id,text,lang,public_metrics&max_results=10&user.fields=id,description,created_at,username,profile_image_url,verified'

            # first env 'dev' Bearer Token
            headers = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAACsx%2BQAAAAAA2%2F9Onm5ZIzMJotHeoJQpCFtJV10%3DSK9tQfBsNZirwauxiFzDXl80sB7M0xMGLaAbtGZkhReYFBA1Rz',
            }
            # second env 'twitterReviews' Bearer Token
            headers1 = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAJKAVgEAAAAAlJpPjhiR6zoOkW9kX4Z3mybV568%3DZUS51isbSfpuSiLJGFDXY0woi6sXyRDiCQCeIOhoxfwzcFhGNS',
            }

            tweetsList = []

            #make POPULAR and full archive search
            popularSearch = requests.request("GET", popularURL, headers=headers1)
            poptweets = json.loads(popularSearch.content)
            if 'error' in poptweets.keys():
                    print(poptweets["error"])
                    # HttpResponse(poptweets["error"], content_type='application/json', status=400)
            else:
                tweetsList.append(poptweets["statuses"])

            fullArchiveSearch = requests.request("GET", recentURL, headers=headers)
            arctweets = json.loads(fullArchiveSearch.content)
            if 'error' in arctweets.keys():
                print(arctweets["error"])
                # HttpResponse(arctweets["error"], content_type='application/json', status=400)
            else: tweetsList.append(arctweets["results"])
            
            if len(tweetsList) < 1:
                print("0 Tweets were found")
                # return HttpResponse("No Tweet were Found", status=404, content_type='text/plain')
            
            print(len(tweetsList)) 

            calssify = {}
            calssify['sentimment'] = analize.SNL_Twitter.analyze(query, tweetsList, lang)
            calssify['content']= tweetsList
            
            
            return HttpResponse(json.dumps(calssify), content_type='application/json', status=200)
            
        raise BadRequest('Invalid Request!')


    def SearchTwitter(query):
        tweetsList = []
        next_search = ''
        #web encode the search term i.e replace spaces with %20
        query_P = urllib.parse.quote(query)
        print(f"Search Query: {query}")
        #first env 'dev' for 30day search
        recentURL = "https://api.twitter.com/1.1/tweets/search/30day/dev.json?query={} lang:ar".format(query_P)
        #second env 'twitterReviews' for full archive search
        fullarchiveURL = "https://api.twitter.com/1.1/tweets/search/fullarchive/twitterReviews.json?query={} lang:ar".format(query_P) #&next=eyJtYXhJZCI6MTQ2MjA2NDQwMDE1MjY0NTYzNH0=
        #search for popular tweet
        popularURL = 'https://api.twitter.com/1.1/search/tweets.json?q={}&lang=ar&result_type=popular&tweet_mode=extended'.format(query_P)
        #Twitter api v2 recent search 
        apiV2URL = 'https://api.twitter.com/2/tweets/search/recent?query={} lang:ar&tweet.fields=id,text,lang,public_metrics&max_results=10&user.fields=id,description,created_at,username,profile_image_url,verified'.format(query_P)

        # first env 'dev' Bearer Token
        headers = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAACsx%2BQAAAAAA2%2F9Onm5ZIzMJotHeoJQpCFtJV10%3DSK9tQfBsNZirwauxiFzDXl80sB7M0xMGLaAbtGZkhReYFBA1Rz',
        }
        # second env 'twitterReviews' Bearer Token
        headers1 = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAJKAVgEAAAAAlJpPjhiR6zoOkW9kX4Z3mybV568%3DZUS51isbSfpuSiLJGFDXY0woi6sXyRDiCQCeIOhoxfwzcFhGNS',
        }

        #make POPULAR and full archive search
        popularSearch = requests.request("GET", popularURL, headers=headers1)
        poptweets = json.loads(popularSearch.content)
        if 'error' in poptweets.keys():
                print(poptweets["error"])
        else:
            tweetsList.append(poptweets["statuses"])
        
        
        for i in range(2):
            if(i > 0):
    #             fullarchiveURL = f"https://api.twitter.com/1.1/tweets/search/fullarchive/twitterReviews.json?query={query_P} lang:ar&next={next_search}"
                recentURL = f"https://api.twitter.com/1.1/tweets/search/30day/dev.json?query={query_P} lang:ar&next={next_search}"
            fullArchiveSearch = requests.request("GET", recentURL, headers=headers)
            arctweets = json.loads(fullArchiveSearch.content)
            if 'error' in arctweets.keys():
                print(arctweets["error"]); break
            tweetsList.append(arctweets["results"])
            next_search = arctweets["next"]
            if ("next" in arctweets.keys() == False): break
            time.sleep(1)
            
        
        return tweetsList






    def first(req):
        # log.warning("Wrong URL")
        # data = 'oc2093'
        return render(req, 'first.html', {'name': 'Ahmed'})
        # return HttpResponse('Hello World!')

    



##new APP
# Bearer AAAAAAAAAAAAAAAAAAAAAJKAVgEAAAAAlJpPjhiR6zoOkW9kX4Z3mybV568%3DZUS51isbSfpuSiLJGFDXY0woi6sXyRDiCQCeIOhoxfwzcFhGNS
## key I1OTsG6u3zD1jrP3s32AgHuAH
### sec O8bk3Dc3XbxjPBgj2VZK4JTIQeyVj7ME4mli3wAFI4JC7cGvvm