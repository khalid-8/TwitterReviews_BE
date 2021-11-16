import pickle
import re, string, random, os
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
# from requests import models
from ..models import tweets_sentiment
from django.forms.models import model_to_dict
from django.conf import settings
from .plots import plots as plt
from django.core.files.images import ImageFile



class SNL_Twitter():

    #Load the model
    filename = 'TwitterNLP/MLmodel/twitterReviews_model_V02.sav'
    NLPmodel = pickle.load(open(filename, 'rb'))
    #Load Stop words
    #load the english stop words
    f = open("{}/TwitterNLP/MiddleWare/stopwords/english".format(settings.BASE_DIR), 'r')
    stopWords = f.read()

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


    def pre_clean(tweet):
        clean_tweet = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', tweet)
        clean_tweet = re.sub("(@[A-Za-z0-9_]+)","", clean_tweet)
        clean_tweet = re.sub("['|’|”|..|``|\n|\n\n]", '', clean_tweet)
        clean_tweet = re.sub('"', '', clean_tweet)
        return clean_tweet


        
    def analyze(term, tweets):
        # print(tweets)
        # data_len = 0
        # data = tweets['results']
        data = tweets['statuses']
        # for res in tweets['results']:
        #     data.append(res)
        #     data_len += len(res)

        # print("\n\n\n*************************")
        # print(data[0])
        # load the model from disk

        # custom_tokens = SNL_Twitter.remove_noise(word_tokenize(data))
        # result = NLPmodel.classify(dict([token, True] for token in custom_tokens))
        
        tokens_list = []

        #dict to hold the results
        results = {
            "postive": [],
            "negative": []
        }

        # print(stopWords)
        #toknize then classiy the tweets
        # for res in data:
        for tweet in data:
            # if tweet['lang'] != "en":
            #     continue  
            clean_tweet = SNL_Twitter.pre_clean(tweet['full_text'])
            tokens_list.append(SNL_Twitter.remove_noise(word_tokenize(clean_tweet), stop_words= SNL_Twitter.stopWords))

        for i in range(len(tokens_list)):
            sentiment = SNL_Twitter.NLPmodel.classify(dict([token, True] for token in tokens_list[i]))
            PopTweet_obj = {
                "id" : data[i]['id_str'],
                "date" : data[i]['created_at'],
                "tweet" : data[i]['full_text'],
                "reply_count": 0,
                "retweet_count" : data[i]['retweet_count'],
                "favorite_count" : data[i]['favorite_count'], 
                "screen_name": (data[i]['user'])['name'],
                "username" : (data[i]['user'])['screen_name'],
                "profile_image_url": (data[i]['user'])['profile_image_url'],
                "user_id" : (data[i]['user'])['id'],
                "verified": (data[i]['user'])['verified']
            }
            if  sentiment == 'Positive':
                results['postive'].append(PopTweet_obj)
                # tweets_ids['postive'].append(tokens_list['id'][i])
            elif sentiment == 'Negative':
                results['negative'].append(PopTweet_obj)
                
            #     results['postive'].append(tokens_list['tweet'][i])
            #     tweets_ids['postive'].append(tokens_list['id'][i])
            # elif sentiment == 'Negative':
            #     results['negative'].append(tokens_list['tweet'][i])
            #     tweets_ids['negative'].append(tokens_list['id'][i])

        
        #classifed tweets count
        tweet_count = len(results['postive']) + len(results['negative'])

        #make the plots
        plots = plt.plot_maker(len(results['postive']), 
                len(results['negative']), tweet_count, term)

        #add the tweets count to our reults
        results['tweet_count'] = tweet_count
        #add the search term to our results
        results['search_term'] = term
        # print(f'first:\n{type(plots[0])}\nSecond:\n{plots[1]}')
        #save the results to the DB
        model = tweets_sentiment(
            search_term = term, 
            total_count = tweets['search_metadata']['count'],
            negative_count = len(results['negative']),
            postive_count = len(results['postive']), 
            postive_tweets = results['postive'],
            negative_tweets = results['negative'],
            charts_graph = plots[0],
            pie_graph = plots[1]
        )


        model.save()

        # print(model_to_dict(model))
        # print(tweets_ids)
        # print(f"Results: {len(results['postive'])} Postives, {len(results['negative'])} Negatives")
        
        return [results, plots]


