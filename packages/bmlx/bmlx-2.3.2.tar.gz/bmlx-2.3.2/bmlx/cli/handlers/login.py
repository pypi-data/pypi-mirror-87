import requests
import click
import json
import sys
from bmlx.bmlx_ini import BmlxINI
import openapi_client
from openapi_client.exceptions import ApiException as ApiException
from bmlx.metadata.bmlxflow_store import get_api_endpoint


def login(user, token, env):
    configuration = openapi_client.Configuration(
        get_api_endpoint(env), api_key={"X-Auth-Token": token}
    )
    api_client = openapi_client.ApiClient(configuration)
    auth_api = openapi_client.AuthApi(api_client)
    resp = auth_api.authenticate(user=user)
    if resp.error != "OK":
        click.echo("Login Failed: %s" % resp.error)
    else:
        click.echo("login success")
        b = BmlxINI(env)
        b.token = token
        b.user = user
        b.flush()
