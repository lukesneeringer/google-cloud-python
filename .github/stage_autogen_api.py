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


# It is important that this script can run with vanilla Python.
#
# Colors are non-trivial to do, so this is an 80% solution; if you install
# click, you get colors.
try:
    import click
    _ = click.secho
except ImportError:
    def _(message, file=sys.stdout, nl=True, **kwargs):
        """Print a message to the console."""
        if nl:
            message += '\n'
        file.write(message)


REPO_ROOT = os.path.realpath(os.path.dirname(__file__))


def stage_api(src, dest):
    """Stage an auto-generated API in the appropriate location in g-c-python.

    Args:
        src (str): The file path where the auto-generated API was written
            to disk.
        dest (str): Optional. The top-level directory where the API should
            be staged. This is determined based on the package name in
            setup.py and generally should not be needed.

    Returns:
        int: The exit code.
    """
    # Determine the destination directory, if one was not explicitly provided.
    #
    # We do this by reading setup.py and getting the name of the package from
    # there, and stripping the google-cloud- prefix.
    if dest:
        _('Destination directory explicitly set: \r', nl=False)
        _('\r%s/' % dest, fg='green')
    else:
        _('Determining directory to stage in: \r', nl=False)
        with io.open(os.path.join(src, 'setup.py'), 'r') as setup_py:
            setup = setup_py.read()
            package_match = re.search(r"name='google-cloud-([a-z-]+)',", setup)

            # If we could not find a package, abort loudly.
            if not package_match:
                _('\r ERROR', fg='red', bold=True)
                _('Could not determine the staging location. Is this a valid '
                  'Google Cloud API package? If it is, provide the dest '
                  'directory manually.', file=sys.stderr, fg='red', bold=True)
                return 32

            # The dest is the end of the package name; google-cloud prefix
            # dropped.
            dest = package_match.groups()[1].replace('-', '_')
            _('\r%s/' % dest, fg='green')

    # Determine if this is a new API or an existing one.
    _('Determining whether this API is being added or updated: \r', nl=False)
    new_api = False
    if not os.path.isdir(os.path.join(REPO_ROOT, dest)):
        new_api = True
    _('\r%s' % 'Added' if new_api else 'Updated', fg='green', bold=True)

    # If the API is new, copy the whole kit and kaboodle.
    copies = []
    if new_api:
        copies.append('')  # Project root.
    else:
        copies.append('google')
        copies.append('tests')
        copies.append('docs')
    _('Copying files: ')
    for copy_target in copies:
        _('  Copying %s/ from autogen: \r' % copy_target)
        shutil.copytree(
            src=os.path.join(src, copy_target),
            dst=os.path.join(REPO_ROOT, dest, copy_target),
        )
        _('\rSuccess', fg='green')


def _verify_src(src):
    """Verify the source directory."""
    src = os.path.realpath(os.path.expanduser(src))
    if not os.path.isdir(src):
        raise argparse.ArgumentTypeError('Path not found: %s' % src)
    if not os.path.isfile(os.path.join(src, 'setup.py')):
        raise argparse.ArgumentTypeError('Not a Python package: %s' % src)
    return src


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stage an auto-generated API')
    parser.add_argument('src', type=_verify_src)
    parser.add_argument('dest', default=None)
    args = parser.parse_args()

    try:
        return_value = stage_api(args.src, args.dest)
        sys.exit(return_value)
    except Exception as ex:
        _('An error occurred.', fg='red', bold=True, file=sys.stderr)
        _('What happened: %s\n' % ex, file=sys.stderr)
        _('It is possible that your working area has been left in an '
          'inconsistent state.', file=sys.stderr)
        sys.exit(1)
