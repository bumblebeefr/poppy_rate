#! /bin/sh
cd `echo "$0" | sed -e "s/[^\/]*$//"`
./local.virtualenv/bin/ipython notebook
