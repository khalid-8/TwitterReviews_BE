import pickle
import re, string, os
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
# from requests import models
from ..models import tweets_sentiment
from django.conf import settings
from .plots import plots as plt
# from django.core.files.images import ImageFile
import datetime
from django.utils import timezone



class SNL_Twitter():

    #Load the models
    # #English
    # filename = 'TwitterNLP/MLmodel/twitterReviews_model_V02.sav'
    # NLPmodel = pickle.load(open(filename, 'rb'))
    #Arabic
    filename1 = 'TwitterNLP/MLmodel/twitterReviews_model_ArabicV0.2.sav'
    NLP_ARmodel = pickle.load(open(filename1, 'rb'))
    #Load the model
    filename_new = 'TwitterNLP/MLmodel/twitterReviews_model_V02.sav'
    NLPmodel = pickle.load(open(filename_new, 'rb'))
    #Load Stop words
    #load english stop words
    en = open("{}/TwitterNLP/MiddleWare/stopwords/english".format(settings.BASE_DIR), 'r')
    stopWords = en.read()
    #load arabic stop words
    ar = open("{}/TwitterNLP/MiddleWare/stopwords/FullArabicSW.txt".format(settings.BASE_DIR), 'r')
    ar_stopWords = ar.read()
    ar_stopWords = ar_stopWords.split('\n')


    #function ... and remove stop words
    def remove_noise(tweet_tokens, stop_words = ()):
        cleaned_tokens = []
        for token, tag in pos_tag(tweet_tokens):
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

    #function to remove unwatned text from the tweet (i.e, URLs, Mentions, Search Term)
    def pre_clean(tweet, searchTerms=['']):
        clean_tweet = tweet.strip()
        clean_tweet = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', tweet)
        clean_tweet = re.sub("(@[A-Za-z0-9_]+)","", clean_tweet)
        clean_tweet = re.sub("['|’|]", '', clean_tweet)
        clean_tweet = re.sub("\n", '', clean_tweet)
        clean_tweet = re.sub("RT :", '',clean_tweet)
        if (len(searchTerms) > 1):
            for term in searchTerms:
                clean_tweet = re.sub(term, '', clean_tweet)
        else: clean_tweet = re.sub(searchTerms[0], '', clean_tweet)
        return clean_tweet

    #function to get the full text of the tweet as its returned from Twitter API
    def getFullText(tweet): 
        #if it was a popluar tweet
        if "full_text" in tweet.keys(): return tweet["full_text"]
        #if tweet was retweeted
        if "retweeted_status" in tweet.keys():
            if "extended_tweet" in tweet["retweeted_status"].keys(): return tweet["retweeted_status"]["extended_tweet"]["full_text"]
        #else if tweet wasn't reweeted    
        return tweet["extended_tweet"]["full_text"] if "extended_tweet" in tweet.keys() else tweet["text"]
    
    #function to get the tweet ID
    def getTweetID(tweet):
        if "retweeted_status" in tweet.keys():
            return tweet["retweeted_status"]["id_str"]
        return tweet["id_str"]


    def analyze(term, tweets, lang):
        # data = []
        # for tweet in tweets:
        #     data += tweet
        tokens_list = []

        #dict to hold the results
        results = {
            "postive": [],
            "negative": []
        }

        #toknize then classiy the tweets
        for tweet in tweets:
            clean_tweet = SNL_Twitter.pre_clean(SNL_Twitter.getFullText(tweet), term)
            tokens_list.append(SNL_Twitter.remove_noise(word_tokenize(clean_tweet), stop_words= SNL_Twitter.ar_stopWords if (lang == "ar") else SNL_Twitter.stopWords))

        for i in range(len(tokens_list)):
            if lang == "ar":
                sentiment = SNL_Twitter.NLPmodel.classify(dict([token, True] for token in tokens_list[i]))
            else:
                sentiment = SNL_Twitter.NLP_ARmodel.classify(dict([token, True] for token in tokens_list[i]))
            PopTweet_obj = {
                "id" : SNL_Twitter.getTweetID(tweets[i]),
                "date" : tweets[i]['created_at'],
                "tweet" : SNL_Twitter.getFullText(tweets[i]),
                "reply_count": 0,
                "retweet_count" : tweets[i]['retweet_count'],
                "favorite_count" : tweets[i]['favorite_count'], 
                "screen_name": (tweets[i]['user'])['name'],
                "username" : (tweets[i]['user'])['screen_name'],
                "profile_image_url": (tweets[i]['user'])['profile_image_url'],
                "user_id" : (tweets[i]['user'])['id'],
                "verified": (tweets[i]['user'])['verified']
            }
            if  sentiment == 'Positive':
                results['postive'].append(PopTweet_obj)
            elif sentiment == 'Negative':
                results['negative'].append(PopTweet_obj)

        
        #classifed tweets count
        tweet_count = len(results['postive']) + len(results['negative'])

        #make the plots
        plots = plt.plot_maker(len(results['postive']), 
                len(results['negative']), tweet_count, term)

        #add the tweets count to our reults
        results['tweet_count'] = tweet_count
        #add the search term to our results
        results['search_term'] = term

        #populate the results to the DB model
        modelObj = tweets_sentiment(
            search_term = term, 
            total_count = tweet_count,
            negative_count = len(results['negative']),
            postive_count = len(results['postive']), 
            postive_tweets = results['postive'],
            negative_tweets = results['negative'],
            charts_graph = plots[0],
            pie_graph = plots[1],
            expiration_date= timezone.now() + datetime.timedelta(minutes=30)
        )

        #save to the model to the DB
        modelObj.save()
        
        return tweets_sentiment.objects.filter(id=modelObj.id).values()[0]



# print(model_to_dict(modelObj))
# print(tweets_ids)
# print(f"Results: {len(results['postive'])} Postives, {len(results['negative'])} Negatives")