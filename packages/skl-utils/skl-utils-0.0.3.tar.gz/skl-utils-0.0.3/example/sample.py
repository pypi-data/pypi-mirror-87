from sklearn.pipeline import Pipeline
from skl_utils import *

if __name__ == '__main__':
    data = {
        'Age': [28, 34, 29, 42, 23, 19, 22, 30],
        'Size': ['M', 'S', 'S', 'L', 'M', 'L', 'S', 'S'],
        'Sex': ['M', 'M', 'M', 'F', 'M', 'M', 'F', 'F'],
        'Country': ['USA', 'China', 'USA', 'China', 'France', 'France', 'China', 'USA'],
        'Salary': [1000, 2500, 1200, 5000, 500, 250, None, 2400],
        'Num_Children': [2, 0, 0, 3, 2, 1, 4, 3],
        'Num_Pet': [5, 1, 0, 5, 2, 2, 3, 2]
    }
    df = pd.DataFrame(data)

    numeric_features = ['Age', 'Salary', 'Num_Children', 'Num_Pet']
    nominal_features = ['Sex', 'Country', 'Size']

    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', MinMaxScaler())])

    nominal_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(drop='first'))])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('nom', nominal_transformer, nominal_features),
        ],
        remainder='passthrough')
    
    data = preprocessor.fit_transform(df)

    print(data)
