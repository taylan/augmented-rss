from datetime import datetime
import PyRSS2Gen
from feeds import default_headers
from feeds.AugmentedFeedBase import AugmentedFeedBase
from bs4 import BeautifulSoup
from requests import get


class DilbertFeed(AugmentedFeedBase):
    def __init__(self):
        super(DilbertFeed, self).__init__('dilbert', 'http://feed.dilbert.com/dilbert/daily_strip?format=xml')

    @staticmethod
    def _get_comic_image_path(url):
        path = BeautifulSoup(get(url, headers=default_headers).text).select('.STR_Image img')[0]["src"]
        return 'http://www.dilbert.com/{0}'.format(path)

    def augment(self, feed=None):
        if not feed:
            feed = self._retreive_feed()

        items = [
            PyRSS2Gen.RSSItem(
                title=x.title,
                link=x.link,
                description='<img src="{0}" />'.format(self._get_comic_image_path(x.id)),
                guid=x.id,
                pubDate=datetime(
                    x.published_parsed[0],
                    x.published_parsed[1],
                    x.published_parsed[2],
                    x.published_parsed[3],
                    x.published_parsed[4],
                    x.published_parsed[5])
            )

            for x in feed.entries[:4]
        ]

        return PyRSS2Gen.RSS2(
            title=feed['feed'].get("title"),
            link=feed['feed'].get("link"),
            description=feed['feed'].get("description"),
            language=feed['feed'].get("language"),
            copyright=feed['feed'].get("copyright"),
            managingEditor=feed.feed['publisher'],
            pubDate=feed.feed['published'],
            lastBuildDate=feed.feed['published'],
            items=items
        )
