import click
import pandas as pd
from eganalyze import __version__
from eganalyze.lib import EgData


@click.group()
@click.version_option(
    __version__, '--version', message="%(prog)s, version %(version)s"
)
def main():
    pass


@main.command()
@click.argument('input', type=click.Path(exists=True))
def analyze(input):

    data = EgData(pd.read_csv(input))

    click.echo(
        'Mean interest rate: {0:.2f}%'.format(data.mean_interest_rate)
    )
    click.echo(
        'Outstanding mean interest rate: {0:.2f}%'.format(data.outstanding_mean_interest_rate)
    )
    click.echo(
        'Outstanding weighted mean interest rate: {0:.2f}%'.format(data.outstanding_weighted_mean_interest_rate)
    )

    click.echo(
        'Mean LTV: {0:.2f}%'.format(data.mean_ltv)
    )
    click.echo(
        'Outstanding mean LTV: {0:.2f}%'.format(data.outstanding_mean_ltv)
    )
    click.echo(
        'Outstanding weighted mean LTV: {0:.2f}%'.format(data.outstanding_weighted_mean_ltv)
    )