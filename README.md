# MathPage Authenticator

MathPage Authenticator is a **custom JupyterHub authenticator** designed to
work with [ingang.mathpage.dev](https://ingang.mathpage.dev), an online lecture
learning system. It enables secure authentication for JupyterHub users based on
MathPage credentials.

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

1. Configure JupyterHub

Modify your `jupyterhub_config.py` to use `mathpage_authenticator`:

```python
from mathpage_authenticator import LocalMathPageAuthenticator
c.JupyterHub.authenticator_class = LocalMathPageAuthenticator
c.MathPageAuthenticator.auth_url = 'https://ingang.mathpage.dev/system/api/learner/check'
c.MathPageAuthenticator.auth_api_access_token = '820fd1095209f48f0682db52e40461cc2c11bac8'

c.Authenticator.admin_users = {'admin'}
c.Authenticator.auto_login = False
c.Authenticator.enable_auth_state = True
c.LocalAuthenticator.create_system_users = True

c.Spawner.cmd = ['/usr/local/venv/bin/jupyterhub-singleuser']
c.Spawner.environment = {'SAGE_ROOT': '/path/to/sage'}
```

## License

This project is licensed under the MIT License.
