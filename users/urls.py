"""
URL patterns for the users app.
Login/Logout use Django's built-in views.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),

    # Django's built-in login view - we just point it to our template
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

    # Django's built-in logout view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
