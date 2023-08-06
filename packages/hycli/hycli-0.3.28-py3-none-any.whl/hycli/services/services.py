import requests

import click

from halo import Halo

from .requests import request_token


class Services(object):
    def __init__(self, ctx, check_up=False):
        """
        Holds attributes related to service.
        """
        endpoints = ctx.obj.get("endpoints")

        self.env = ctx.obj.get("env")
        self.headers = ctx.obj.get("headers")
        self.username = ctx.obj.get("username")
        self.password = ctx.obj.get("password")
        self.authentication_endpoint = endpoints.get("authentication")

        if check_up:
            self.are_up(endpoints, ctx)

        self.extractor_endpoint = endpoints.get("extractor")

        self.token = None
        self.token_counter = 0
        self.refresh_token()

    def are_up(self, endpoints, ctx):
        """ Check if endpoints are reachable. """
        for name, url in endpoints.items():
            url_spinner = Halo(spinner="dots")
            svc = name.capitalize()

            try:
                req = requests.get(url)

            # On connection error.
            except requests.exceptions.ConnectionError:
                url_spinner.fail(f"{svc} on endpoint {url} is offline\n")
                endpoints[name] = None
                if name == "extractor":
                    click.echo(
                        f"Expected extraction service on {url}, service is mandatory."
                    )
                    ctx.exit()
            except Exception as e:
                url_spinner.fail(f"{svc} on endpoint {url} is offline\n")
                endpoints[name] = None
                if name == "extractor":
                    click.echo(
                        f"Expected extraction service on {url}, service is mandatory.\n{e}"
                    )
                    ctx.exit()
            # Connection was successful on 401 and 405.
            else:
                if req.status_code == 401 or req.status_code == 405:
                    url_spinner.succeed(f"{svc} endpoint is online\n")
                else:
                    url_spinner.fail(f"{svc} endpoint returns {req.status_code}\n")
                    endpoints[name] = None

    def get_token(self, refresh_on_every=50):
        if self.token_counter % refresh_on_every == 0:
            self.refresh_token()
        self.token_counter += 1
        return self.token

    def refresh_token(self):
        if self.env != "localhost":
            self.token = request_token(
                self.authentication_endpoint, self.username, self.password
            )
