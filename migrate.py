#!/usr/bin/env python

from fabric import Connection

c = Connection(host="scouts-bevaix.ch", user="root", port=22)

with c.cd("/var/www/scouts-bevaix.ch/www.scouts-bevaix.ch"):
    c.run("git pull")
    c.run("systemctl restart www.scouts-bevaix.ch_gunicorn.service")
