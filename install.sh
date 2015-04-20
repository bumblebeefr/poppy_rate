#! /bin/sh
cd `echo "$0" | sed -e "s/[^\/]*$//"`

echo "Create virtualenv in local.virtualenv"
virtualenv local.virtualenv

mkdir local.lib

echo "Clone poppy_humanoid to be able to install last version from git"
git clone https://github.com/poppy-project/poppy-humanoid.git local.lib/poppy-humanoid

echo "Install python dependencies"
./local.virtualenv/bin/pip install --pre -r requirements.txt

