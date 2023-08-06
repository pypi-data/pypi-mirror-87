'''
Podcast module.
'''

__all__ = (
    'Podcast',
)

import datetime
import email.utils
import json
import logging
import os
import re
import urllib.parse
import urllib.request

import feedparser
import pytz

#: The logger instance.
LOGGER   = logging.getLogger(__name__)

#: The local timezone to use.
TIMEZONE = pytz.timezone('Europe/Zurich')

#: The default retention in days.
DEFAULT_RETENTION = 7


class Podcast:
    '''
    A single podcast.

    :param str podcast_dir: The podcast directory
    '''

    #: The name of the metadata file.
    metadata_filename = '.podload'

    #: Accepted link mime types.
    accepted_types = (
        'audio/mpeg',
    )

    @classmethod
    def create(cls, podcasts_dir, url, retention=DEFAULT_RETENTION):
        '''
        Create a new podcast from an URL.

        This will create a new directory with the meta file in it.

        :param str podcasts_dir: The podcasts directory
        :param str url: The podcast URL
        :param int retention: The retention in days

        :return: The podcast instance
        :rtype: Podcast
        '''
        LOGGER.info('Creating new podcast from "%s"', url)

        title         = feedparser.parse(url).feed.title
        podcast_dir   = os.path.join(podcasts_dir, title)
        metadata_file = os.path.join(podcast_dir, cls.metadata_filename)

        if not os.path.exists(podcast_dir):
            os.makedirs(podcast_dir)

        if os.path.exists(metadata_file):
            LOGGER.error('Podcast metadata file "%s" is already existing', metadata_file)
        else:
            with open(metadata_file, 'w') as file:
                json.dump({
                    'url': url,
                    'title': title,
                    'retention': retention or DEFAULT_RETENTION,
                }, file)

        return cls(podcast_dir)

    def __init__(self, podcast_dir):
        '''
        Constructor.
        '''
        LOGGER.debug('Initialising podcast at "%s"', podcast_dir)

        self.podcast_dir      = podcast_dir
        self.metadata_file    = os.path.join(podcast_dir, self.metadata_filename)
        self.metadata         = {}
        self.current_download = None

        self.load_metadata()
        self.clean_metadata()

    def __str__(self):
        '''
        The informal string representation of the podcast.

        :return: The title
        :rtype: str
        '''
        return self.metadata['title']

    def __repr__(self):
        '''
        The official string representation of the podcast.

        :return: The class w/ title
        :rtype: str
        '''
        return f'<{self.__class__.__name__}: {self.metadata["title"]}>'

    @property
    def info(self):
        '''
        The informations of the podcasts.

        :return: The filename & title
        :rtype: generator
        '''
        for file in os.listdir(self.podcast_dir):
            if not file.startswith('.'):
                yield file, self.metadata.get('episodes', {}).get(file, '')

    def load_metadata(self):
        '''
        Load the metadata from disk.
        '''
        LOGGER.debug('Loading metadata from "%s"', self.metadata_file)

        with open(self.metadata_file, 'r') as file_handle:
            self.metadata = json.load(file_handle)

    def save_metadata(self):
        '''
        Save the metadata to disk.
        '''
        LOGGER.debug('Saving metadata to "%s"', self.metadata_file)

        with open(self.metadata_file, 'w') as file_handle:
            json.dump(self.metadata, file_handle)

    def clean_metadata(self):
        '''
        Clean the metadata.
        '''
        if 'episodes' not in self.metadata:
            return

        episodes = self.metadata['episodes']
        delete   = []

        for episode in episodes:
            if not os.path.exists(os.path.join(self.podcast_dir, episode)):
                delete.append(episode)

        for item in delete:
            del episodes[item]

        self.save_metadata()

    def clean(self, retention=None):
        '''
        Clean all podcast episodes which are older than the retention.

        :param retention: An alternative retention in days
        :type retention: None or int
        '''
        retention = retention or self.metadata.get('retention', DEFAULT_RETENTION)
        threshold = datetime.datetime.now() - datetime.timedelta(days=retention)

        for file in os.listdir(self.podcast_dir):
            drive = os.path.splitext(file)[0]
            if re.match(r'\d{4}(-\d{2}){2} \d{2}:\d{2}', drive):
                if datetime.datetime.strptime(drive, '%Y-%m-%d %H:%M') < threshold:
                    LOGGER.info('Deleting "%s"', file)
                    os.remove(os.path.join(self.podcast_dir, file))
                else:
                    LOGGER.debug('Not deleteing "%s" because it\'s within the retention', file)
            else:
                LOGGER.debug('Ignoring "%s" because filename doesn\'t match', file)

        self.clean_metadata()

    def set_retention(self, retention):
        '''
        Set a new retention.

        :param int retention: The retention in days
        '''
        LOGGER.info('Setting retention of "%s" to %d days', self, retention)
        self.metadata['retention'] = retention
        self.save_metadata()

    def parse(self):
        '''
        Parse the podcast feed.

        :return: The feed
        :rtype: dict
        '''
        url = self.metadata['url']

        LOGGER.info('Parsing podcasts at "%s"', url)

        feed = feedparser.parse(url)

        self.metadata['title'] = feed.feed.title  # pylint: disable=no-member
        self.save_metadata()

        return feed

    def download(self, retention=None, verify=False):  # pylint: disable=too-many-locals
        '''
        Download all episodes which are within the retention days.

        :param retention: An alternative retention in days
        :type retention: None or int
        :param bool verify: Verify the file size and redownload if missmatch
        '''
        retention = retention or self.metadata.get('retention', DEFAULT_RETENTION)
        episodes  = self.metadata.setdefault('episodes', {})
        threshold = datetime.datetime.now(tz=TIMEZONE) - datetime.timedelta(days=retention)
        feed      = self.parse()

        for entry in feed.entries:  # pylint: disable=no-member
            title     = entry.title
            published = email.utils.parsedate_to_datetime(entry.published)
            links     = [link for link in entry.links if link.type in self.accepted_types]

            if published < threshold:
                LOGGER.debug('Ignoring "%s" because it\'s older than %d days', title, retention)
                continue

            if not links:
                LOGGER.debug('Ignoring "%s" because no acceptable link types found', title)
                continue

            link      = links[0].href
            suffix    = os.path.splitext(urllib.parse.urlparse(link).path)[1]
            date_str  = published.strftime('%Y-%m-%d %H:%M')
            file_name = f'{date_str}{suffix}'
            file_path = os.path.join(self.podcast_dir, file_name)
            exists    = os.path.exists(file_path)

            if not verify and exists:
                LOGGER.debug('Ignoring "%s" because it\'s already existing', title)
                continue

            with urllib.request.urlopen(link) as response:
                if exists and int(response.headers['content-length']) == os.stat(file_path).st_size:
                    LOGGER.debug(
                        'Ignoring "%s" because it\'s already existing and filesize matches', title)
                    continue
                if exists:
                    LOGGER.warning('Redownloading "%s" as the file size missmatches', title)
                else:
                    LOGGER.info('Downloading podcast episode "%s" to "%s"', title, file_path)

                with open(file_path, 'wb') as file:
                    file.write(response.read())

                episodes[file_name] = title
                self.save_metadata()
