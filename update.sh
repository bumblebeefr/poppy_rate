#! /bin/sh
cd `echo "$0" | sed -e "s/[^\/]*$//"`

echo "Pull poppy_hunmanoid last modifictions"
cd local.lib/poppy-humanoid
git pull
cd -

echo "Upgrading python dependencies"
./local.virtualenv/bin/pip install --pre -U --force-reinstall -r requirements.txt

