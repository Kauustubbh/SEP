"""
Views for the users app.
Handles: Register, Login, Logout.
Django's built-in views handle login/logout - we just configure them.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm


def register_view(request):
    """
    Register a new user.
    GET: Show the registration form.
    POST: Validate, save user, log them in, redirect to dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')  # Already logged in? Go to dashboard.

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, f"Welcome to ReSource, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})
