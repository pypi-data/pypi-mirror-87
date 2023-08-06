#!/usr/bin/env bash
if [ ! -z ${VIRTUAL_ENV+x} ]
    then
        deactivate
fi

mkdir -p log

git -C .pyenv pull || git clone https://github.com/pyenv/pyenv.git .pyenv


export PYENV_ROOT=$(readlink -f ./)/.pyenv
export PATH=$PATH:$PYENV_ROOT/bin:$HOME/.local/bin
export PATH=$(echo $(sed 's/:/\n/g' <<< $PATH | sort | uniq) | sed -e 's/\s/':'/g')


pyenv init

pyenv install -s 3.5-dev
pyenv install -s 3.6-dev 
pyenv install -s 3.7-dev 
pyenv install -s 3.8-dev 
pyenv install -s 3.9-dev

pyenv local 3.5-dev 3.6-dev 3.7-dev 3.8-dev 3.9-dev

$(pyenv which pip3.9) install --upgrade --upgrade-strategy eager --user virtualenv
if [ ! -d "env" ]
    then
        virtualenv -p $(pyenv which python3.9) env
fi
source env/bin/activate

pip install --upgrade --upgrade-strategy eager  pip
pip install --upgrade --upgrade-strategy eager 'tox>=3.7' tox-pyenv 'prompt-toolkit<3.0' ipython
pip install --upgrade --upgrade-strategy eager  black flake8 flake8-bugbear pydocstyle isort
pip install --upgrade --upgrade-strategy eager  pytest pytest-benchmark pytest-html
