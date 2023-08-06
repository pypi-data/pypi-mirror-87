# coding: utf-8
"""
CLI commands.
"""
import json
import logging
from time import sleep

import click
import yaml

from .create import create
from .delete import delete
from .mode import mode
from .read import read
from .update import update
from .util import (default_open_at, default_close_at, execute, load_config,
                   AliasedGroup, StrLength)

_logger = logging.getLogger(__name__)


@click.group(cls=AliasedGroup, help='OptHub CLI client.')
@click.option('-u', '--url', envvar='OPTHUB_URL',
              type=str, default='https://opthub-api.herokuapp.com/v1/graphql',
              help='OptHub URL.')
@click.option('-m', '--mode', envvar='OPTHUB_MODE',
              type=click.Choice(['guest', 'owner', 'player'],
                                case_sensitive=False),
              default='guest', help='Operation mode.')
@click.option('--verify/--no-verify', envvar='OPTHUB_VERIFY',
              default=True, help='Verity SSL certificate.')
@click.option('-r', '--retries', envvar='OPTHUB_RETRIES',
              type=click.IntRange(min=0), default=0,
              help='Retries for HTTPS connection.')
@click.option('-q', '--quiet', count=True, help='Be quieter.')
@click.option('-v', '--verbose', count=True, help='Be more verbose.')
@click.option('-c', '--config', envvar='OPTHUB_CONFIG', is_eager=True,
              type=click.Path(dir_okay=False), default='~/.opt.yml',
              callback=load_config, help='Configuration file.')
@click.option('-a', '--auth-url', envvar='OPTHUB_AUTH_URL',
              type=str, default='https://opthub.us.auth0.com',
              help='Authentication URL.')
@click.option('-i', '--auth-client-id', envvar='OPTHUB_AUTH_CLIENT_ID',
              type=str, default='E3JSaUuGCopA8To7e8SttdOv28l3x3Mf',
              help='Authentication client ID.')
@click.option('--access-token', envvar='OPTHUB_ACCESS_TOKEN',
              type=str,
              help='OptHub access token.')
@click.option('--refresh-token', envvar='OPTHUB_REFRESH_TOKEN',
              type=str,
              help='OptHub refresh token.')
@click.option('--id-token', envvar='OPTHUB_ID_TOKEN',
              type=str,
              help='OptHub ID token.')
@click.version_option()
@click.pass_context
def opt(ctx, **kwargs):
    """The entrypoint of CLI.

    :param ctx: Click context
    :param kwargs: Click options
    """
    verbosity = 10 * (kwargs['quiet'] - kwargs['verbose'])
    log_level = logging.WARNING + verbosity
    logging.basicConfig(level=log_level)
    _logger.info('Log level is set to %d.', log_level)
    _logger.debug('opt(%s)', kwargs)
    ctx.obj = kwargs


opt.add_command(create)
opt.add_command(read)
opt.add_command(update)
opt.add_command(delete)
opt.add_command(mode)


@opt.command(help='Show status.')
@click.pass_context
def status(ctx):
    """Show status.

    Guest mode: show the summary of OptHub status.
    Owner mode: show the status of the current user.
    Player mode: show the status of the current player.

    :param ctx: Click context
    """
    _logger.debug('status()')
    execute(
        ctx,
        '''
        query summary {
          users_aggregate {aggregate {count}}
          problems_aggregate {aggregate {count}}
          indicators_aggregate {aggregate {count}}
          competitions_aggregate {aggregate {count}}
          matches_aggregate {aggregate {count}}
          environments_aggregate {aggregate {count}}
          solutions_aggregate {aggregate {count}}
        }
        ''')


@opt.command(help='Submit a solution.')
@click.option('-m', '--match', envvar='OPTHUB_SUBMIT_MATCH',
              type=click.IntRange(min=1), required=True,
              help='Match ID.')
@click.option('--wait/--no-wait', envvar='OPTHUB_SUBMIT_WAIT',
              default=True,
              help='Wait for evaluation.')
@click.option('-i', '--interval', envvar='OPTHUB_SUBMIT_INTERVAL',
              type=click.IntRange(min=1), default=2,
              help='Polling interval to wait.')
@click.option('-x', '--solution', envvar='OPTHUB_SUBMIT_SOLUTION',
              type=click.File(), default='-',
              help='File storing a solution.')
@click.pass_context
def submit(ctx, **kwargs):
    """Submit a solution to evaluate.

    :param ctx: Click context
    :param kwargs: Click options
    """
    _logger.debug('submit(%s)', kwargs)
    variable = yaml.safe_load(kwargs['solution'].read())
    _logger.debug('variable=%s', variable)
    _logger.info('Submitting a solution...')
    response = execute(
        ctx,
        '''
        mutation(
          $match: Int!
          $variable: jsonb!
        ) {
          insert_solutions_one(
            object: {
              match_id: $match
              variable: $variable
            }
          ) {
            id
            created_at
          }
        }
        ''', {'match': kwargs['match'], 'variable': variable}, kwargs['wait'])
    _logger.info('...Submitted.')
    _logger.debug('response=%s', response)
    if not kwargs['wait']:
        _logger.info('Exit without wait.')
        return

    _logger.info('Waiting evaluation and scoring...')
    solution = response['insert_solutions_one']
    while True:  # Wait for evaluation and scoring
        _logger.info('Sleep %s seconds...', kwargs['interval'])
        sleep(kwargs['interval'])
        _logger.info('...Slept.')
        _logger.info('Polling the result...')
        response = execute(
            ctx,
            '''
            query($id: Int!) {
              solutions_by_pk(id: $id) {
                id
                objective
                constraint
                score
                evaluation_error
                scoring_error
              }
            }
            ''', {'id': solution['id']}, kwargs['wait'])
        _logger.info('...Polled.')
        _logger.debug('response=%s', response)
        solution = response['solutions_by_pk']
        if (solution['evaluation_error'] is not None
            or solution['scoring_error'] is not None
            or solution['score'] is not None):
            _logger.info('...Waited.')
            break

    click.echo(json.dumps(solution))


@opt.command(help='Create a new competition on OptHub.')
@click.option('-i', '--id', type=StrLength(2, 32), required=True,
              prompt=True, help='Identifier.')
@click.option('--public/--private',
              default=False, prompt=True,
              help='Visibility.')
@click.option('-o', '--open-at', type=click.DateTime(), required=True,
              prompt=True, default=default_open_at, help='Open date.')
@click.option('-c', '--close-at', type=click.DateTime(), required=True,
              prompt=True, default=default_close_at, help='Close date.')
@click.option('-e', '--description_en', type=str, required=True,
              prompt=True, help='Description in English.')
@click.option('-j', '--description_ja', type=str, required=True,
              prompt=True, help='Description in Japanese.')
@click.pass_context
def organize(ctx, **kwargs):
    """Create a new competition on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug('organize(%s)', kwargs)
    click.confirm(
        'Do you create a competition with the following values?\n%s' % kwargs,
        abort=True
    )
    response = execute(
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
            public
            description_en
            description_ja
            owner { name }
            open_at
            close_at
            created_at
          }
        }
        ''', kwargs)

    var = {'competition_id': response['insert_competitions_one']['id']}
    while click.confirm('Do you add a match to this competition?'):
        var['name'] = click.prompt('name', type=str)
        var['problem_id'] = click.prompt('Problem ID', type=str)
        var['indicator_id'] = click.prompt('Indicator ID', type=str)
        var['budget'] = click.prompt('Budget', type=int)
        execute(
            ctx,
            '''
            mutation(
              $name: String!
              $competition_id: String!
              $problem_id: String!
              $indicator_id: String!
              $budget: String!
            ) {
              insert_matches_one(
                object: {
                  name: $name
                  competition_id: $competition_id
                  problem_id: $problem_id
                  indicator_id: $indicator_id
                  budget: $budget
                }
              ) {
                id
                created_at
              }
            }
            ''', var)


if __name__ == '__main__':
    opt()  # pylint: disable=no-value-for-parameter
