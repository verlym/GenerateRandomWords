# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 09:19:43 2018

@author: Verly
"""
from collections import Counter
from itertools import chain, imap
from operator import itemgetter
import math
import tweepy
import time
import json

consumerKey="qQgqiGQeLcFE1t8rh8jIRvcQk"
consumerSecret="Ii3nUh1h41iBN6OvrIYSJbi8fGdWk4gYZR5VyBRq612wB2yR1b"
accessToken="832981398-m4iDqr0DFwyVRlP0MQu7tCeLpF7w0Unesx05Y1bX"
accessSecret="dMyh8JeOuPwJl5sx8IP8fVIX2KvCCoQhchdImhDpSVXQu"

class PrintListener(tweepy.StreamListener):
    def __init__(self, time_limit=10):
        self.start_time = time.time()
        self.limit = time_limit
        self.semuakata=[]
        self.semuahuruf=[]
        self.kata=[]
        super(PrintListener, self).__init__()
    
    
    def on_data(self, data):
        #stream selama 10 detik
        if (time.time() - self.start_time) < self.limit:
        # Decode JSON data
            try:
                tweet = json.loads(data)
                if "text" in tweet:
                    tweets = tweet["text"].encode('ascii', 'ignore')
                    self.semuahuruf.extend(list(tweets))
                    self.semuakata.extend(list(tweets.split()))
            except KeyError:
                print ""        
        else:
            #menghitung panjang kata untuk menetukan kata yang dibentuk
            panjangkata= math.ceil(len(self.semuahuruf)/len(self.semuakata))
            max=int(panjangkata)
            counter = Counter(chain.from_iterable(imap(set, self.semuahuruf)))
            self.kata = map(itemgetter(0), counter.most_common(max))
            self.kata[:max]
            #print kata dari kombinasi huruf terbanyak
            print "kata yang terbentuk: ","".join(x for x in self.kata).replace(" ","")
            
            return False
        
    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    listener = PrintListener()

    # otentikasi Twitter
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessSecret)

    stream = tweepy.Stream(auth, listener)
    stream.sample()