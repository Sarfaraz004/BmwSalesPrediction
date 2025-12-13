# ml_engine/ml/train_likelihood.py

import joblib
from sklearn.ensemble import RandomForestClassifier
from ml_engine.ml.utils import load_data, encode_data

# 1️⃣ Load data
df = load_data()

# 2️⃣ Normalize classification column
df['sales_classification'] = (
    df['sales_classification']
    .astype(str)
    .str.strip()
    .str.lower()
)

# 3️⃣ Create target (FIXED)
df['high_purchase'] = df['sales_classification'].map({
    'high': 1,
    'low': 0,
    'retail': 0
})

# 4️⃣ SAFETY: fill remaining NaNs as 0
df['high_purchase'] = df['high_purchase'].fillna(0).astype(int)

# 5️⃣ Features
features = [
    'model',
    'price_usd',
    'region',
    'fuel_type',
    'engine_size_l'
]

categorical = ['model', 'region', 'fuel_type']
target = 'high_purchase'

# 6️⃣ Encode categoricals
df, encoders = encode_data(df, categorical)

X = df[features]
y = df[target]

# 7️⃣ Train classifier
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)

model.fit(X, y)

# 8️⃣ Save model
joblib.dump(model, "ml_engine/ml/models/likelihood_model.pkl")
joblib.dump(encoders, "ml_engine/ml/models/likelihood_encoders.pkl")

print(f"✅ Purchase likelihood model trained successfully on {len(df)} rows")
