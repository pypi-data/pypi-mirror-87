# coding: utf-8
"""
Utilities.
"""
from datetime import datetime, timedelta
import json
import logging
import os
from time import sleep

from click import Group, echo, style
from click.types import StringParamType
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import requests
import yaml

_logger = logging.getLogger(__name__)

# Default dates for creating a competition
default_open_at = datetime.utcnow()
default_close_at = default_open_at + timedelta(days=1)
default_open_at = default_open_at.strftime('%Y-%m-%dT%H:%M:%S')
default_close_at = default_close_at.strftime('%Y-%m-%dT%H:%M:%S')


class AliasedGroup(Group):
    """A Click group with short subcommands.

    Example
    -------
    >>> @click.group(cls=AliasedGroup)
    >>> def long_name_command():
    ...     print('This command can be called with `l`!')
    """
    def get_command(self, ctx, cmd_name):
        ret = Group.get_command(self, ctx, cmd_name)
        if ret is not None:
            return ret
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if len(matches) > 1:
            ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))
        if not matches:
            return None
        return Group.get_command(self, ctx, matches[0])


class StrLength(StringParamType):
    """A Click option type of string with length validation.

    This is basically the same as `str`, except for additional
    functionalities of length validation.

    :param min: Minimum length
    :param max: Maximum length
    :param clamp: Clamp the input if exeeded
    """
    def __init__(self, min=None, max=None, clamp=False):  # pylint: disable=redefined-builtin
        self.min = min
        self.max = max
        self.clamp = clamp

    def convert(self, value, param, ctx):
        ret = StringParamType.convert(self, value, param, ctx)
        length = len(ret)
        if self.clamp:
            if self.min is not None and length < self.min:
                return ret + ' ' * (self.min - length)
            if self.max is not None and length > self.max:
                return ret[:self.max]
        if self.min is not None and length < self.min or \
           self.max is not None and length > self.max:
            if self.min is None:
                self.fail(
                    'Length %d is longer than the maximum valid length %d.'
                    % (length, self.max), param, ctx)
            elif self.max is None:
                self.fail(
                    'Length %d is shorter than the minimum valid length %d.'
                    % (length, self.min), param, ctx)
            else:
                self.fail(
                    'Length %d is not in the valid range of %d to %d.'
                    % (length, self.min, self.max), param, ctx)
        return ret

    def __repr__(self):
        return 'StrLength(%d, %d)' % (self.min, self.max)


def root(ctx):
    """Retrieve the root context.

    :param ctx: Click context
    :return ctx: Click root context
    """
    while ctx.parent:
        ctx = ctx.parent
    return ctx


def touch(path, mode=0o666, exist_ok=True):
    """Emulate pathlib.Path.touch(mode, exist_ok), which is available in Python 3.4+.

    This function behaves as follows:
    When the path does not exist, create an empty file with a given mode.
    When the path exists and exist_ok is True, update the timestamp without any change of its mode and contents.
    When the path exists and exist_ok is False, raise a FileExistsError.

    :param path: Path to a file
    :param mode: Permission triplet
    :param exist_ok: Do not raise errors when the path exists
    """
    if not os.path.exists(path):
        # Create an empty file with a given mode
        with open(path, "a"):
            os.chmod(path, mode)
    else:
        if not exist_ok:
            raise FileExistsError("[Errno 17] File exists: '%s'" % path)
        # Change the timestamp without overwriting the mode and contents
        with open(path, "a"):
            pass


def load_config(ctx, param, value):  # pylint: disable=unused-argument
    """Load `ctx.default_map` from a file.

    :param ctx: Click context
    :param param: Parameter name
    :param value: File name
    :return dict: Loaded config
    """
    rctx = root(ctx)
    config_path = os.path.expanduser(value)
    if not os.path.exists(config_path):
        rctx.default_map = {}
    else:
        with open(config_path) as cfg:
            rctx.default_map = yaml.safe_load(cfg)
    return value


def save_config(ctx, param, value):  # pylint: disable=unused-argument
    """Save `ctx.default_map` to a file.

    :param ctx: Click context
    :param param: Parameter name
    :param value: File name
    :return dict: Saved config
    """
    rctx = root(ctx)
    config_path = os.path.expanduser(value)
    touch(config_path, mode=0o600)
    with open(config_path, 'w') as cfg:
        yaml.dump(rctx.default_map, cfg)
    return rctx.default_map


def execute(ctx, document, variable_values=None, quiet=False):
    """Execute a GraphQL document and print results.

    :param ctx: Click context
    :param document: GraphQL document
    :param variable_values: variables
    :return dict: GraphQL response
    """
    transport = RequestsHTTPTransport(
        url=ctx.obj['url'],
        verify=ctx.obj['verify'],
        retries=ctx.obj['retries'],
        headers={'Authorization': 'Bearer ' + ctx.obj['access_token']} if ctx.obj['access_token'] else None,
    )
    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )
    try:
        results = client.execute(
            gql(document), variable_values=variable_values)
    except Exception as exc:  # pylint: disable=broad-except
        # Since gql simply raises an Exception no matter what GraphQL error happens,
        # the true cause should be extracted from error messages in a stringified dict.
        # The message is like:
        # ("{'extensions': {'path': '$', 'code': 'invalid-jwt'}, 'message': 'Could not verify JWT: JWTExpired'}",)
        # ("{'extensions': {'path': '$', 'code': 'validation-failed'}, 'message': 'no mutations exist'}",)
        if exc.args and (
            'Could not verify JWT: JWTExpired' in exc.args[0]
            or ('no mutations exist' in exc.args[0] and not ctx.obj['access_token'])):
            # The access token has been expired; refresh it.
            res = get_token(ctx)
            ctx.obj['access_token'] = res['access_token']
            ctx.obj['id_token'] = res['id_token']
            ctx.obj['refresh_token'] = res['refresh_token']
            root(ctx).default_map.update(res)
            save_config(ctx, None, ctx.obj['config'])

            # Try again with a new access token.
            transport.headers = {'Authorization': 'Bearer ' + ctx.obj['access_token']}
            results = client.execute(
                gql(document), variable_values=variable_values)
        else:
            # Other errors are unrecoverable; abort.
            ctx.fail('%s when executing %s\n' % (exc, document))
    if not quiet:
        echo(json.dumps(results))
    return results


def authorize_device(url, client_id, scope, audience):
    """Get new tokens via the device authorization flow.

    See https://auth0.com/docs/flows/device-authorization-flow

    :param url: Authentication URL
    :param client_id: Client ID of this CLI tool
    :param scope: Space-delimited list of requested scope permissions
    :param audience: OptHub URL
    :return dict: Authentication response
    """
    device_code_url = url + '/oauth/device/code'
    token_url = url + '/oauth/token'
    userinfo_url = url + '/userinfo'

    payload = {'client_id': client_id, 'scope': scope, 'audience': audience}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url=device_code_url, data=payload, headers=headers)
    res = yaml.safe_load(response.text)

    echo('=' * 70)
    echo('To activate Opt with your account:')
    echo()
    echo('  1. On your browser, go to: ' + style(res['verification_uri'], fg='cyan', underline=True))
    echo('  2. Enter the following code: ' + style(res['user_code'], bold=True))
    echo('  3. Sign up or sign in (if not yet).')
    echo()
    echo('The code expires in %d minutes.' % (res['expires_in'] / 60))
    echo('=' * 70)
    echo()
    echo('Opt is waiting for your activation...')

    device_code = res['device_code']
    interval = res['interval']
    payload = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code,
        'client_id': client_id,
    }

    while True:
        sleep(interval)
        response = requests.post(url=token_url, data=payload, headers=headers)
        res = yaml.safe_load(response.text)
        if response.status_code == requests.codes.ok:  # pylint: disable=no-member
            break
        if res['error'] == 'slow_down':
            interval += 1
        elif res['error'] != 'authorization_pending':
            raise Exception(res['error_description'])

    response = requests.get(
        url=userinfo_url,
        headers={'Authorization': 'Bearer ' + res['access_token']})
    userinfo = yaml.safe_load(response.text)
    echo('Opt is activated with your account: %s' % userinfo['nickname'])
    echo()
    return res


def refresh_token(url, client_id, refresh_token, scope=None):
    """Refresh the access token and id token.

    See https://auth0.com/docs/tokens/refresh-tokens/use-refresh-tokens

    :param url: Authentication URL
    :param client_id: Client ID of this CLI tool
    :param refresh_token: Refresh token to use
    :param scope: Space-delimited list of requested scope permissions
    :return dict: Refresh response
    """
    token_url = url + '/oauth/token'
    payload = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'refresh_token': refresh_token,
    }
    if scope:
        payload['scope'] = scope
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url=token_url, data=payload, headers=headers)
    res = yaml.safe_load(response.text)
    return res


def get_token(ctx):
    """Get new tokens.

    When a refresh token exists and is not expired, refresh tokens.
    When a refresh token does not exists or is expired, get tokens via the device authorization flow.

    :param ctx: Click context
    :return dict: Authentication response
    """
    res = None
    if ctx.obj['refresh_token']:
        res = refresh_token(
            url=ctx.obj['auth_url'],
            client_id=ctx.obj['auth_client_id'],
            refresh_token=ctx.obj['refresh_token'])

    if not res or 'access_token' not in res:  # If refreshing token failed
        res = authorize_device(
            url=ctx.obj['auth_url'],
            client_id=ctx.obj['auth_client_id'],
            scope='openid profile email offline_access',
            audience=ctx.obj['url'])
    return res


def str_to_dict(ctx, param, value):  # pylint: disable=unused-argument
    """Convert a YAML string to a dict.

    :param ctx: Click context
    :param param: Parameter info
    :param value: YAML string
    :return dict: Python dict
    """
    if not value:
        return None
    try:
        dic = yaml.safe_load(value)
        if not isinstance(dic, dict):
            raise Exception('expected `dict` but %s' % type(dic))
    except Exception as exc:  # pylint: disable=broad-except
        ctx.fail('%s when converting `%s`\n' % (exc, value))
    return dic
