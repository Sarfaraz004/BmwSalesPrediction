from django.contrib import admin
from django.urls import path, include
from admin_data import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('analytics/data/<str:model>/', views.fetch_model_data, name='model_data'),
    path('graphs/', views.graphs_view, name='graphs_view'),
    path("dashboard/data/", views.dashboard_data, name="dashboard-data"),
]
