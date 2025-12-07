# visualization/views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import CarSale

def dashboard(request):
    cars_list = CarSale.objects.all().order_by('-year')
    paginator = Paginator(cars_list, 25)  # 25 rows per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard.html', {'page_obj': page_obj})

# visualization/views.py
from django.shortcuts import render
from .models import CarSale
from django.http import JsonResponse
import pandas as pd

def analytics_dashboard(request):
    models = CarSale.objects.values_list('model', flat=True).distinct()
    return render(request, "analytics.html", {"models": models})


def fetch_model_data(request, model):
    year = request.GET.get("year")
    years_only = request.GET.get("years_only")

    # Query
    qs = CarSale.objects.filter(model=model)

    # If request only wants list of years
    if years_only:
        years = qs.values_list("year", flat=True).distinct()
        return JsonResponse({"years": sorted(list(years))})

    # Apply year filter for analytics
    if year:
        qs = qs.filter(year=year)

    df = pd.DataFrame(list(qs.values()))

    response = {
        "years": df["year"].tolist(),
        "prices": df["price_usd"].tolist(),
        "sales": df["sales_volume"].tolist(),
        "region_data": df.groupby("region")["sales_volume"].sum().to_dict()
    }
    return JsonResponse(response)

from django.db.models import Avg, Count

def dashboard_data(request):
    data = {
        "avg_price_by_model": list(
            CarSale.objects.values("model")
            .annotate(avg_price=Avg("price_usd"))
            .order_by("-avg_price")
        ),

        "sales_by_year": list(
            CarSale.objects.values("year")
            .annotate(total_sales=Avg("sales_volume"))
            .order_by("year")
        ),

        "sales_by_region": list(
            CarSale.objects.values("region")
            .annotate(total_sales=Avg("sales_volume"))
        ),

        "classification_count": list(
            CarSale.objects.values("sales_classification")
            .annotate(total=Count("id"))
        ),

        "mileage_vs_price": list(
            CarSale.objects.values("mileage_km", "price_usd")
        )
    }

    return JsonResponse(data)

def graphs_view(request):
    return render(request, "dashboard.html")

