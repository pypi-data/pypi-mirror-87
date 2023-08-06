import click
from halo import Halo

from .. import convert_to_csv, Services


@click.command(context_settings=dict(max_content_width=200))
@click.argument("path", type=click.Path(exists=True))
@click.option("-w", "--workers", default=1, show_default=True, help="amount of workers")
@click.option(
    "-p",
    "--probability",
    default=False,
    show_default=True,
    help="include probability",
    is_flag=True,
)
@click.pass_context
def to_csv(ctx, path, workers, probability):
    """ Convert invoice to csv """
    # Services available
    spinner = Halo(spinner="dots")
    spinner.start()
    services = Services(ctx, check_up=True)
    spinner.succeed(f"Found dir: {path}\n ")

    # Conversion
    convert_to_csv(path, services, workers, path)
    spinner.succeed("Converted invoice(s) to csv")
