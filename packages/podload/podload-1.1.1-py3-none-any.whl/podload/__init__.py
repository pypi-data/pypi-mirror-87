'''
Podload module.
'''

import argparse
import logging

from .manager import *
from .podcast import *


def help_formatter(prog):
    '''
    The help formatter for the argument parser.

    :param str prog: The prog

    :return: The help formatter
    :rtype: argparse.HelpFormatter
    '''
    return argparse.HelpFormatter(prog, max_help_position=40)


def main():
    '''
    Run the CLI script.
    '''
    parser = argparse.ArgumentParser(
        description='The simple podcast loader.',
        formatter_class=help_formatter
    )

    retention_args = '-r', '--retention'
    retention_kwargs = {'type': int, 'help': 'an alternative retention in days'}

    parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')
    parser.add_argument('directory', help='the name of the podcasts directory')

    subparsers = parser.add_subparsers(dest='action', required=True)

    subparsers.add_parser(name='info', help='display the podcast infos')

    clean = subparsers.add_parser(name='clean', help='clean old episodes')
    clean.add_argument(*retention_args, **retention_kwargs)

    add = subparsers.add_parser(name='add', help='add a new podcast')
    add.add_argument('url', help='a podcast URL to add')
    add.add_argument(*retention_args, **retention_kwargs)

    download = subparsers.add_parser(name='download', help='download the latest episodes')
    download.add_argument(*retention_args, **retention_kwargs)
    download.add_argument('-v', '--verify', action='store_true', help='verify the file size')

    retention = subparsers.add_parser(name='set-retention', help='set a new retention')
    retention.add_argument('podcast', help='the podcast title')
    retention.add_argument('retention', type=int, help='the new retention in days')

    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.DEBUG if args.debug else logging.INFO,
    )

    manager = Manager(args.directory)

    if args.action == 'info':
        for podcast in manager.podcasts:
            print(f'\n{podcast} ({podcast.metadata.get("retention")} days retention):')
            for file, title in podcast.info:
                print(f'    {file}  {title}')

    elif args.action == 'clean':
        manager.clean(retention=args.retention)

    elif args.action == 'add':
        manager.add_podcast(url=args.url, retention=args.retention)

    elif args.action == 'download':
        manager.download(retention=args.retention, verify=args.verify)

    elif args.action == 'set-retention':
        manager.set_retention(podcast=args.podcast, retention=args.retention)


if __name__ == '__main__':
    main()
