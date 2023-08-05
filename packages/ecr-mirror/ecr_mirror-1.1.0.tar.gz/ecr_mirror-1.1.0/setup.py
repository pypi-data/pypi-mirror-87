# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecr_mirror']

package_data = \
{'': ['*']}

install_requires = \
['boto3', 'boto3-stubs[ecr]', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['ecr-mirror = ecr_mirror:cli']}

setup_kwargs = {
    'name': 'ecr-mirror',
    'version': '1.1.0',
    'description': 'Mirror public Docker images to private ECR repositories',
    'long_description': '# Docker ECR Mirror\n\n![](https://img.shields.io/pypi/v/ecr-mirror.svg)\n![](https://img.shields.io/pypi/l/ecr-mirror.svg)\n![](https://img.shields.io/pypi/pyversions/ecr-mirror.svg)\n\nMirror public docker images to ECR, automagically. This requires [Skopeo](https://github.com/containers/skopeo) to be installed.\n\n`pip install ecr-mirror`\n\n## Usage\n\n```\n$ ecr-mirror\nUsage: ecr-mirror [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --registry-id TEXT  The registry ID. This is usually your AWS account ID.\n  --role-arn TEXT     Assume a specific role to push to AWS\n  --help              Show this message and exit.\n\nCommands:\n  copy        Copy all tags that match a given glob expression into ECR\n  list-repos  List all repositories that will be synced\n  sync        Copy public images to ECR using ECR tags\n```\n\nCreate an ECR repository with the following two tags set:\n\n* `upstream-image` set to a public Docker hub image, i.e `nginx` or `istio/proxyv2`\n* `upstream-tags` set to a `/`-separated list of tag **globs**, i.e `1.6.*` or just `1.2-alpine`. ECR does not allow the\n  use of the `*` character in tag values, so you should use `+` as a replacement.\n\nTerraform example:\n\n```hcl\nresource "aws_ecr_repository" "repo" {\n  name = "nginx"\n  tags = {\n    upstream-image = "nginx",\n    // Mirror 1.16* and 1.17*\n    upstream-tags = "1.16+/1.17+"\n  }\n}\n```\n\nRunning `ecr-mirror sync` will begin concurrently fetching all images and pushing them to ECR.\n\nYou can run `ecr-mirror list` to see all repositories that will be mirrored.\n\nYou can also manually copy specific image patterns using `ecr-mirror copy`:\n\n`ecr-mirror copy "istio/proxyv2:1.6.*" ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com/istio-proxyv2`\n',
    'author': 'Tom Forbes',
    'author_email': 'tom.forbes@onfido.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
