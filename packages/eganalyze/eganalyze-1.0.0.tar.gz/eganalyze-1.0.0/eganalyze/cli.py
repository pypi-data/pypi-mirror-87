import click
import pandas as pd


@click.command()
@click.argument('input', type=click.Path(exists=True))
def main(input):
    df = pd.read_csv(input)

    # Extract Loan ID from Project Name
    df['id'] = [val[-1].strip() for val in df['Project Name'].str.split(',')]

    # Build URL using Loan ID
    df['url'] = 'https://estateguru.co/portal/investment/single/' + df['id']

    # Calculate percentage of outstanding principal
    df['outstanding_principal_percentage'] = (df['Outstanding principal'] / df['Outstanding principal'].sum())

    # Calculate weighted interest rate
    df['interest_rate_weighted'] = (df['outstanding_principal_percentage'] * df['Interest Rate'])

    # Output
    click.echo(
        'Average interest rate: {0:.4f}%'.format(float(df['Interest Rate'].mean()))
    )
    click.echo(
        'Weighted average interest rate: {0:.4f}%'.format(float(df['interest_rate_weighted'].sum()))
    )