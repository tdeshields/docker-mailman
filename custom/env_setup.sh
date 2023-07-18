#!/bin/bash

# this script will setup the environment on a fresh machine for the docker-mailman git project. 

# checking for or setting up the mailman-web local directories
if [ -d "/opt/mailman/web" ];
then
	:
else
	mkdir -p /opt/mailman/web
fi


# checking for or setting up mailman-core local directories
if [ -d "/opt/mailman/core" ];
then
	:
else
	mkdir -p /opt/mailman/core
fi


# Checking for or setting up the directory for our database backup
if [ -d "/opt/backup" ];
then
	:
else
	mkdir -p /opt/backup
fi


# Checking for or setting up the directory for our ssl certs
if [ -d "/opt/mailman/ssl" ];
then
	:
else
	mkdir -p /opt/mailman/ssl
fi


# Checking for or setting up the directory for nginx proxy
if [ -d "/opt/mailman/nginx/conf.d" ];
then
	:
else
	mkdir -p /opt/mailman/nginx/conf.d
fi



# changing to working dir and moving all the config files in the proper place
cd /opt/mailman/docker-mailman
cp custom/settings_local.py ../web/settings_local.py
cp custom/mailman-extra.cfg ../core/mailman-extra.cfg
cp custom/proxy.conf ../nginx/conf.d/proxy.conf

# Setting up the database backup and logrotate
logrotate_path="/etc/logrotate.d/db_backup"
logrotate_conf="/opt/mailman/docker-mailman/custom/db_backup"

cp "$logrotate_conf" "$logrotate_path"

chown root:root "$logrotate_path"
chmod 644 "$logrotate_path"

cron_dump="00 22 * * * /opt/mailman/docker-mailman/custom/db_backup.sh"
cron_log="05 22 * * * /usr/sbin/logrotate /etc/logrotate.d/db_backup --state /var/lib/logrotate/db_status"

(crontab -l 2>/dev/null; echo "$cron_dump") | crontab -
(crontab -l 2>/dev/null; echo "$cron_log") | crontab -



# Disabling sendmail so it doesn't fight with postfix
systemctl disable sendmail
systemctl stop sendmail

# Checking for or setting up postfix for use as the MTA
if ! command -v postfix &>/dev/null;
then
	yum install -y postfix
fi

postfix_conf="/etc/postfix/main.cf"
cp custom/main.cf /etc/postfix/main.cf
