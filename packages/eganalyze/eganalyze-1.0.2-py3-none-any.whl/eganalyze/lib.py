from eganalyze import settings


class EgData:

    def __init__(self, df):
        self.df = df
        self._normalize_column_names()
        self._enrich()

    def _normalize_column_names(self):
        # "Interest Rate" becomes "interest_rate"
        self.df = self.df.rename(columns=lambda x: x.replace(' ', '_').lower())

    def _enrich(self):
        # Loan ID from Project Name
        self.df['id'] = [val[-1].strip() for val in self.df['project_name'].str.split(',')]

        # Build URL using Loan ID
        self.df['url'] = settings.LOAN_URL + self.df['id']

        # Calculate percentage of outstanding principal
        self.df['outstanding_principal_percentage'] = (self.df['outstanding_principal'] / self.df['outstanding_principal'].sum())

        # Calculate weighted interest rate
        self.df['outstanding_interest_rate_weighted'] = (self.df['outstanding_principal_percentage'] * self.df['interest_rate'])

    @property
    def mean_interest_rate(self):
        return float(self.df['interest_rate'].mean())

    @property
    def outstanding_mean_interest_rate(self):
        return float(self.df[self.df.outstanding_principal > 0]['interest_rate'].mean())

    @property
    def outstanding_weighted_mean_interest_rate(self):
        return float(self.df['outstanding_interest_rate_weighted'].sum())
