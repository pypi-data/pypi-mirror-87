# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aws_sso_util',
 'aws_sso_util._aws_sso_lib',
 'aws_sso_util._aws_sso_lib.vendored_botocore',
 'aws_sso_util.cfn_lib']

package_data = \
{'': ['*']}

install_requires = \
['aws-error-utils>=1.0.4,<2.0.0',
 'aws-sso-lib>=1.2.0,<2.0.0',
 'boto3>=1.16.13,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['aws-sso-util = aws_sso_util.cli:cli']}

setup_kwargs = {
    'name': 'aws-sso-util',
    'version': '2.18.0',
    'description': 'Utilities to make AWS SSO easier',
    'long_description': '# aws-sso-util\n## Making life with AWS SSO a little easier\n\n[AWS SSO](https://aws.amazon.com/single-sign-on/) has some rough edges, and `aws-sso-util` is here to smooth them out, hopefully temporarily until AWS makes it better.\n\n`aws-sso-util` contains utilities for the following:\n* Configuring `.aws/config`\n* Logging in/out\n* AWS SDK support\n* Looking up identifiers\n* CloudFormation\n\nThe underlying Python library for AWS SSO authentication is [`aws-sso-lib`](https://pypi.org/project/aws-sso-lib/), which has useful functions like interactive login, creating a boto3 session for specific a account and role, and the programmatic versions of the `lookup` functions in `aws-sso-util`.\n\n`aws-sso-util` supersedes `aws-sso-credential-process`, which is still available in its original form [here](https://github.com/benkehoe/aws-sso-credential-process).\nRead the updated docs for `aws-sso-util credential-process` [here](docs/credential-process.md).\n\n## Quickstart\n\n1. I recommend you install [`pipx`](https://pipxproject.github.io/pipx/), which installs the tool in an isolated virtualenv while linking the script you need.\n\nMac [and Linux](https://docs.brew.sh/Homebrew-on-Linux):\n```bash\nbrew install pipx\npipx ensurepath\n```\n\nOther:\n```bash\npython3 -m pip install --user pipx\npython3 -m pipx ensurepath\n```\n\n2. Install\n```bash\npipx install aws-sso-util\n```\n\n3. Learn\n```bash\naws-sso-util --help\n```\n\n## Documentation\n\nSee the full docs at [https://github.com/benkehoe/aws-sso-util](https://github.com/benkehoe/aws-sso-util)\n',
    'author': 'Ben Kehoe',
    'author_email': 'ben@kehoe.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benkehoe/aws-sso-util',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
