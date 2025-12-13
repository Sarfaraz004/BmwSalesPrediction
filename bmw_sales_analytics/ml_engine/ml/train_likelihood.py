from ml_engine.ml.utils import load_data, encode_data
import joblib
from sklearn.ensemble import RandomForestClassifier

FEATURES = [
    'model','price_usd','region',
    'fuel_type','engine_size_l'
]

TARGET = 'high_purchase'
CATEGORICAL = ['model','region','fuel_type']

df = load_data(required_columns=FEATURES + ['sales_classification'])

df['sales_classification'] = (
    df['sales_classification']
    .astype(str).str.strip().str.lower()
)

df['high_purchase'] = df['sales_classification'].map({
    'high': 1,
    'low': 0,
    'retail': 0
}).fillna(0)

df, encoders = encode_data(df, CATEGORICAL)

X = df[FEATURES]
y = df[TARGET]

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)

model.fit(X, y)

joblib.dump(model, 'ml_engine/ml/models/likelihood_model.pkl')
joblib.dump(encoders, 'ml_engine/ml/models/likelihood_encoders.pkl')

print(f"✅ Likelihood model trained on {len(df)} rows")
