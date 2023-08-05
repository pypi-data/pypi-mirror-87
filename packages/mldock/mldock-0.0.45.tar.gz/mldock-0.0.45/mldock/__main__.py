# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import os
import sys
import logging
import click

# add serum package to path
sys.path.insert(1, ".")

from mldock.__init__ import MLDOCK_LOGO
from mldock.command.initialize import init
from mldock.command.local import local
from mldock.command.push import push
from mldock.log import configure_logger

click.disable_unicode_literals_warning = True

@click.group()
@click.option(u"-v", u"--verbose", count=True, help=u"Turn on debug logging")
@click.option(u"-t", u"--docker-tag", default=u"latest", help=u"Specify tag for Docker image")
@click.pass_context
def cli(ctx, verbose, docker_tag):
    """
    CLI tool built to add simple functionality to sagify development.
    """
    _FILE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    logger=configure_logger('mldock', verbose=verbose)
    logger.info(MLDOCK_LOGO)
    ctx.obj = {'verbose': verbose, 'docker_tag': docker_tag, 'helper_library_path':_FILE_DIR_PATH}

def add_commands(cli):
    cli.add_command(init)
    cli.add_command(local)
    cli.add_command(push)

add_commands(cli)

if __name__ == '__main__':
    cli()
