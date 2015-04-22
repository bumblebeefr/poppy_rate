#! /bin/sh
cd `echo "$0" | sed -e "s/[^\/]*$//"`

echo "Create virtualenv in local.virtualenv"
virtualenv local.virtualenv


echo "Install python dependencies"
./local.virtualenv/bin/pip install --pre -r requirements.txt

