import pandas as pd
from admin_data.models import CarSale
from sklearn.preprocessing import LabelEncoder

DROP_COLUMNS = ['id', 'payment_id', 'purchase_date']

def load_data(required_columns=None):
    """
    Load CarSale data safely.
    - Drops non-ML columns (payment_id, purchase_date)
    - Drops rows ONLY if required columns are missing
    """
    qs = CarSale.objects.all().values()
    df = pd.DataFrame(qs)

    # 1️⃣ Drop irrelevant columns
    df = df.drop(columns=DROP_COLUMNS, errors='ignore')

    # 2️⃣ Drop rows only if REQUIRED columns are missing
    if required_columns:
        df = df.dropna(subset=required_columns)

    return df

def encode_data(df, categorical_cols):
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    return df, encoders
