# coding: utf-8
"""
Low-level create commands.
"""
import logging

import click
import yaml

from .util import AliasedGroup, StrLength, execute, str_to_dict

_logger = logging.getLogger(__name__)


@click.group(cls=AliasedGroup, help='Create an object.')
def create():
    """Create an object."""


@create.command(help='Create a problem.')
@click.option('-i', '--id',
              type=StrLength(min=2), required=True, prompt=True,
              help='ID.')
@click.option('-t', '--image',
              type=StrLength(min=1), required=True, prompt=True,
              help='Docker image tag.')
@click.option('--public/--private',
              default=False, prompt=True,
              help='Visibility.')
@click.option('-e', '--description_en',
              type=StrLength(min=1), prompt=True,
              help='Description in English.')
@click.option('-j', '--description_ja',
              type=StrLength(min=1), prompt=True,
              help='Description in Japanese.')
@click.pass_context
def problem(ctx, **kwargs):
    """Create a problem.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('create.problem(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id: String!
          $image: String!
          $public: Boolean!
          $description_en: String!
          $description_ja: String!
        ) {
          insert_problems_one(
            object: {
              id: $id
              image: $image
              public: $public
              description_en: $description_en
              description_ja: $description_ja
            }
          ) {
            id
            created_at
          }
        }
        ''',
        kwargs)


@create.command(help='Create an indicator.')
@click.option('-i', '--id',
              type=StrLength(min=2), required=True, prompt=True,
              help='ID.')
@click.option('-t', '--image',
              type=StrLength(min=1), required=True, prompt=True,
              help='Docker image tag.')
@click.option('--public/--private',
              default=False, prompt=True,
              help='Visibility.')
@click.option('-e', '--description_en',
              type=StrLength(min=1), prompt=True,
              help='Description in English.')
@click.option('-j', '--description_ja',
              type=StrLength(min=1), prompt=True,
              help='Description in Japanese.')
@click.pass_context
def indicator(ctx, **kwargs):
    """Create an indicator.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('create.indicator(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id: String!
          $image: String!
          $public: Boolean!
          $description_en: String!
          $description_ja: String!
        ) {
          insert_indicators_one(
            object: {
              id: $id
              image: $image
              public: $public
              description_en: $description_en
              description_ja: $description_ja
            }
          ) {
            id
            created_at
          }
        }
        ''',
        kwargs)


@create.command(help='Create an environment.')
@click.option('-m', '--match',
              type=click.IntRange(min=1), required=True, prompt=True,
              help='Match ID.')
@click.option('-k', '--key',
              type=StrLength(min=1), required=True, prompt=True,
              help='Key.')
@click.option('-v', '--value',
              type=yaml.safe_load, required=True, prompt=True,
              help='Value.')
@click.option('--public/--private',
              default=False, prompt=True,
              help='Visibility.')
@click.pass_context
def environment(ctx, **kwargs):
    """Create an environment.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('create.environment(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $match: Int!
          $public: Boolean!
          $key: String!
          $value: jsonb!
        ) {
          insert_environments_one(
            object: {
              match_id: $match
              public: $public
              key: $key
              value: $value
            }
          ) {
            id
            created_at
          }
        }
        ''',
        kwargs)


@create.command(help='Create a match.')
@click.option('-n', '--name',
              type=StrLength(min=2), required=True, prompt=True,
              help='Name.')
@click.option('-c', '--competition',
              type=StrLength(min=2), required=True, prompt=True,
              help='Competition ID.')
@click.option('-p', '--problem',
              type=StrLength(min=2), required=True, prompt=True,
              help='Problem ID.')
@click.option('-i', '--indicator',
              type=StrLength(min=2), required=True, prompt=True,
              help='Indicator ID.')
@click.option('-b', '--budget',
              type=click.IntRange(min=1), required=True, prompt=True,
              help='Budget.')
@click.pass_context
def match(ctx, **kwargs):
    """Create a match.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('create.match(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $name: String!
          $competition: String!
          $problem: String!
          $indicator: Int!
          $budget: Int!
        ) {
          insert_matches_one(
            object: {
              name: $name
              competition_id: $competition
              problem_id: $problem
              indicator_id: $indicator
              budget: $budget
            }
          ) {
            id
            created_at
          }
        }
        ''',
        kwargs)


@create.command(help='Create a competition.')
@click.option('-i', '--id', type=StrLength(min=2), required=True,
              prompt=True, help='ID.')
@click.option('--public/--private',
              default=False, prompt=True,
              help='Visibility.')
@click.option('-o', '--open-at', type=click.DateTime(), required=True,
              prompt=True, help='Open date.')
@click.option('-c', '--close-at', type=click.DateTime(), required=True,
              prompt=True, help='Close date.')
@click.option('-e', '--description_en', type=StrLength(min=1), required=True,
              prompt=True, help='Description in English.')
@click.option('-j', '--description_ja', type=StrLength(min=1), required=True,
              prompt=True, help='Description in Japanese.')
@click.pass_context
def competition(ctx, **kwargs):
    """Create a competition.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('create.competition(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id: String!
          $public: Boolean!
          $description_en: String!
          $description_ja: String!
          $open_at: String!
          $close_at: String!
        ) {
          insert_competitions_one(
            object: {
              id: $id
              public: $public
              description_en: $description_en
              description_ja: $description_ja
              open_at: $open_at
              close_at: $close_at
            }
          ) {
            id
            created_at
          }
        }
        ''',
        kwargs)
