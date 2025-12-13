from ml_engine.ml.utils import load_data, encode_data
import joblib
from sklearn.ensemble import GradientBoostingRegressor

FEATURES = [
    'model','year','region','price_usd',
    'fuel_type','engine_size_l'
]

TARGET = 'sales_volume'
CATEGORICAL = ['model','region','fuel_type']

df = load_data(required_columns=FEATURES + [TARGET])

df, encoders = encode_data(df, CATEGORICAL)

X = df[FEATURES]
y = df[TARGET]

model = GradientBoostingRegressor()
model.fit(X, y)

joblib.dump(model, 'ml_engine/ml/models/sales_model.pkl')
joblib.dump(encoders, 'ml_engine/ml/models/sales_encoders.pkl')

print(f"✅ Sales model trained on {len(df)} rows")
