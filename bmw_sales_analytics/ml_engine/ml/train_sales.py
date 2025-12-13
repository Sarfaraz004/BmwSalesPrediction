from sklearn.ensemble import GradientBoostingRegressor
import joblib
from ml_engine.ml.utils import load_data, encode_data

df = load_data()

features = [
    'model','year','region','price_usd',
    'fuel_type','engine_size_l'
]

target = 'sales_volume'
categorical = ['model','region','fuel_type']

df, encoders = encode_data(df, categorical)

X = df[features]
y = df[target]

model = GradientBoostingRegressor()
model.fit(X, y)

joblib.dump(model, 'ml_engine/ml/models/sales_model.pkl')
joblib.dump(encoders, 'ml_engine/ml/models/sales_encoders.pkl')
