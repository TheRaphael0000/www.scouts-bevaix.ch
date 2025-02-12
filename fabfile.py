#!/usr/bin/env python

import click
import fabric


def deploy(c):
    with c.cd("/opt/www.scouts-bevaix.ch"):
        c.run("git status")
        if not click.confirm("Stash and deploy to main ?", default=True):
            exit()
        c.run("git stash")
        c.run("git checkout main")
        c.run("git pull")
        c.run("docker compose up -d --build")


c = fabric.Connection(host="scouts-bevaix.ch", user="root", port=22)
deploy(c)
