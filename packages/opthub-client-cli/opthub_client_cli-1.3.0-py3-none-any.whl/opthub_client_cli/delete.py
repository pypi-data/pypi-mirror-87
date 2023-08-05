# coding: utf-8
"""
Low-level delete commands.
"""
import logging

import click

from .util import AliasedGroup, StrLength, execute

_logger = logging.getLogger(__name__)


@click.group(cls=AliasedGroup)
def delete():
    """Delete an object."""


@delete.command(help='Delete a problem.')
@click.argument('id', type=StrLength(min=2))
@click.pass_context
def problem(ctx, **kwargs):
    """Delete a problem.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('delete.problem(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation delete_problem($id: String!) {
          delete_problems_by_pk(id: $id) {
            id
            image
            public
            description_en
            description_ja
            owner { name }
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@delete.command(help='Delete an indicator.')
@click.argument('id', type=StrLength(min=2))
@click.pass_context
def indicator(ctx, **kwargs):
    """Delete an indicator.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('delete.indicator(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation($id: String!) {
          delete_indicators_by_pk(id: $id) {
            id
            image
            public
            description_en
            description_ja
            owner { name }
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@delete.command(help='Delete an environment.')
@click.argument('id', type=int)
@click.pass_context
def environment(ctx, **kwargs):
    """Delete an environment.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('delete.environment(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation($id: Int!) {
          delete_environments_by_pk(id: $id) {
            id
            match_id
            public
            key
            value
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@delete.command(help='Delete a match.')
@click.argument('id', type=int)
@click.pass_context
def match(ctx, **kwargs):
    """Delete a match.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('delete.match(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation($id: Int!) {
          delete_matches_by_pk(id: $id) {
            id
            name
            competition_id
            problem_id
            indicator_id
            budget
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@delete.command(help='Delete a competition.')
@click.argument('id', type=StrLength(min=2))
@click.pass_context
def competition(ctx, **kwargs):
    """Delete a competition.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('delete.competition(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation($id: String!) {
          delete_competitions_by_pk(id: $id) {
            id
            public
            description_en
            description_ja
            owner { name }
            open_at
            close_at
            created_at
            updated_at
          }
        }
        ''',
        kwargs)
