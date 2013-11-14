default_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'}

from .ToothpasteForDinnerFeed import ToothpasteForDinnerFeed
from .DilbertFeed import DilbertFeed
from .SaturdayMorningBreakfastCerealFeed import SaturdayMorningBreakfastCerealFeed

_instances = [instance() for name, instance in globals().items() if name.endswith('Feed')]
feeds = {i.name: i for i in _instances}

__all__ = ['feeds']