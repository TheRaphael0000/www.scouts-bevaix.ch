#!/usr/bin/env python

import click
import fabric


def deploy(c):
    with c.cd("/var/www/scouts-bevaix.ch/www.scouts-bevaix.ch"):
        c.run("git status")
        if not click.confirm("Stash and deploy to main ?", default=True):
            exit()
        c.run("git stash")
        c.run("git checkout main")
        c.run("git pull")
        c.run("systemctl restart www.scouts-bevaix.ch_gunicorn.service")


c = fabric.Connection(host="scouts-bevaix.ch", user="root", port=22)
deploy(c)
