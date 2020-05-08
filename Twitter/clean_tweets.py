from re import sub
from hazm import Normalizer, Lemmatizer, Stemmer, InformalNormalizer
import sys


def omit_other_info(file_path):
    with open(file_path,encoding="utf8") as file:
        tweets=file.readlines()

    clean_tweets=[]
    for tweet in tweets:
        index=tweet.find(">")
        tweet=tweet[index+2:].replace("\n", "")
        clean_tweets.append(tweet)

    return clean_tweets


def no_links(tweets):
    no_link_tweets=[]
    # deleting links
    for tweet in tweets:
        no_link_tweet = sub(r'http\S+', '', tweet)
        no_link_tweets.append(no_link_tweet)

    # deleting empty strings
    no_link_tweets[:] = [tweet for tweet in no_link_tweets if tweet.replace(" ", "") != '']
    return no_link_tweets

def no_pics(tweets):
    no_pics_tweets=[]
    # deleting links
    for tweet in tweets:
        no_pics_tweet = sub(r'pic.twitter.com\S+', '', tweet)
        no_pics_tweets.append(no_pics_tweet)

    # deleting empty strings
    no_pics_tweets[:] = [tweet for tweet in no_pics_tweets if tweet.replace(" ", "") != '']
    return no_pics_tweets


def normalizer(tweets):
    normalizer_tweets=[]
    for tweet in tweets:
      normalizer_tweets.append(Normalizer().normalize(tweet))

    return normalizer_tweets

def informal_normalizer(tweets):
    normalizer_tweets=[]
    counter=0
    total=len(tweets)
    for tweet in tweets:
        sents = InformalNormalizer().normalize(tweet)
        sents = [[word[0] for word in sent] for sent in sents]
        sents = [' '.join(sent) for sent in sents]
        text = ''.join(sents)
        normalizer_tweets.append(text)
        counter+=1
        print("\rEpisode {}/{}".format(counter,total), end="")
        sys.stdout.flush()

    return normalizer_tweets



def stemmer(tweets):
    stemmer_tweets=[]
    for tweet in tweets:
      stemmer_tweets.append(Stemmer().stem(tweet))

    return stemmer_tweets

def lemmatizer(tweets):
    lemmatizer_tweets=[]
    for tweet in tweets:
      lemmatizer_tweets.append(Lemmatizer().lemmatize(tweet))

    return lemmatizer_tweets


def clean_tweets(file_path):
    cleaned_tweets=omit_other_info(file_path)
    cleaned_tweets=no_links(cleaned_tweets)
    cleaned_tweets=no_pics(cleaned_tweets)
    cleaned_tweets=normalizer(cleaned_tweets)
    cleaned_tweets=informal_normalizer(cleaned_tweets)
    cleaned_tweets=stemmer(cleaned_tweets)
##    cleaned_tweets=lemmatizer(cleaned_tweets)
    
    return cleaned_tweets

def clean_twitter_account(username):
    tweets=clean_tweets('tweets/{}.txt'.format(username))
    print(len(tweets))
####    print(tweets[233])
    with open('tweets/{}_result.txt'.format(username),'w',encoding="utf8") as file:
        for tweet in tweets:
            file.write(tweet)

    


if __name__ == '__main__':
##    clean_twitter_account('a_sheikhahmadi')
    clean_twitter_account('Hedyeh_AD')
    
