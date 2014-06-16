from datetime import datetime
import PyRSS2Gen
from bs4 import BeautifulSoup
from feeds import default_headers
from feeds.AugmentedFeedBase import AugmentedFeedBase
import requests


class ToothpasteForDinnerFeed(AugmentedFeedBase):
    def __init__(self):
        super(ToothpasteForDinnerFeed, self).__init__('tpfd', 'http://www.toothpastefordinner.com/rss/rss.php')

    @staticmethod
    def _get_comic_image_path(images, ts):
        dt = datetime.fromtimestamp(ts).strftime('%m%d%y')
        src = [img for img in images if dt in img]
        return src[0] if src else ''

    def augment(self, feed=None):
        if not feed:
            feed = self._retreive_feed()
        images = [img['src'] for img in BeautifulSoup(requests.get('http://toothpastefordinner.com/', headers=default_headers).text).select('img.comic')]

        items = [
            PyRSS2Gen.RSSItem(
                title=x.title,
                link=x.link,
                description='<img src="{0}" />{1}'.format(self._get_comic_image_path(images, int(x.guid.split('=')[1])), x.description),
                guid=x.link,
                pubDate=datetime(
                    x.published_parsed[0],
                    x.published_parsed[1],
                    x.published_parsed[2],
                    x.published_parsed[3],
                    x.published_parsed[4],
                    x.published_parsed[5])
            )

            for x in feed.entries[:10]
        ]

        rss = PyRSS2Gen.RSS2(
            title=feed['feed'].get('title'),
            link=feed['feed'].get('link'),
            description=feed['feed'].get('description'),
            language=feed['feed'].get('language'),
            copyright=feed['feed'].get('copyright'),
            managingEditor=feed.feed['publisher'],
            pubDate=feed.feed['published'],
            lastBuildDate=feed.feed['published'],
            docs=feed.feed['docs'],
            items=items
        )

        return rss
