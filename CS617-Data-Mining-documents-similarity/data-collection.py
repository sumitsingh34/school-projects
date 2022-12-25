import sys
import os
from urllib import request
import feedparser
from html.parser import HTMLParser
from xml.etree import cElementTree as etree


TAG = 'p'

class MyHTMLParser(HTMLParser):

    printflag = False

    def __init__(self):
        HTMLParser.__init__(self)
        self.messages = []

    def handle_starttag(self, tag, attrs):
        if tag == TAG:
            self.printflag = True

    def handle_endtag(self, tag):
        if tag == TAG:
            self.printflag = False

    def handle_data(self, data):
        if self.printflag:
            #print(data)
            self.messages.append(data)


def main():

    #https://www.bbc.co.uk/news/10628494#userss
    #f = feedparser.parse("http://feeds.bbci.co.uk/news/world/rss.xml")
    #f = feedparser.parse("http://rss.cnn.com/rss/edition_world.rss")
    #f = feedparser.parse("https://www.buzzfeed.com/world.xml")

    rssFeedDict = {
                     'business': ['http://feeds.bbci.co.uk/news/business/rss.xml','https://thewest.com.au/business/rss'],
                     'politics': ['http://feeds.bbci.co.uk/news/politics/rss.xml','https://www1.cbn.com/rss-cbn-news-politics.xml'],
                    'health': ['http://feeds.bbci.co.uk/news/health/rss.xml','https://www1.cbn.com/rss-cbn-articles-health.xml','https://moxie.foxnews.com/google-publisher/health.xml','https://www.menshealth.com/rss/all.xml/'],
                    'gaming':['http://feeds.ign.com/ign/all','http://feeds.feedburner.com/RockPaperShotgun','http://feeds.feedburner.com/VGChartz'],
                    'science_and_environment': ['http://feeds.bbci.co.uk/news/science_and_environment/rss.xml','http://feeds.nature.com/nature/rss/current','http://www.thestar.com/content/thestar/feed.RSSManagerServlet.articles.life.technology.rss'],
                    'technology': ['http://feeds.bbci.co.uk/news/technology/rss.xml','https://moxie.foxnews.com/google-publisher/tech.xml','https://www.latimes.com/business/technology/rss2.0.xml'],
                    'entertainment_and_arts': ['http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml','https://www1.cbn.com/rss-cbn-articles-entertainment.xml','https://www1.cbn.com/rss-cbn-blogs-hollywoodinsight.xml','https://thewest.com.au/entertainment/rss','https://www1.cbn.com/rss-cbn-articles-cbnmusic.xml'],
                    'finance':['https://www1.cbn.com/rss-cbn-news-finance.xml','https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664','https://www1.cbn.com/rss-cbn-articles-finances.xml','https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=21324812'],
                    'sports':['https://moxie.foxnews.com/google-publisher/sports.xml','https://www.cbssports.com/rss/headlines/boxing/','https://www.cbssports.com/rss/headlines/mlb/','https://www.espn.com/espn/rss/rpm/news'],
                    'travel':['https://thewest.com.au/travel/rss','https://moxie.foxnews.com/google-publisher/travel.xml']
                    }

    for topic_name,rssFeedList in rssFeedDict.items():
        #topic_name = rssFeed.split('/')[-2]
        num = 0
        for rssFeed in rssFeedList:
            f = feedparser.parse(rssFeed)

            for x in f['entries']:
                num +=1

                if num >= 150: # taking only 150 articales max
                    break

                with request.urlopen(x['link']) as response:
                    html = response.read().decode('utf-8')
                    parser =  MyHTMLParser()
                    parser.feed(html)
    #                 print(x['title'],'==>',parser.messages)
    #                 input('?')

                path = f'RawData/{topic_name}'
                if not os.path.exists(path):
                    os.makedirs(path)

                #file_name = x['title'].strip()[:50]+'.txt'
                file_name = f"{num}.txt"
    #             print(file_name)
    #             input()
#                 special_char = '@!#$%^&*()<>?/\|}{~:;[]""\n'
#                 file_name = [ ch.replace(ch,'_') if ch in special_char else ch for ch in file_name ]
#                 file_name = "".join(file_name)

                with open(os.path.join(path,file_name),'w', encoding='utf-8') as f:
                    f.write("".join(parser.messages))


if __name__ == "__main__":

    main()
