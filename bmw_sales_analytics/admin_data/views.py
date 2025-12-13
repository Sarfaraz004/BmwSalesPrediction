# visualization/views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import CarSale
from django.http import JsonResponse
import pandas as pd
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps
from django.shortcuts import render, redirect

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

@staff_or_superuser_required
def dashboard(request):
    cars_list = CarSale.objects.all().order_by('-year')
    paginator = Paginator(cars_list, 25)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard.html', {'page_obj': page_obj})

@staff_or_superuser_required
def analytics_dashboard(request):
    models = CarSale.objects.values_list('model', flat=True).distinct()
    return render(request, "analytics.html", {"models": models})


@staff_or_superuser_required
def fetch_model_data(request, model):
    year = request.GET.get("year")
    years_only = request.GET.get("years_only")
    qs = CarSale.objects.filter(model=model)
    if years_only:
        years = qs.values_list("year", flat=True).distinct()
        return JsonResponse({"years": sorted(list(years))})
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


@staff_or_superuser_required
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


@staff_or_superuser_required
def graphs_view(request):
    return render(request, "dashboard.html")

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        
        if not user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        
        if not user.is_superuser:
            return render(request, 'errors/403.html', status=403)
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@superuser_required
def manage_users(request):
    search_query = request.GET.get("search", "").strip()

    # Default: show staff users only
    if search_query:
        users = User.objects.filter(username__icontains=search_query)
    else:
        users = User.objects.filter(is_staff=True)

    return render(request, "manage_users.html", {"users": users, "search_query": search_query})


@superuser_required
def update_user_permissions(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)

        user.is_staff = bool(request.POST.get("is_staff"))
        user.is_superuser = bool(request.POST.get("is_superuser"))
        user.save()

    return redirect("manage_users")


@superuser_required
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)

    # Prevent superuser from deleting themselves
    if request.user.id == user.id:
        return render(request, "errors/403.html", {"message": "You cannot delete your own account."}, status=403)

    user.delete()
    return redirect("/manage-users/")
