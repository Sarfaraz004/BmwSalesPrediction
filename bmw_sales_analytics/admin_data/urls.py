from django.contrib import admin
from django.urls import path, include
from admin_data import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('analytics/data/<str:model>/', views.fetch_model_data, name='model_data'),
    path('graphs/', views.graphs_view, name='graphs_view'),
    path("dashboard/data/", views.dashboard_data, name="dashboard-data"),
    path("manage-users/delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path("manage-users/", views.manage_users, name="manage_users"),
    path("manage-users/update/<int:user_id>/", views.update_user_permissions, name="update_user_permissions"),
]
