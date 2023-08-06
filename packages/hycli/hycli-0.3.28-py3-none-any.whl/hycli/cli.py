import click

from .commands import to_csv, to_xlsx, to_json, compare
from .commons.consts import default_endpoints
from . import __version__


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"Version {__version__}")
    ctx.exit()


@click.group()
@click.option(
    "-v",
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Print out hycli version",
)
@click.option(
    "-e",
    "--endpoint-env",
    default="production",
    show_default=True,
    type=click.Choice(["localhost", "staging", "production"], case_sensitive=False),
    help="endpoint environment",
)
@click.option(
    "-u",
    "--username",
    envvar="HYCLI_USERNAME",
    default=None,
    help="your API username for accessing the environment",
)
@click.option(
    "-p",
    "--password",
    envvar="HYCLI_PASSWORD",
    default=None,
    help="your API password for accessing the environment",
)
@click.option(
    "--extractor", help="custom extractor endpoint",
)
@click.option(
    "-H",
    "--header",
    multiple=True,
    help="extractor endpoint header(s) can be multiple. Similair to curl, e.g. -H 'keyheader: value' -H '2ndkeyheader: 2ndvalue'",
)
@click.pass_context
def main(ctx, endpoint_env, username, password, extractor, header):
    """
    Can extract information from a directory of documents (invoices, receipts) to csv/xlsx using the Hypatos Extraction service.
    """
    ctx.obj = {
        "env": endpoint_env,
        "headers": {h.split(":")[0].strip(): h.split(":")[1].strip() for h in header},
    }

    ctx.obj["endpoints"] = {
        k: v for k, v in default_endpoints[endpoint_env].items() if v is not None
    }

    if username:
        ctx.obj["username"] = username

    if password:
        ctx.obj["password"] = password

    if extractor:
        ctx.obj["endpoints"]["extractor"] = extractor


main.add_command(to_csv.to_csv)
main.add_command(to_xlsx.to_xlsx)
main.add_command(to_json.to_json)
main.add_command(compare.compare)

if __name__ == "__main__":
    main()
