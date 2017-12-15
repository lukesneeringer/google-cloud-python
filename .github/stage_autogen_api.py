#!/usr/bin/env python
# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script exists to take output from artman and stage it appropriately
# in google-cloud-python.

import argparse
import io
import os
import re
import shutil
import sys

try:
    import click
except ImportError:
    print('You need the `click` Python library to run this script.')
    print('Install it with: `pip install click`.')
    sys.exit(120)


REPO_ROOT = os.path.realpath(os.path.dirname(__file__))


@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.option('--dest', default=None)
def stage_api(src, dest):
    _ = click.secho

    # Sanity check: Ensure that the source directory looks like an API.
    if not os.path.isfile(os.path.join(src, 'setup.py')):
        raise click.BadParameter('Not a Python package: %s' % src)

    # Determine the destination directory, if one was not explicitly provided.
    #
    # We do this by reading setup.py and getting the name of the package from
    # there, and stripping the google-cloud- prefix.
    if dest:
        _('Destination directory explicitly set: \r', nl=False)
        _('\r%s/' % dest, fg='green', bold=True)
    else:
        _('Determining directory to stage in: \r', nl=False)
        with io.open(os.path.join(src, 'setup.py'), 'r') as setup_py:
            setup_script = setup_py.read()
