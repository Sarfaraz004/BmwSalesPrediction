import joblib
from sklearn.ensemble import RandomForestRegressor
from ml_engine.ml.utils import load_data, encode_data

df = load_data()

features = [
    'model','year','region','fuel_type',
    'transmission','engine_size_l','mileage_km'
]

target = 'price_usd'
categorical = ['model','region','fuel_type','transmission']

df, encoders = encode_data(df, categorical)

X = df[features]
y = df[target]

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, 'ml_engine/ml/models/price_model.pkl')
joblib.dump(encoders, 'ml_engine/ml/models/encoders.pkl')

print("Price model trained")
