#!/bin/bash

EMAIL="linuxadmins@groups.usm.edu"
#EMAIL="tony.deshields@usm.edu"
ALERT_FILE="/opt/mailman/docker-mailman/custom/alert_file.json"

# Checking to see if the alert_file is present. If not we create it.
if [ ! -f $ALERT_FILE ];
then
        touch $ALERT_FILE
        echo "{" >> $ALERT_FILE
        echo "  \"docker-mailman_database_1\": 0," >> $ALERT_FILE
        echo "  \"mailman-core\": 0," >> $ALERT_FILE
        echo "  \"mailman-web\": 0," >> $ALERT_FILE
        echo "  \"mailman-nginx\": 0" >> $ALERT_FILE
        echo "}" >> $ALERT_FILE
fi


for container_id in $(/bin/podman ps --format "{{.ID}}");
do

        container_name=$(/bin/podman inspect --format '{{.Name}}' "$container_id" |sed 's#^/##')
        alert_status=$(jq -r ".[\"$container_name\"]" "$ALERT_FILE")


        # Checking for unhealthy status, checking json flag, then alerting administrator if passing
        if /bin/podman inspect --format '{{.State.Health.Status}}' "$container_id" |grep -q "unhealthy" && [ "$alert_status" -eq 0 ];
        then
        
                healthcheck_logs=$(/bin/podman inspect --format '{{json .State.Health.Log}}' "$container_id" |jq -r '[.[-1]]')
                subject="Podman Health Status Alert: $container_name"
                echo -e "Here is the latest healthcheck log: \n\n$healthcheck_logs" | mailx -s "$subject" -S v15-compat=yes -Ssmtp-auth=none -S mta=smtp://smtp.usm.edu:25 $EMAIL

                jq ".[\"$container_name\"] = 1" "$ALERT_FILE" > "$ALERT_FILE.tmp"
                mv "$ALERT_FILE.tmp" "$ALERT_FILE"


        # Checking for changed health status, fix flag in json file, then alert administrator if passing
        elif /bin/podman inspect --format '{{.State.Health.Status}}' "$container_id" |grep -q "healthy" && [ "$alert_status" -eq 1 ];
        then

                subject="Podman Health Status Alert: $container_name"
                echo "$container_name has returned to a healthy state!" | mailx -s "$subject" -S v15-compat=yes -Ssmtp-auth=none -S mta=smtp://smtp.usm.edu:25 $EMAIL

                # Reset the alert status to 0 for this container in the JSON file
                jq ".[\"$container_name\"] = 0" "$ALERT_FILE" > "$ALERT_FILE.tmp"
                mv "$ALERT_FILE.tmp" "$ALERT_FILE"
                
        fi
done
