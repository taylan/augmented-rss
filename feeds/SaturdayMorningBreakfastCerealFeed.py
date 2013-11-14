from datetime import datetime
import PyRSS2Gen
from feeds.AugmentedFeedBase import AugmentedFeedBase
from requests import get
from bs4 import BeautifulSoup
from feeds import default_headers
from re import sub


class SaturdayMorningBreakfastCerealFeed(AugmentedFeedBase):
    def __init__(self):
        super(SaturdayMorningBreakfastCerealFeed, self).__init__('smbc', 'http://feeds.feedburner.com/smbc-comics/PvLb')

    @staticmethod
    def _get_extra_image_url(url):
        return BeautifulSoup(get(url, headers=default_headers).text).select('#aftercomic img')[0]["src"]

    @staticmethod
    def _augment_description(desc, extra_img_url):
        return sub('(?si)(<img src="[a-zA-Z0-9:/.-]+">)', r'\1<br/><img src="{0}" /><br>'.format(extra_img_url), desc)

    def augment(self, feed=None):
        if not feed:
            feed = self._retreive_feed()

        for e in feed.entries[:1]:
            print(self._get_extra_image_url(e.feedburner_origlink))

        items = [
            PyRSS2Gen.RSSItem(
                title=x.title,
                link=x.link,
                description=self._augment_description(x.description, self._get_extra_image_url(x.feedburner_origlink)),
                pubDate=datetime(
                    x.published_parsed[0],
                    x.published_parsed[1],
                    x.published_parsed[2],
                    x.published_parsed[3],
                    x.published_parsed[4],
                    x.published_parsed[5])
            )

            for x in feed.entries
        ]

        rss = PyRSS2Gen.RSS2(
            title=feed['feed'].get('title'),
            link=feed['feed'].get('link'),
            description=feed['feed'].get('description'),
            language=feed['feed'].get('language'),
            items=items
        )

        return rss

