from ml_engine.ml.utils import load_data, encode_data
import joblib
from sklearn.ensemble import RandomForestRegressor

FEATURES = [
    'model','year','region','fuel_type',
    'transmission','engine_size_l','mileage_km'
]

TARGET = 'price_usd'
CATEGORICAL = ['model','region','fuel_type','transmission']

# Load only required rows
df = load_data(required_columns=FEATURES + [TARGET])

df, encoders = encode_data(df, CATEGORICAL)

X = df[FEATURES]
y = df[TARGET]

model = RandomForestRegressor(n_estimators=300, max_depth=15, random_state=42)
model.fit(X, y)

joblib.dump(model, 'ml_engine/ml/models/price_model.pkl')
joblib.dump(encoders, 'ml_engine/ml/models/encoders.pkl')

print(f"✅ Price model trained on {len(df)} rows")
