#!/usr/bin/env bash

current_dir=`dirname $0`

source $current_dir/deploy.conf
$GOOGLE_APPS_SDK_HOME/dev_appserver.py $current_dir/db-cat/
echo 'http://localhost:8000/'