NginxTcollector
===============

Nginx tcollector plugin.

In order to use this plugin, you'll need to add the following to your nginx configuration file:

	location /status {
        stub_status on;
        access_log off;
    }

Then copy **nginx_substatus.py** to /usr/local/tcollector/collectors/0/ or to the corresponding directory if installed else where.