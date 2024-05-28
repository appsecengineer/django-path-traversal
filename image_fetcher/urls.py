# image_fetcher/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('image_app.urls')),  # Include the URLs from your 'image_app'
]

