import requests
import click
import json
import sys
from bmlx.bmlx_ini import BmlxINI

BMLX_HOST = "164.90.77.14"  # "bmlx.mlp.bigo.inner" #
BMLX_PORT = 8888


def login(user, token):
    resp = requests.get(
        "http://%s:%s/cas/validate?user=%s" % (BMLX_HOST, BMLX_PORT, user),
        headers={"X-Auth-Token": token,},
        allow_redirects=False,
    )

    if resp.status_code != 200:
        try:
            obj = json.loads(resp.content)
            message = obj["message"]
            click.echo("Login Failed: %s" % message)
        except (json.JSONDecodeError, KeyError):
            click.echo("Unexpected message: %s" % resp.content)
            sys.exit(-1)
    else:
        click.echo("login success")
        b = BmlxINI()
        b.token = token
        b.user = user
        b.flush()
