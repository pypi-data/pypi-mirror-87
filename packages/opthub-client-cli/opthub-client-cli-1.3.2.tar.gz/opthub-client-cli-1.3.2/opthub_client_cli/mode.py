# coding: utf-8
"""
Mode commands.
"""
import logging

import click

from .util import AliasedGroup, StrLength, save_config

_logger = logging.getLogger(__name__)


@click.group(cls=AliasedGroup)
def mode():
    """Change the current CLI mode."""


@mode.command(help='Change to guest mode.')
@click.pass_context
def guest(ctx):
    """Change to guest mode."""
    _logger.debug('guest()')
    ctx.parent.parent.default_map['mode'] = 'guest'
    save_config(ctx.parent.parent, ctx.obj['config_file'])


@mode.command(help='Change to owner mode.')
@click.pass_context
def owner(ctx):
    """Change to owner mode."""
    _logger.debug('owner()')
    ctx.parent.parent.default_map['mode'] = 'owner'
    save_config(ctx.parent.parent, ctx.obj['config_file'])


@mode.command(help='Change to player.')
@click.option('-c', '--competition', type=StrLength(2, 32), required=True,
              prompt=True, help='Competition ID.')
@click.option('-m', '--match', type=click.IntRange(min=1),
              default=1, help='Match ID.')
@click.pass_context
def player(ctx, **kwargs):
    """Change to player mode.

    :param ctx: Click context.
    :param kwargs: Click options.
    """
    _logger.debug('player(%s)', kwargs)

    # TODO: Check IDs here

    ctx.parent.parent.default_map['mode'] = 'player'
    ctx.parent.parent.default_map['competition'] = kwargs['competition']
    ctx.parent.parent.default_map['match'] = kwargs['match']
    save_config(ctx.parent.parent, ctx.obj['config_file'])
