import click
import pandas as pd
from eganalyze import __version__


@click.group()
@click.version_option(
    __version__, '--version', message="%(prog)s, version %(version)s"
)
def main():
    pass


@main.command()
@click.argument('input', type=click.Path(exists=True))
def analyze(input):
    df = pd.read_csv(input)

    # Extract Loan ID from Project Name
    df['id'] = [val[-1].strip() for val in df['Project Name'].str.split(',')]

    # Build URL using Loan ID
    df['url'] = 'https://estateguru.co/portal/investment/single/' + df['id']

    # Calculate percentage of outstanding principal
    df['outstanding_principal_percentage'] = (df['Outstanding principal'] / df['Outstanding principal'].sum())

    # Calculate weighted interest rate
    df['interest_rate_weighted'] = (df['outstanding_principal_percentage'] * df['Interest Rate'])

    click.echo(
        'Mean interest rate: {0:.4f}%'.format(float(df['Interest Rate'].mean()))
    )
    click.echo(
        'Weighted mean interest rate: {0:.4f}%'.format(float(df['interest_rate_weighted'].sum()))
    )