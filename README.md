# MathPage Authenticator

MathPage Authenticator is a **custom JupyterHub authenticator** designed to
work with [https://ingang.mathpage.dev](https://ingang.mathpage.dev). It enables secure
authentication for JupyterHub users based on MathPage credentials.

## Installation

To install `mathpage_authenticator`, run:

```sh
pip install git+https://github.com/kwankyu/mathpage-authenticator.git
```

## Usage

Configure your install of JupyterHub, modifying your `jupyterhub_config.py` to
use mathpage-authenticator:

```python
from mathpage_authenticator import LocalMathPageAuthenticator
c.JupyterHub.authenticator_class = LocalMathPageAuthenticator
c.LocalMathPageAuthenticator.auth_url = 'https://ingang.mathpage.dev/system/api/user/check'
c.LocalMathPageAuthenticator.auth_api_access_token = '<MATHPAGE_ACCESS_TOKEN>'
c.LocalMathPageAuthenticator.auth_allowed_users = ['<USER1>','<USER2>',...]
c.LocalMathPageAuthenticator.auto_login = False
c.LocalMathPageAuthenticator.enable_auth_state = True
c.LocalMathPageAuthenticator.allow_all = True
c.LocalMathPageAuthenticator.create_system_users = True
c.Spawner.cmd = ['<PATH_TO_JUPYTERHUB_SINGLEUSER>']
```

where `<PATH_TO_JUPYTERHUB_SINGLEUSER>` is what you get from the command.

```bash
$ which jupyterhub-singleuser
/usr/local/venv/bin/jupyterhub-singleuser
```

and `<MATHPAGE_ACCESS_TOKEN>` is obtained by request from
[https://ingang.mathpage.dev](https://ingang.mathpage.dev).

The `LocalMathPageAuthenticator` authenticator checks login credentials only
for users in `auth_allowed_users`. For example, if `<USER1>` is `alice`, then
users with username `alice` or usernames ending in `@alice` are checked.

## License

This project is licensed under the MIT License.
