from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import re, string
import nltk
tweets_texts = df["text"].tolist()
stopwords=stopwords.words('english')
english_vocab = set(w.lower() for w in nltk.corpus.words.words())

def process_tweet_text(tweet):
   if tweet.startswith('@null'):
       return "[Tweet not available]"
   tweet = re.sub(r'\$\w*','',tweet) # Remove tickers
   tweet = re.sub(r'https?:\/\/.*\/\w*','',tweet) # Remove hyperlinks
   tweet = re.sub(r'['+string.punctuation+']+', ' ',tweet) # Remove puncutations like 's
   twtok = TweetTokenizer(strip_handles=True, reduce_len=True)
   tokens = twtok.tokenize(tweet)
   tokens = [i.lower() for i in tokens if i not in stopwords and len(i) > 2 and
             i in english_vocab]
   return tokens

 words = []
 for tw in tweets_texts:
      words += process_tweet_text(tw)
