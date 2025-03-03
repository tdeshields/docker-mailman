#!/bin/bash

# creating the file name
file=mailmandb_backup.$(date +"%Y%m%d%H%M")

# Making sure the backup directory is present
if [ ! -d "/opt/backup" ]
	mkdir -p /opt/backup
fi

# Running the podman command to pull a postgresql dump file from the database
podman exec docker-mailman_database_1 pg_dump -U mailman -f /var/lib/postgresql/data/$file mailmandb

# compressing the dump file on the host side
gzip /opt/mailman/database/$file

# moving it to the proper directory
mv /opt/mailman/database/$file.gz /opt/backup/

# cleaning up older backups >7 days
find /opt/backup -type f -exec stat --format="%W %n" {} + |awk -v limit=$(date -d '7 days ago' +%s) '$1 < limit {print $2}' |xargs /bin/rm -f
