#!/bin/bash
source /usr/local/bin/config_env

PRE=""
CMD="$VE_DIR/bin/python manage.py celeryd -E $CELERY_OPTS --scheduler=djcelery.schedulers.DatabaseScheduler --settings=unisubs_settings"

cd $APP_DIR
if [ ! -z "$NEW_RELIC_LICENSE_KEY" ] ; then
    $VE_DIR/bin/pip install -U newrelic
    PRE="$VE_DIR/bin/newrelic-admin run-program "
fi

echo "Starting Worker..."
$PRE $CMD
