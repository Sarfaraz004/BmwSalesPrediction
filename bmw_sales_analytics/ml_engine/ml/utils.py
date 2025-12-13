import pandas as pd
from admin_data.models import CarSale
from sklearn.preprocessing import LabelEncoder

def load_data():
    qs = CarSale.objects.all().values()
    df = pd.DataFrame(qs)
    df.dropna(inplace=True)
    return df

def encode_data(df, categorical_cols):
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
    return df, encoders
