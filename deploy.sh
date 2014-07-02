#!/usr/bin/env bash

current_dir=`dirname $0`

source $current_dir/deploy.conf
$GOOGLE_APPS_SDK_HOME/appcfg.py update --email=$UPLOADER_EMAIL $current_dir/db-cat/