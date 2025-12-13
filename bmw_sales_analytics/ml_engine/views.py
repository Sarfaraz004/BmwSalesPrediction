# ml_engine/views.py
import joblib, pandas as pd
from django.shortcuts import render

price_model = joblib.load('ml_engine/ml/models/price_model.pkl')
encoders = joblib.load('ml_engine/ml/models/encoders.pkl')

def price_prediction(request):
    result = None

    if request.method == "POST":
        data = request.POST.dict()
        df = pd.DataFrame([data])

        for col, enc in encoders.items():
            df[col] = enc.transform(df[col])

        result = round(price_model.predict(df)[0], 2)

    return render(request, "ml/price_prediction.html", {"result": result})

sales_model = joblib.load('ml_engine/ml/models/sales_model.pkl')
sales_encoders = joblib.load('ml_engine/ml/models/sales_encoders.pkl')

def sales_prediction(request):
    result = None
    if request.method == "POST":
        df = pd.DataFrame([request.POST.dict()])
        for col, enc in sales_encoders.items():
            df[col] = enc.transform(df[col])
        result = int(sales_model.predict(df)[0])

    return render(request,"ml/sales_prediction.html",{"result":result})
