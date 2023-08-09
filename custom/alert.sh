#!/bin/bash

EMAIL="linuxadmins@groups.usm.edu"

# working dir
cd /opt/mailman/docker-mailman

# grabbing the container ID list
for container_id in $(/bin/podman ps --format "{{.ID}}");
do      
        # getting the container name for email alert
        container_name=$(/bin/podman inspect --format '{{.Name}}' "$container_id" |sed 's#^/##')

        # checking the health of the container by the ID
        if /bin/podman inspect --format '{{.State.Health.Status}}' "$container_id" |grep -q "unhealthy";
        then
                # Getting the logs from the container healthcheck
                healthcheck_logs=$(/bin/podman inspect --format '{{json .State.Health.Log}}' "$container_id" |jq -r)
                # creating the subject for the email
                subject="Podman Health Alert: $container_name"
                # packing it all together and sending in email
                echo -e "$healthcheck_logs" | mailx -s "$subject" -S v15-compat=yes -Ssmtp-auth=none -S mta=smtp://smtp.usm.edu:25 $EMAIL

        else
                :
        fi
done
