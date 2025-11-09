from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/', include('prediction.urls')),
    path('visualization/', include('visualization.urls')),
    path('marketplace/', include('marketplace.urls')),
]
