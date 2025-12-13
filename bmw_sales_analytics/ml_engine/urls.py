from django.urls import path
from .views import price_prediction, sales_prediction, purchase_likelihood

urlpatterns = [
  path('price/', price_prediction),
  path('sales/', sales_prediction),
  path('likelihood/', purchase_likelihood),
]
