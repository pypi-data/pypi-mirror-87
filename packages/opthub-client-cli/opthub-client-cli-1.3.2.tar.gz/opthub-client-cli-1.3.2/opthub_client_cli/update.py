# coding: utf-8
"""
Low-level update commands.
"""
import logging

import click
import yaml

from .util import AliasedGroup, StrLength, execute

_logger = logging.getLogger(__name__)


@click.group(cls=AliasedGroup, help='Update an object.')
def update():
    """Update an object."""


@update.command(help='Update a problem.')
@click.argument('id-to-update', type=StrLength(min=2))
@click.option('-i', '--id',
              type=StrLength(min=2),
              help='New ID.')
@click.option('-t', '--image',
              type=StrLength(min=1),
              help='New Docker image tag.')
@click.option('--public/--private',
              help='New visibility.')
@click.option('-e', '--description_en',
              type=StrLength(min=1),
              help='New description in English.')
@click.option('-j', '--description_ja',
              type=StrLength(min=1),
              help='New description in Japanese.')
@click.pass_context
def problem(ctx, **kwargs):
    """Update a problem.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('update.problem(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id_to_update: String!
          $id: String!
          $image: String!
          $public: Boolean!
          $description_en: String!
          $description_ja: String!
        ) {
          update_problems_by_pk(
            pk_columns: { id: $id_to_update }
            _set: {
              id: $id
              image: $image
              public: $public
              description_en: $description_en
              description_ja: $description_ja
            }
          ) {
            id
            updated_at
          }
        }
        ''',
        kwargs)


@update.command(help='Update an indicator.')
@click.argument('id-to-update', type=StrLength(min=2))
@click.option('-i', '--id',
              type=StrLength(min=2),
              help='New ID.')
@click.option('-t', '--image',
              type=StrLength(min=1),
              help='New Docker image tag.')
@click.option('--public/--private',
              help='New visibility.')
@click.option('-e', '--description_en',
              type=StrLength(min=1),
              help='New description in English.')
@click.option('-j', '--description_ja',
              type=StrLength(min=1),
              help='New description in Japanese.')
@click.pass_context
def indicator(ctx, **kwargs):
    """Update an indicator.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('update.indicator(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id_to_update: String!
          $id: String!
          $image: String!
          $public: Boolean!
          $description_en: String!
          $description_ja: String!
        ) {
          update_indicators_by_pk(
            pk_columns: { id: $id_to_update }
            _set: {
              id: $id
              image: $image
              public: $public
              description_en: $description_en
              description_ja: $description_ja
            }
          ) {
            id
            updated_at
          }
        }
        ''',
        kwargs)


@update.command(help='Update an environment.')
@click.argument('id-to-update', type=int)
@click.option('-m', '--match',
              type=click.IntRange(min=1),
              help='New match ID.')
@click.option('-k', '--key',
              type=StrLength(min=1),
              help='New key.')
@click.option('-v', '--value',
              type=yaml.safe_load,
              help='New value.')
@click.option('--public/--private',
              default=False,
              help='New visibility.')
@click.pass_context
def environment(ctx, **kwargs):
    """Update an environment.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('update.environment(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id_to_update: Int!
          $match: Int
          $public: Boolean
          $key: String
          $value: jsonb
        ) {
          update_environments_by_pk(
            pk_columns: { id: $id_to_update }
            _set: {
              match_id: $match
              public: $public
              key: $key
              value: $value
            }
          ) {
            id
            updated_at
          }
        }
        ''',
        kwargs)


@update.command(help='Update a match.')
@click.argument('id-to-update', type=int)
@click.option('-n', '--name',
              type=StrLength(min=2),
              help='New name.')
@click.option('-c', '--competition',
              type=StrLength(min=2),
              help='New competition ID.')
@click.option('-p', '--problem',
              type=StrLength(min=2),
              help='New problem ID.')
@click.option('-i', '--indicator',
              type=StrLength(min=2),
              help='New indicator ID.')
@click.option('-b', '--budget',
              type=click.IntRange(min=1),
              help='New budget.')
@click.pass_context
def match(ctx, **kwargs):
    """Update a match.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('update.match(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id_to_update: Int!
          $name: String!
          $competition: String!
          $problem: String!
          $indicator: String!
          $budget: Int!
        ) {
          update_matches_by_pk(
            pk_columns: { id: $id_to_update }
            _set: {
              name: $name
              competition_id: $competition
              problem_id: $problem
              indicator_id: $indicator
              budget: $budget
            }
          ) {
            id
            updated_at
          }
        }
        ''',
        kwargs)


@update.command(help='Update a competition.')
@click.argument('id-to-update', type=StrLength(min=2))
@click.option('-i', '--id',
              type=StrLength(min=2),
              help='New ID.')
@click.option('--public/--private',
              help='New visibility.')
@click.option('-o', '--open-at',
              type=click.DateTime(),
              help='New open date.')
@click.option('-c', '--close-at',
              type=click.DateTime(),
              help='New close date.')
@click.option('-e', '--description_en',
              type=StrLength(min=1),
              help='New description in English.')
@click.option('-j', '--description_ja',
              type=StrLength(min=1),
              help='New description in Japanese.')
@click.pass_context
def competition(ctx, **kwargs):
    """Update a competition.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('update.competition(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id_to_update: String!
          $id: String!
          $public: Boolean!
          $description_en: String!
          $description_ja: String!
          $open_at: String!
          $close_at: String!
        ) {
          update_competitions_by_pk(
            pk_columns: { id: $id_to_update }
            _set: {
              id: $id
              public: $public
              description_en: $description_en
              description_ja: $description_ja
              open_at: $open_at
              close_at: $close_at
            }
          ) {
            id
            updated_at
          }
        }
        ''',
        kwargs)
