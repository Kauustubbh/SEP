"""
Core app views.
Homepage and Dashboard are here.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from items.models import Item
from rentals.models import Rental


def home_view(request):
    """
    Homepage: shows all available items.
    Supports search by title and category filter.
    """
    items = Item.objects.filter(available=True).order_by('-created_at')

    # Search filter
    search_query = request.GET.get('q', '')
    if search_query:
        items = items.filter(title__icontains=search_query)

    # Category filter
    category = request.GET.get('category', '')
    if category:
        items = items.filter(category=category)

    categories = Item.CATEGORY_CHOICES

    return render(request, 'core/home.html', {
        'items': items,
        'search_query': search_query,
        'selected_category': category,
        'categories': categories,
    })


@login_required
def dashboard_view(request):
    """
    Dashboard: shows the user's listings and rental activity.

    My Listings tab:
      - Items the user has listed
      - Incoming rental requests on their items

    My Rentals tab:
      - Items the user has requested to rent
      - Status of those requests
    """
    user = request.user

    # Items this user has listed
    my_items = Item.objects.filter(owner=user).order_by('-created_at')

    # Rental requests coming IN to this user (people wanting to rent their items)
    incoming_requests = Rental.objects.filter(
        item__owner=user
    ).order_by('-created_at')

    # Rental requests this user has MADE (items they want to rent)
    my_rental_requests = Rental.objects.filter(
        renter=user
    ).order_by('-created_at')

    return render(request, 'core/dashboard.html', {
        'my_items': my_items,
        'incoming_requests': incoming_requests,
        'my_rental_requests': my_rental_requests,
    })
