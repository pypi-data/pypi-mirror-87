# coding: utf-8
"""
Low-level read commands.
"""
import logging

import click

from .util import AliasedGroup, execute, str_to_dict

_logger = logging.getLogger(__name__)


@click.group(cls=AliasedGroup, name='list')
def read():
    """List objects."""


@read.command(help='List users on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 1000),
              default=50, help='Limit.')
@click.pass_context
def users(ctx, **kwargs):
    """List users on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('list.users(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: users_bool_exp = {}
        ) {
          users(limit: $limit, offset: $offset, where: $query) {
            name
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@read.command(help='List problems on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 1000),
              default=50, help='Limit.')
@click.pass_context
def problems(ctx, **kwargs):
    """List problems on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('list.problems(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: problems_bool_exp = {}
        ) {
          problems(limit: $limit, offset: $offset, where: $query) {
            id
            owner { name }
            image
            public
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@read.command(help='List indicators on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 1000),
              default=50, help='Limit.')
@click.pass_context
def indicators(ctx, **kwargs):
    """List indicators on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('list.indicators(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: indicators_bool_exp = {}
        ) {
          indicators(offset: $offset, limit: $limit, where: $query) {
            id
            owner { name }
            image
            public
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@read.command(help='List competitions on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 1000),
              default=50, help='Limit.')
@click.pass_context
def competitions(ctx, **kwargs):
    """List competitions on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('list.competitions(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: competitions_bool_exp = {}
        ) {
          competitions(offset: $offset, limit: $limit, where: $query) {
            id
            owner { name }
            matches { id }
            public
            open_at
            close_at
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@read.command(help='List progress on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 1000),
              default=50, help='Limit.')
@click.pass_context
def progress(ctx, **kwargs):
    """List progress on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('list.progress(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: progress_bool_exp = {}
        ) {
          progress(offset: $offset, limit: $limit, where: $query) {
            user_id
            match_id
            budget
            submitted
            evaluating
            evaluated
            scoring
            scored
            scores
            created_at
            updated_at
            evaluation_started_at
            evaluation_finished_at
            scoring_started_at
            scoring_finished_at
          }
        }
        ''',
        kwargs)


@read.command(help='List environments on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 1000),
              default=50, help='Limit.')
@click.pass_context
def environments(ctx, **kwargs):
    """List environments on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('list.environments(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: environments_bool_exp = {}
        ) {
          environments(limit: $limit, offset: $offset, where: $query) {
            id
            key
            value
            public
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@read.command(help='List matches on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 1000),
              default=50, help='Limit.')
@click.pass_context
def matches(ctx, **kwargs):
    """List matches on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('list.matches(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: matches_bool_exp = {}
        ) {
          matches(offset: $offset, limit: $limit, where: $query) {
            id
            name
            competition_id
            problem_id
            indicator_id
            budget
            environments { id }
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@read.command(help='List solutions on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 1000),
              default=50, help='Limit.')
@click.pass_context
def solutions(ctx, **kwargs):
    """List solutions on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('list.solutions(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: solutions_bool_exp = {}
        ) {
          solutions(offset: $offset, limit: $limit, where: $query) {
            id
            owner { name }
            match_id
            variable
            objective
            constraint
            score
            created_at
            updated_at
            evaluation_started_at
            evaluation_finished_at
            scoring_started_at
            scoring_finished_at
          }
        }
        ''',
        kwargs)
