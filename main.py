import os
import tweepy
import csv
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API credentials from .env
bearer_token = os.getenv("BEARER_TOKEN")

# Authenticate using Tweepy Client (Twitter API v2)
client = tweepy.Client(bearer_token=bearer_token)

class SentimentAnalysis:
    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):
        searchTerm = input("Enter Keyword/Tag to search about: ")
        NoOfTerms = int(input("Enter how many tweets to search: "))

        query = f"{searchTerm} -is:retweet lang:en"
        tweets = client.search_recent_tweets(query=query, max_results=min(NoOfTerms, 100), tweet_fields=["text"])

        if not tweets.data:
            print("❌ No tweets found. Try a different keyword.")
            return

        csvFile = open('result.csv', 'a')
        csvWriter = csv.writer(csvFile)

        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0

        for tweet in tweets.data:
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity

            if analysis.sentiment.polarity == 0:
                neutral += 1
            elif 0 < analysis.sentiment.polarity <= 0.3:
                wpositive += 1
            elif 0.3 < analysis.sentiment.polarity <= 0.6:
                positive += 1
            elif 0.6 < analysis.sentiment.polarity <= 1:
                spositive += 1
            elif -0.3 < analysis.sentiment.polarity <= 0:
                wnegative += 1
            elif -0.6 < analysis.sentiment.polarity <= -0.3:
                negative += 1
            elif -1 < analysis.sentiment.polarity <= -0.6:
                snegative += 1

        csvWriter.writerow(self.tweetText)
        csvFile.close()

        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        polarity = polarity / NoOfTerms

        print(f"How people are reacting on {searchTerm} by analyzing {NoOfTerms} tweets.\n")
        print("General Report: ")
        if polarity == 0:
            print("Neutral")
        elif 0 < polarity <= 0.3:
            print("Weakly Positive")
        elif 0.3 < polarity <= 0.6:
            print("Positive")
        elif 0.6 < polarity <= 1:
            print("Strongly Positive")
        elif -0.3 < polarity <= 0:
            print("Weakly Negative")
        elif -0.6 < polarity <= -0.3:
            print("Negative")
        elif -1 < polarity <= -0.6:
            print("Strongly Negative")

        print("\nDetailed Report:")
        print(f"{positive}% people thought it was positive")
        print(f"{wpositive}% people thought it was weakly positive")
        print(f"{spositive}% people thought it was strongly positive")
        print(f"{negative}% people thought it was negative")
        print(f"{wnegative}% people thought it was weakly negative")
        print(f"{snegative}% people thought it was strongly negative")
        print(f"{neutral}% people thought it was neutral")

        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)

    def cleanTweet(self, tweet):
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\ / \ / \S+)", " ", tweet).split())

    def percentage(self, part, whole):
        return format(100 * float(part) / float(whole), '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = [
            f'Positive [{positive}%]', f'Weakly Positive [{wpositive}%]', f'Strongly Positive [{spositive}%]',
            f'Neutral [{neutral}%]', f'Negative [{negative}%]', f'Weakly Negative [{wnegative}%]', f'Strongly Negative [{snegative}%]'
        ]
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title(f'How people are reacting on {searchTerm} by analyzing {noOfSearchTerms} Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()
