import click
from halo import Halo

from .. import convert_to_json, Services


@click.command(context_settings=dict(max_content_width=200))
@click.argument("path", type=click.Path(exists=True))
@click.option("-w", "--workers", default=3, show_default=True, help="amount of workers")
@click.option(
    "-o",
    "--output",
    help="output path for json files absolute or relative from current location.",
)
@click.option(
    "-s",
    "--skip",
    is_flag=True,
    default=False,
    help="Skip converting documents which are found to have been converted in output path.",
)
@click.pass_context
def to_json(ctx, path, workers, output, skip):
    """ Convert invoices to jsons """
    # Services available
    spinner = Halo(spinner="dots")
    spinner.start()
    services = Services(ctx, check_up=True)
    spinner.succeed(f"Found dir: {path}\n ")

    # Conversion
    skipped_files = convert_to_json(path, services, workers, output, skip)

    if skipped_files:
        spinner.fail("Could not convert all invoice(s) to json output.")
        for skipped_file in skipped_files:
            click.echo(f"{skipped_file[0]} - Error: {skipped_file[1]}")
    else:
        spinner.succeed("Converted all invoice(s) to json output.")
