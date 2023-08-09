#!/bin/bash

EMAIL="linuxadmins@groups.usm.edu"


cd /opt/mailman/docker-mailman

for container_id in $(/bin/podman ps --format "{{.ID}}");
do
        container_name=$(/bin/podman inspect --format '{{.Name}}' "$container_id" |sed 's#^/##')

        if /bin/podman inspect --format '{{.State.Health.Status}}' "$container_id" |grep -q "unhealthy";
        then
                healthcheck_logs=$(/bin/podman inspect --format '{{json .State.Health.Log}}' "$container_id" |jq -r)
                subject="Podman Health Alert: $container_name"

                echo -e "$healthcheck_logs" | mailx -s "$subject" -S v15-compat=yes -Ssmtp-auth=none -S mta=smtp://smtp.usm.edu:25 $EMAIL

        else
                :
        fi
done
