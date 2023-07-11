The files in this directory are the configuration changes that were made to make the container stack work with my environment.

- mailman-extra.cfg is placed locally in /opt/mailman/web/ and is passed into the container mailman-web.

- settings_local.py is placed locally in /opt/mailman/core/ and is passed into the container mailman-core.

- Take the lines in main.cf and add them to the /etc/postfix/main.cf on the host machine. This points the MTA postfix towards the container network gateway and defines the mailman hosts. 
