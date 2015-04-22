#! /bin/sh
cd `echo "$0" | sed -e "s/[^\/]*$//"`

echo "Upgrading python dependencies"
./local.virtualenv/bin/pip install --pre -U --force-reinstall -r requirements.txt

