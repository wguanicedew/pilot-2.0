#    copyright: European Organization for Nuclear Research (CERN)
#    @license: Licensed under the Apache License, Version 2.0 (the "License");
#    You may not use this file except in compliance with the License.
#    You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""
Installation script Pilot's development virtualenv
"""

import optparse
import os
import subprocess
import sys
import imp
from distutils.spawn import find_executable


ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
VENV = os.path.join(ROOT, '.venv')
PIP_REQUIRES = os.path.join(ROOT, 'tools', 'pip-requires')
PIP_REQUIRES_TEST = os.path.join(ROOT, 'tools', 'pip-requires-test')


def die(message, *args):
    print >> sys.stderr, message % args
    sys.exit(1)


def run_command(cmd, redirect_output=True, check_exit_code=True, shell=False):
    """
    Runs a command in an out-of-process shell, returning the
    output of that command.  Working directory is ROOT.
    """
    if shell:
        cmd = ['sh', '-c', cmd]
    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE if redirect_output else None)
    output = proc.communicate()[0]
    if check_exit_code and proc.returncode != 0:
        # print("ec = %d " % proc.returncode)
        die('Command "%s" failed.\n%s', ' '.join(cmd), output)
    return output


def has_module(mod):
    try:
        imp.find_module(mod)
        return True
    except ImportError:
        return False


HAS_EASY_INSTALL = bool(find_executable("easy_install"))
HAS_VIRTUALENV = has_module('virtualenv')
HAS_PIP = has_module('pip')
HAS_CURL = bool(find_executable('curl'))


def check_dependencies():
    """Make sure virtualenv is in the path."""
    global HAS_VIRTUALENV

    if not HAS_VIRTUALENV:
        print 'virtualenv not found.'
        # Try installing it via curl/pip/easy_install...
        if HAS_PIP:
            print 'Installing virtualenv via pip...'
            if not run_command([sys.executable, '-m', 'pip', 'install', 'virtualenv']).strip():
                die("Failed to install virtualenv.")
            print 'done.'
        elif HAS_EASY_INSTALL:
            print 'Installing virtualenv via easy_install...'
            if not run_command(['easy_install', 'virtualenv']).strip():
                die("Failed to install virtualenv.")
            print 'done.'
    print 'done.'
    HAS_VIRTUALENV = True


def create_virtualenv(venv=VENV):
    """
    Creates the virtual environment and installs PIP only into the
    virtual environment
    """
    if HAS_VIRTUALENV:
        print 'Creating venv...'
        run_command([sys.executable, "-m", 'virtualenv', '-q', '--no-site-packages', VENV])
    elif HAS_CURL:
        print 'Creating venv via curl...',
        if not run_command("curl -s https://raw.github.com/pypa/virtualenv/master/virtualenv.py | %s -"
                           " --no-site-packages %s" % (sys.executable, VENV), shell=True):
            die('Failed to install virtualenv with curl.')
    print 'done.'
    print 'Installing pip in virtualenv...',
    if not run_command(['sh', 'tools/with_venv.sh', 'easy_install', 'pip>1.0']).strip():
        die("Failed to install pip.")
    print 'done.'


def install_dependencies(venv=VENV, client=False):
    print 'Installing dependencies with pip (this can take a while)...'

    if not client:
        run_command(['.venv/bin/pip', 'install', '-r', PIP_REQUIRES], redirect_output=False)

    run_command(['.venv/bin/pip', 'install', '-r', PIP_REQUIRES_TEST], redirect_output=False)


def _detect_python_version(venv):
    lib_dir = os.path.join(venv, "lib")
    for pathname in os.listdir(lib_dir):
        if pathname.startswith('python'):
            return pathname
    raise Exception('Unable to detect Python version')


def print_help():
    help = """
 Pilot development environment setup is complete.

 Pilot development uses virtualenv to track and manage Python dependencies
 while in development and testing.

 To activate the Pilot virtualenv for the extent of your current shell session
 you can run:

 $ source .venv/bin/activate

 Or, if you prefer, you can run commands in the virtualenv on a case by case
 basis by running:

 $ tools/with_venv.sh <your command>

 Also, make test will automatically use the virtualenv.
    """
    print help


if __name__ == '__main__':

    parser = optparse.OptionParser()
    (options, args) = parser.parse_args()
    # check_dependencies()
    create_virtualenv()
    install_dependencies()
    print_help()
