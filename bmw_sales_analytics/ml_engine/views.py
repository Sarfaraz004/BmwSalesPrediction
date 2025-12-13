# ml_engine/views.py

import pandas as pd
import joblib
from django.shortcuts import render
from functools import wraps

def staff_or_superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        
        # Not logged in → go to login
        if not user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        
        # Logged in but not staff → show cute Forbidden page
        if not (user.is_staff or user.is_superuser):
            return render(request, 'errors/403.html', status=403)
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

price_model = joblib.load('ml_engine/ml/models/price_model.pkl')
encoders = joblib.load('ml_engine/ml/models/encoders.pkl')

FEATURES = [
    'model',
    'year',
    'region',
    'fuel_type',
    'transmission',
    'engine_size_l',
    'mileage_km'
]

@staff_or_superuser_required
def price_prediction(request):
    result = None

    if request.method == "POST":
        # 1️⃣ Extract ONLY required fields
        input_data = {f: request.POST.get(f) for f in FEATURES}

        # 2️⃣ Create DataFrame
        df = pd.DataFrame([input_data])

        # 3️⃣ Convert numeric fields
        df['year'] = df['year'].astype(int)
        df['engine_size_l'] = df['engine_size_l'].astype(float)
        df['mileage_km'] = df['mileage_km'].astype(float)

        # 4️⃣ Encode categoricals
        for col, enc in encoders.items():
            df[col] = enc.transform(df[col].astype(str))

        # 5️⃣ Predict
        result = round(price_model.predict(df)[0], 2)

    return render(
        request,
        "ml/price_prediction.html",
        {"result": result}
    )

# ml_engine/views.py

import pandas as pd
import joblib
from django.shortcuts import render

sales_model = joblib.load('ml_engine/ml/models/sales_model.pkl')
sales_encoders = joblib.load('ml_engine/ml/models/sales_encoders.pkl')

FEATURES = [
    'model',
    'year',
    'region',
    'price_usd',
    'fuel_type',
    'engine_size_l'
]

@staff_or_superuser_required
def sales_prediction(request):
    result = None

    if request.method == "POST":
        # 1️⃣ Extract ONLY required features
        input_data = {f: request.POST.get(f) for f in FEATURES}

        # 2️⃣ Build DataFrame
        df = pd.DataFrame([input_data])

        # 3️⃣ Convert numeric columns
        df['year'] = df['year'].astype(int)
        df['price_usd'] = df['price_usd'].astype(float)
        df['engine_size_l'] = df['engine_size_l'].astype(float)

        # 4️⃣ Encode categorical columns
        for col, enc in sales_encoders.items():
            df[col] = enc.transform(df[col].astype(str))

        # 5️⃣ Predict
        result = int(sales_model.predict(df)[0])

    return render(
        request,
        "ml/sales_prediction.html",
        {"result": result}
    )


# ml_engine/views.py

import pandas as pd
import joblib
from django.shortcuts import render

likelihood_model = joblib.load('ml_engine/ml/models/likelihood_model.pkl')
likelihood_encoders = joblib.load('ml_engine/ml/models/likelihood_encoders.pkl')

FEATURES = [
    'model',
    'price_usd',
    'region',
    'fuel_type',
    'engine_size_l'
]

@staff_or_superuser_required
def purchase_likelihood(request):
    probability = None
    label = None

    if request.method == "POST":
        # 1️⃣ Extract ONLY trained features
        input_data = {f: request.POST.get(f) for f in FEATURES}

        # 2️⃣ Build DataFrame
        df = pd.DataFrame([input_data])

        # 3️⃣ Convert numeric fields
        df['price_usd'] = df['price_usd'].astype(float)
        df['engine_size_l'] = df['engine_size_l'].astype(float)

        # 4️⃣ Encode categoricals
        for col, enc in likelihood_encoders.items():
            df[col] = enc.transform(df[col].astype(str))

        # 5️⃣ Predict probability
        probability = likelihood_model.predict_proba(df)[0][1] * 100

        # Optional readable label
        if probability >= 70:
            label = "High Purchase Likelihood"
        elif probability >= 40:
            label = "Medium Purchase Likelihood"
        else:
            label = "Low Purchase Likelihood"

    return render(
        request,
        "ml/likelihood.html",
        {
            "prob": round(probability, 2) if probability else None,
            "label": label
        }
    )
