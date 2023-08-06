import logging
import re

from pathlib import Path

from itsicli.use_cases.commands.base import BaseCommand, request_input
from itsicli.use_cases.files import UseCaseConfig
from itsicli.use_cases.scaffold import Scaffolder


def valid_id(id_value):
    return re.search('^[\w\-_]+$', id_value)


INVALID_ID = 'Use case id can only contain alphanumeric, underscore, or dash characters.\n'


class InitCommand(BaseCommand):

    HELP = 'initialize an ITSI Use Case'

    NAME = 'init'

    class Args(object):
        USE_CASE_ID = 'use_case_id'
        USE_CASE_TITLE = 'use_case_title'

    @classmethod
    def add_to_parser(cls, parser):
        subparser = parser.add_parser(cls.NAME, help=cls.HELP)
        subparser.add_argument('--{}'.format(cls.Args.USE_CASE_ID), help='the Use Case id')
        subparser.add_argument('--{}'.format(cls.Args.USE_CASE_TITLE), help='the Use Case title')

    def run(self, args):
        config = self.init_config(args)

        scaffolder = Scaffolder(config.path.parent)
        scaffolder.create_file('README.md')
        scaffolder.create_file('manifest.json')

    def init_config(self, args):
        config = UseCaseConfig(Path.cwd())
        new_data = {}

        curr_id = config.id
        use_case_id = getattr(args, self.Args.USE_CASE_ID)

        if use_case_id and not valid_id(use_case_id):
            logging.error(INVALID_ID)

            new_data[UseCaseConfig.attr_id] = self.request_use_case_id()

        elif not curr_id:
            new_data[UseCaseConfig.attr_id] = self.request_use_case_id()

        curr_title = config.title
        use_case_title = getattr(args, self.Args.USE_CASE_ID)

        if not use_case_title and not curr_title:
            new_data[UseCaseConfig.attr_title] = request_input('Use case title')

        if not new_data:
            return config

        if config.exists():
            logging.info('Updating {}'.format(config.path))
        else:
            logging.info('Creating {}'.format(config.path))

        config.update(new_data)
        config.write()

        return config

    def request_use_case_id(self):
        while True:
            use_case_id = input('Use case id: ')

            if not valid_id(use_case_id):
                logging.error(INVALID_ID)
                continue

            if use_case_id:
                break

        return use_case_id
