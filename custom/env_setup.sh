#!/bin/bash

# this script will setup the environment on a fresh machine for the docker-mailman git project. 

# checking for or setting up the mailman-web local directories
if [ -d "/opt/mailman/web" ]
	exit 0
else
	mkdir -p /opt/mailman/web
fi


# checking for or setting up mailman-core local directories
if [ -d "/opt/mailman/core" ]
	exit 0
else
	mkdir -p /opt/mailman/core
fi

# Checking for or setting up the directory for our database backup
if [ -d "/opt/backup" ]
	exit 0
else
	mkdir -p /opt/backup
fi

# changing to working dir and moving all the config files in the proper place
cd /opt/mailman/docker-mailman
cp custom/settings_local.py ../web/settings_local.py
cp custom/mailman-extra.cfg ../core/mailman-extra.cfg

