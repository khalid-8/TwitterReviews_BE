from codecs import decode
from django.http import JsonResponse, HttpResponse, response
import requests, logging, json, urllib
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import BadRequest
from dotenv import load_dotenv
import os

# import logging
from .MiddleWare import analize
import datetime
from django.utils import timezone
from .models import userIpAddress

# Create instatnce of logger
log = logging.getLogger("django")
# load the environment variables
load_dotenv()
recent = os.getenv("RECENT_URL")
fullarchive = os.getenv("FULL_ARCHIVE_URL")
popular = os.getenv("POUPLAR_URL")
apiV2 = os.getenv("POUPLAR_URL")
bearer = os.getenv("FIRST_BEARER")
second_bearer = os.getenv("SECOND_BEARER")


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
            print(request)
            #if query is empty
            if query.isspace(): 
                return HttpResponse("Bad Request!", status=400, content_type='text/plain')

            #check for elgibilgty 
            if (Analize.check_and_update_eligibility(request['ip_address']) == False):
                return HttpResponse("User Exceeded Daily Limit", status=401, content_type='text/plain')

            #web encode the search term i.e replace spaces with %20
            query_P = urllib.parse.quote(query)
            #web encode the search term i.e replace spaces with %20
            query_P = urllib.parse.quote(query)
            # print(f"Search Query: {query}")
            #first env 'dev' for 30day search
            recentURL = f"{recent}query={query_P} lang:{lang}"
            print(f"Recent URL: {recentURL}")

            #second env 'twitterReviews' for full archive search
            fullarchiveURL = f"{fullarchive}query={query_P} lang:{lang}" #&next=eyJtYXhJZCI6MTQ2MjA2NDQwMDE1MjY0NTYzNH0=
            
            #search for popular tweet
            popularURL = f"{popular}q={query_P}&lang={lang}&result_type=popular&tweet_mode=extended"
        
            #Twitter api v2 recent search 
            apiV2URL = f"{apiV2}query={query_P} lang:{lang}&tweet.fields=id,text,lang,public_metrics&max_results=10&user.fields=id,description,created_at,username,profile_image_url,verified"

            # first env 'dev' Bearer Token
            headers = {
            'Authorization': bearer,
            }
            # second env 'twitterReviews' Bearer Token
            headers1 = {
            'Authorization': second_bearer,
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

    
    #check if the user didn't exceed the number of searches (3 per user) using their IP address
    def check_and_update_eligibility(ip): 
        DBobject = userIpAddress.objects.filter(ip_address=ip)
        # ip exist in the DB
        if (DBobject):
            num_req = DBobject.values("number_of_requests").first()["number_of_requests"]
            # print("******************************")
            # print()
            #number of requests exceeded the daily limit
            if (num_req == 3):
                return False
            #otherwise update the number of requests 
            DBobject.update(number_of_requests= num_req+1) 
            return True
        #if the ip dosen't exist in the DB add it
        add_User_IpAddress(ip)
        return True
        #if(DBobject):
            


def add_User_IpAddress(ip_add):
    # Create an instance of foo with expiration date now + one day
    ipModel = userIpAddress(
        ip_address = ip_add,
        expiration_date=timezone.now() + datetime.timedelta(days=1))

    ipModel.save()
    # objects.create()
