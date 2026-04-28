"""
Main URL configuration for ReSource project.
All app URLs are included here with clear prefixes.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core pages: home, dashboard
    path('', include('core.urls')),

    # User auth: login, register, logout, profile
    path('', include('users.urls')),

    # Item CRUD: list, create, detail, edit, delete
    path('', include('items.urls')),

    # Rental workflow: request, approve, reject, complete
    path('', include('rentals.urls')),
]

# Serve media files (uploaded images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
