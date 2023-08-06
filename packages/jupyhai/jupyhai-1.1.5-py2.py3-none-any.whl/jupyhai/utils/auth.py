import os

from valohai_cli.api import APISession
from valohai_cli.settings import settings

from jupyhai.api_urls import ME_URL
from jupyhai.consts import HOST


def logout():
    settings.persistence.update(host=None, user=None, token=None)
    settings.persistence.save()


def login_status():
    return (
        settings.persistence.get('user') is not None
        and settings.persistence.get('token') is not None
    )


def get_current_username():
    if login_status():
        return settings.persistence.get('user')['username']
    return ""


def get_user_data(token, host):
    with APISession(host, token) as sess:
        return sess.get(ME_URL, timeout=10).json()


def verify_and_save_token(token, host):
    user_data = get_user_data(token, host)
    settings.persistence.update(host=host, user=user_data, token=token)
    settings.persistence.save()
    return user_data


def do_environment_login(log):
    try:
        token = os.environ['VALOHAI_TOKEN']
        user_data = verify_and_save_token(token, HOST)
        settings.persistence.update(
            host=HOST, user=user_data, token=token,
        )
        settings.persistence.save()
        log.info('Jupyhai: Token login => %s' % user_data['username'])
    except Exception:
        log.error('Jupyhai: Token login failed!', exc_info=True)


def login_with_credentials(username, password, host):
    logout()
    with APISession(host) as sess:
        response = sess.post(
            '/api/v0/get-token/',
            data={'username': username, 'password': password},
            timeout=10,
        )
        response.raise_for_status()
        token = response.json()['token']
    return verify_and_save_token(token, host)
