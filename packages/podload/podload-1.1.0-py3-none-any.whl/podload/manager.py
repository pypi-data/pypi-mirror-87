'''
Podcast manager module.
'''

__all__ = (
    'Manager',
)

import logging
import os

from .podcast import Podcast

LOGGER = logging.getLogger(__name__)


class Manager:
    '''
    The podcast manager.

    :param str podcasts_dir: The podcast directory
    '''

    def __init__(self, podcasts_dir):
        '''
        Constructor.
        '''
        self.podcasts_dir = podcasts_dir
        self.podcasts     = []

        self.load_podcasts()

    def load_podcasts(self):
        '''
        Load the podcasts from the disk.
        '''
        LOGGER.info('Loading podcasts from %s', self.podcasts_dir)

        if not os.path.exists(self.podcasts_dir):
            LOGGER.warning('Directory %s is missing, not loading podcasts', self.podcasts_dir)
            return

        for root, dirs, files in os.walk(self.podcasts_dir):  # pylint: disable=unused-variable
            for file in files:
                if file != Podcast.metadata_filename:
                    continue
                self.podcasts.append(Podcast(os.path.join(root)))

    def add_podcast(self, **kwargs):
        '''
        Add a new podcast.

        :param dict kwargs: The kwargs to pass to :meth:`podload.podcast.Podcast.create()`
        '''
        self.podcasts.append(Podcast.create(podcasts_dir=self.podcasts_dir, **kwargs))

    def delegate(self, method, **kwargs):
        '''
        Delegate a method to all podcasts.

        :param str method: The name of the method :class:`podload.podcast.Podcast`
        :param dict kwargs: The kwargs to pass to :meth:`podload.podcast.Podcast.download()`
        '''
        for podcast in self.podcasts:
            getattr(podcast, method)(**kwargs)

    def set_retention(self, podcast, retention):
        '''
        Set a new retention on a podcast.

        :param str podcast: The podcast title
        :param int retention: The retention in days
        '''
        for podcast_obj in self.podcasts:
            if podcast_obj.metadata['title'] == podcast:
                podcast_obj.set_retention(retention)

    def clean(self, **kwargs):
        '''
        Download all episodes.

        :param dict kwargs: The kwargs to pass to :meth:`podload.podcast.Podcast.download()`
        '''
        self.delegate('clean', **kwargs)

    def download(self, **kwargs):
        '''
        Download all episodes.

        :param dict kwargs: The kwargs to pass to :meth:`podload.podcast.Podcast.download()`
        '''
        self.delegate('download', **kwargs)
