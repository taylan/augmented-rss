from datetime import datetime
import PyRSS2Gen
from feeds import default_headers
from .AugmentedFeedBase import AugmentedFeedBase
from bs4 import BeautifulSoup
from requests import get


class AwwwardsFeed(AugmentedFeedBase):
    def __init__(self):
        super(AwwwardsFeed, self).__init__('awwwards', 'http://feeds.feedburner.com/awwwards-sites-of-the-day')

    @staticmethod
    def _get_page_url(url):
        return BeautifulSoup(get(url, headers=default_headers).text).select('.view-site')[0]["href"]

    def augment(self, feed=None):
        if not feed:
            feed = self._retreive_feed()

        items = [
            PyRSS2Gen.RSSItem(
                title=x.title,
                link=x.link,
                description='{0}<br><a href="{1}">View Site</a>'.format(x.description, self._get_page_url(x.link)),
                pubDate=datetime(
                    x.published_parsed[0],
                    x.published_parsed[1],
                    x.published_parsed[2],
                    x.published_parsed[3],
                    x.published_parsed[4],
                    x.published_parsed[5])
            )

            for x in feed.entries[:5]
        ]

        return PyRSS2Gen.RSS2(
            title=feed['feed'].get('title'),
            link=feed['feed'].get('link'),
            description=feed['feed'].get('description'),
            pubDate=feed.feed['updated'],
            lastBuildDate=feed.feed['updated'],
            items=items
        )
