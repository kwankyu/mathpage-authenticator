"""
Django Authenticator
"""
import json
import os
import urllib
import subprocess
import re

from tornado.httputil import url_concat
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

from jupyterhub.auth import Authenticator, LocalAuthenticator

from traitlets import Unicode, Dict

class DjangoAuthenticator(Authenticator):

    auth_url = Unicode(
        os.environ.get('DJANGO_AUTH_URL', ''),
        config=True,
        help='Django authentication url',
    )

    auth_api_access_token = Unicode(
        os.environ.get('DJANGO_AUTH_API_ACCESS_TOKEN', ''),
        config=True,
        help='Django authentication api access token',
    )

    async def authenticate(self, handler, data=None):
        http_client = AsyncHTTPClient()

        params = dict(
            username=data['username'],
            password=data['password'],
        )

        headers = {
            "Accept": "application/json",
            "User-Agent": "JupyterHub",
            "Authorization": "Token " + self.auth_api_access_token,
        }

        print(self.auth_url, headers)

        req = HTTPRequest(self.auth_url,
                          method="POST",
                          headers=headers,
                          body=urllib.parse.urlencode(params),
                          )

        resp = await http_client.fetch(req)
        user_data = json.loads(resp.body.decode('utf8', 'replace'))

        username = user_data['username']
        if not username: # empty string for unauthenticated user
            self.log.error("Invalid user name or password %s", data['username'])
            return

        auth_state = {
            'active_author': False,
            }

        author = user_data['author']
        if author:
            auth_state['active_author'] = author['is_active']

        # convert a Django username to a valid Ubuntu system username
        username = username.replace('@', '_with_')

        return {'name': username, 'auth_state': auth_state}

class LocalDjangoAuthenticator(LocalAuthenticator, DjangoAuthenticator):
    """A version that mixes in local system user creation"""

    async def pre_spawn_start(self, user, spawner):
        auth_state = await user.get_auth_state()

        # for debugging, turn off comment-out and see /var/log/jupyterhub.log
        #
        # self.log.info(auth_state)

        if not auth_state:
            return

        # Disallow new outgoing internet connections by the user
        if not auth_state['active_author']:
            p = subprocess.Popen(['id', user.name], stdout=subprocess.PIPE)
            s = p.stdout.read().decode()
            m = re.search('uid=(\d+)', s)
            uid = m.group(1)

            subprocess.run(['iptables', '-A', 'OUTPUT', '-o', 'eth0',
                            '-m', 'owner', '--uid-owner', uid, '-j', 'REJECT'])
        else:
            p = subprocess.Popen(['id', user.name], stdout=subprocess.PIPE)
            s = p.stdout.read().decode()
            m = re.search('uid=(\d+)', s)
            uid = m.group(1)

            subprocess.run(['iptables', '-D', 'OUTPUT', '-o', 'eth0',
                            '-m', 'owner', '--uid-owner', uid, '-j', 'REJECT'])

        # Disallow other users to sneak into this user's home directory
        subprocess.run(['chmod', '700', '/home/{}'.format(user.name)])
