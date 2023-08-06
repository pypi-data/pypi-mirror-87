import numpy as np
from sklearn.pipeline import Pipeline
from skl_utils import *

if __name__ == '__main__':
    data = {
        'Age': [28, 34, 29, 42, 23, 19, 22, 30],
        # 'Size': ['M', 'S', 'S', 'L', 'M', 'L', 'S', 'S'],
        # 'Sex': ['M', 'M', 'M', 'F', 'M', 'M', 'F', 'F'],
        # 'Country': ['USA', 'China', 'USA', 'China', 'France', 'France', 'China', 'USA'],
        # 'Salary': [1000, 2500, 1200, 5000, 500, 250, None, 2400],
        # 'Num_Children': [2, 0, 0, 3, 2, 1, 4, 3],
        # 'Num_Pet': [5, 1, 0, 5, 2, 2, 3, 2]
    }
    df = pd.DataFrame(data)
    
    def inverse(X):
        return np.exp(X) - 1

    numeric_transformer = Pipeline([
        # ('select', ColumnExtractor(columns=['Age'])),
        # ('imputer', SimpleImputer(strategy='median')),
        # ('scaler', MinMaxScaler())
        ('select', FunctionTransformer(np.log1p, inverse)),
    ])
    
    print(df)

    data = numeric_transformer.fit_transform(df)

    print(data)
    
    reverse = numeric_transformer.inverse_transform(data)
    print(reverse)
