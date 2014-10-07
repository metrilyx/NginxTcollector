===============
NginxTcollector
===============

Nginx tcollector plugin.

Usage
-----
In order to use this plugin, you'll need to add the following to your nginx configuration file::

    location /status {
        stub_status on;
        access_log off;
    }

Installation
------------
Copy **nginx_substatus.py** to **/usr/local/tcollector/collectors/0** or to the corresponding directory if installed else where.


**Note** - The default assumes the plugin will be running on the same machine running nginx.
