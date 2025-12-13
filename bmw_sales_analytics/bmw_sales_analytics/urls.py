from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('visualization.urls')),
    path('admin/', admin.site.urls),
    path('basemode/', include('admin_data.urls')),
    path('ml_engine/', include('ml_engine.urls')),
]
