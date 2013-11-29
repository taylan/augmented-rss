from datetime import datetime
import PyRSS2Gen
from bs4 import BeautifulSoup
from feeds import default_headers
from feeds.AugmentedFeedBase import AugmentedFeedBase
from requests import get
from re import search, DOTALL, IGNORECASE


class HoverStatesFeed(AugmentedFeedBase):
    def __init__(self):
        super(HoverStatesFeed, self).__init__('hover-states', 'http://feeds.feedburner.com/HoverStates')

    @staticmethod
    def _get_comic_image_path(url):
        return BeautifulSoup(get(url, headers=default_headers).text).select('.btn-launch')[0]["href"]

    @staticmethod
    def _insert_site_link(content, link):
        return '{0}<br><br><a href="{1}">Launch Site</a>'.format(search("(<img .* />)", content, DOTALL | IGNORECASE).group(1), link)

    def augment(self, feed=None):
        if not feed:
            feed = self._retreive_feed()

        items = [
            PyRSS2Gen.RSSItem(
                title=x.title,
                link=x.link,
                description=self._insert_site_link(x.content[0]['value'], self._get_comic_image_path(x.link)),
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
            description='Hover States',
            items=items
        )



