"""
Views for the items app.
CRUD: Create, Read, Update, Delete items.
Uses function-based views for simplicity.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item
from .forms import ItemForm


def item_list_view(request):
    """
    Homepage item list with optional search + category filter.
    Anyone (logged in or not) can browse items.
    """
    items = Item.objects.filter(available=True).order_by('-created_at')

    # --- Search by title ---
    search_query = request.GET.get('q', '')
    if search_query:
        items = items.filter(title__icontains=search_query)

    # --- Filter by category ---
    category = request.GET.get('category', '')
    if category:
        items = items.filter(category=category)

    # Get unique categories for filter buttons
    categories = Item.CATEGORY_CHOICES

    return render(request, 'items/item_list.html', {
        'items': items,
        'search_query': search_query,
        'selected_category': category,
        'categories': categories,
    })


def item_detail_view(request, pk):
    """Show a single item's full details."""
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'items/item_detail.html', {'item': item})


@login_required
def item_create_view(request):
    """
    Create a new item listing.
    Only logged-in users can list items.
    """
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user  # Set the owner to current user
            item.save()
            messages.success(request, f'"{item.title}" listed successfully!')
            return redirect('item_detail', pk=item.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ItemForm()

    return render(request, 'items/item_form.html', {'form': form, 'action': 'Create'})


@login_required
def item_edit_view(request, pk):
    """
    Edit an existing item.
    Only the item owner can edit it.
    """
    item = get_object_or_404(Item, pk=pk)

    # Security check: only owner can edit
    if item.owner != request.user:
        messages.error(request, "You don't have permission to edit this item.")
        return redirect('item_detail', pk=pk)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{item.title}" updated successfully!')
            return redirect('item_detail', pk=item.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ItemForm(instance=item)

    return render(request, 'items/item_form.html', {'form': form, 'action': 'Edit', 'item': item})


@login_required
def item_delete_view(request, pk):
    """
    Delete an item.
    Only the item owner can delete it.
    Shows a confirmation page on GET, deletes on POST.
    """
    item = get_object_or_404(Item, pk=pk)

    # Security check: only owner can delete
    if item.owner != request.user:
        messages.error(request, "You don't have permission to delete this item.")
        return redirect('item_detail', pk=pk)

    if request.method == 'POST':
        title = item.title
        item.delete()
        messages.success(request, f'"{title}" has been deleted.')
        return redirect('dashboard')

    return render(request, 'items/item_confirm_delete.html', {'item': item})
