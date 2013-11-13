import feedparser


class AugmentedFeedBase(object):
    def __init__(self, name, url):
        self._name = name
        self._url = url

    @property
    def name(self):
        return self._name

    def _retreive_feed(self):
        return feedparser.parse(self._url)

    def augment(self, feed=None):
        return feed

    def __repr__(self):
        return 'type: {0} - name: {1}, url: {2}'.format(self.__class__.__name__, self.name, self._url)
