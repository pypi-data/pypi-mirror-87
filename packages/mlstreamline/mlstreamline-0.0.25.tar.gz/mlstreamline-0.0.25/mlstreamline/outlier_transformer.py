from sklearn.base import BaseEstimator, TransformerMixin
from numpy import percentile, vectorize


def replace_outliers(value, upper, lower):
    if value > upper:
        return upper
    elif value < lower:
        return lower
    else:
        return value


replace_outliers = vectorize(replace_outliers)


class OutlierTransformer(BaseEstimator, TransformerMixin):
    # Class Constructor
    def __init__(self):
        pass

    # Return self, nothing else to do here
    def fit(self, X, y=None):
        return self

    # Custom transform method we wrote that creates aformentioned features and drops redundant ones
    def transform(self, X, y=None):
        column_data = X.copy()
        q25, q75 = percentile(column_data, 25), percentile(column_data, 75)
        iqr = q75 - q25
        # calculate the outlier cutoff
        cut_off = iqr * 1.5
        lower, upper = q25 - cut_off, q75 + cut_off
        column_data = replace_outliers(column_data, upper, lower)
        return column_data
