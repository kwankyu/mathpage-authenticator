# MathPage Authenticator

MathPage Authenticator is a **custom JupyterHub authenticator** designed to
work with [ingang.mathpage.dev](https://ingang.mathpage.dev). It enables secure
authentication for JupyterHub users based on MathPage credentials.

## Features

- Integrates JupyterHub authentication with **ingang.mathpage.dev**.
- Provides a seamless login experience for students and instructors.
- Designed for easy deployment and configuration.

## Installation

To install `mathpage_authenticator`, run:

```sh
pip install git+https://github.com/kwankyu/mathpage_authenticator.git
```

## Usage

Configure your install of JupyterHub. Modify your `jupyterhub_config.py` to use `mathpage_authenticator`:

```python
from mathpage_authenticator import LocalMathPageAuthenticator
c.JupyterHub.authenticator_class = LocalMathPageAuthenticator
c.LocalMathPageAuthenticator.auth_url = 'https://ingang.mathpage.dev/system/api/learner/check'
c.LocalMathPageAuthenticator.auth_api_access_token = '<MATHPAGE_ACCESS_TOKEN>'

c.Authenticator.admin_users = {'admin'}
c.Authenticator.auto_login = False
c.Authenticator.enable_auth_state = True
c.LocalAuthenticator.create_system_users = True

c.Spawner.cmd = ['<PATH_TO_JUPYTERHUB_SINGLEUSER>']
```

where `<PATH_TO_JUPYTERHUB_SINGLEUSER>` is what you get from the command

```bash
$ which jupyterhub-singleuser
/usr/local/venv/bin/jupyterhub-singleuser
```

and `<MATHPAGE_ACCESS_TOKEN>` is obtained by request from [ingang.mathpage.dev](https://ingang.mathpage.dev).

## License

This project is licensed under the MIT License.
