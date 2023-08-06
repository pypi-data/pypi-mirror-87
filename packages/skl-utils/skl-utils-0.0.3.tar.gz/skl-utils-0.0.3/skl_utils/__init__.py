import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from functools import reduce
from sklearn import base
from sklearn import compose
from sklearn import preprocessing
from sklearn import impute


class ColumnExtractor(base.TransformerMixin):

    def __init__(self, dtype_include=None, dtype_exclude=None, columns=None):
        self.dtype_include = dtype_include
        self.dtype_exclude = dtype_exclude
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if isinstance(X, pd.DataFrame):
            if self.dtype_include is not None or self.dtype_exclude is not None:
                return X.select_dtypes(include=self.dtype_include, exclude=self.dtype_exclude)
            else:
                return X[self.columns]
        else:
            return X


class ColumnSelector(compose.make_column_selector):

    def __init__(self, pattern=None, *, dtype_include=None, dtype_exclude=None, columns=None):
        if columns is not None:
            pattern = '|'.join(columns)
        super().__init__(pattern, dtype_include=dtype_include, dtype_exclude=dtype_exclude)


class FeatureUnion(base.TransformerMixin):

    def __init__(self, transformer_list):
        self.transformer_list = transformer_list

    def fit(self, X, y=None):
        for (name, t) in self.transformer_list:
            t.fit(X, y)
        return self

    def transform(self, X):
        Xts = [t.transform(X) for _, t in self.transformer_list]
        Xunion = reduce(lambda X1, X2: pd.merge(X1, X2, left_index=True, right_index=True), Xts)
        return Xunion


class FunctionTransformer(preprocessing.FunctionTransformer):

    def transform(self, X):
        Xf = super().transform(X)
        if isinstance(X, pd.DataFrame):
            Xf = pd.DataFrame(Xf, index=X.index, columns=X.columns)
        return Xf

    def inverse_transform(self, X):
        Xf = super().inverse_transform(X)
        if isinstance(X, pd.DataFrame):
            Xf = pd.DataFrame(Xf, index=X.index, columns=X.columns)
        return Xf


class OrdinalEncoder(preprocessing.OrdinalEncoder):

    def transform(self, X):
        Xf = super().transform(X)
        if isinstance(X, pd.DataFrame):
            Xf = pd.DataFrame(Xf, index=X.index, columns=X.columns)
        return Xf

    def inverse_transform(self, X):
        Xf = super().inverse_transform(X)
        if isinstance(X, pd.DataFrame):
            Xf = pd.DataFrame(Xf, index=X.index, columns=X.columns)
        return Xf


class OneHotEncoder(preprocessing.OneHotEncoder):

    def transform(self, X):
        Xf = super().transform(X)
        if isinstance(X, pd.DataFrame):
            Xf = pd.DataFrame(Xf.toarray(), index=X.index, columns=self.get_feature_names(X.columns))
        return Xf

    def inverse_transform(self, X):
        Xf = super().inverse_transform(X)
        if isinstance(X, pd.DataFrame):
            try:
                col_name = X.columns.tolist()[0].split('_')[0]
                Xf = pd.DataFrame(Xf, index=X.index, columns=[col_name])
            except RuntimeError:
                pass
        return Xf


class SimpleImputer(impute.SimpleImputer):

    def transform(self, X):
        Xf = super().transform(X)
        if isinstance(X, pd.DataFrame):
            Xf = pd.DataFrame(Xf, index=X.index, columns=X.columns)
        return Xf


class StandardScaler(preprocessing.StandardScaler):

    def transform(self, X, copy=None):
        Xf = super().transform(X, copy=None)
        if isinstance(X, pd.DataFrame):
            Xf = pd.DataFrame(Xf, index=X.index, columns=X.columns)
        return Xf

    def inverse_transform(self, X, copy=None):
        Xf = super().inverse_transform(X, copy=None)
        if isinstance(X, pd.DataFrame):
            Xf = pd.DataFrame(Xf, index=X.index, columns=X.columns)
        return Xf


class MinMaxScaler(preprocessing.MinMaxScaler):

    def transform(self, X):
        Xf = super().transform(X)
        if isinstance(X, pd.DataFrame):
            Xf = pd.DataFrame(Xf, index=X.index, columns=X.columns)
        return Xf

    def inverse_transform(self, X):
        Xf = super().inverse_transform(X)
        if isinstance(X, pd.DataFrame):
            Xf = pd.DataFrame(Xf, index=X.index, columns=X.columns)
        return Xf


class RobustScaler(preprocessing.RobustScaler):

    def transform(self, X):
        Xf = super().transform(X)
        if isinstance(X, pd.DataFrame):
            Xf = pd.DataFrame(Xf, index=X.index, columns=X.columns)
        return Xf

    def inverse_transform(self, X):
        Xf = super().inverse_transform(X)
        if isinstance(X, pd.DataFrame):
            Xf = pd.DataFrame(Xf, index=X.index, columns=X.columns)
        return Xf


class ColumnTransformer(compose.ColumnTransformer):

    def _hstack(self, Xs):
        try:
            # assumes Xs is DataFrame list
            if type(Xs) == list and all(isinstance(x, pd.DataFrame) for x in Xs):
                return pd.concat(Xs, axis=1)
            else:
                return super()._hstack(Xs)
        except RuntimeError:
            return super()._hstack(Xs)


def plot_decision_boundary(clf, x1, x2, y, labels=['0', '1'], cmap=plt.cm.Paired, figsize=(8, 7), step=0.1):
    # set figure size
    plt.figure(figsize=figsize)

    # generate mesh grid
    x_min, x_max = x1.min() - 20 * step, x1.max() + 20 * step
    y_min, y_max = x2.min() - 20 * step, x2.max() + 20 * step
    xx, yy = np.meshgrid(np.arange(x_min, x_max, step), np.arange(y_min, y_max, step))

    # predict labels in mesh grid
    z = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    # plot mesh grid
    plt.pcolormesh(xx, yy, z, cmap=cmap, alpha=.9)

    # plot data points
    scatter = plt.scatter(x1, x2, c=y, cmap=cmap, edgecolors='k', s=50, linewidths=1)
    plt.legend(handles=scatter.legend_elements()[0], labels=labels)

    return plt
