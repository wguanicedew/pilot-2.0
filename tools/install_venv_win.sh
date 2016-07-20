#!/usr/bin/env bash
TOOLS=`dirname $0`
cd "$TOOLS"
cd ..

if [ ! -d .venv ]; then
    python -m pip install virtualenv
    python -m virtualenv --no-site-packages .venv
    tools/with_venv.sh python -m pip install -r tools/pip-requires
    tools/with_venv.sh python -m pip install -r tools/pip-requires-test
fi
