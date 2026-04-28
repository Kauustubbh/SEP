"""
Views for the rentals app.
Handles: Request, Approve, Reject, Complete.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from items.models import Item
from .models import Rental
from .forms import RentalRequestForm


@login_required
def rental_request_view(request, item_id):
    """
    Create a rental request for an item.
    GET: Show the rental request form.
    POST: Create the rental with status='Pending'.
    """
    item = get_object_or_404(Item, pk=item_id)

    # Can't rent your own item
    if item.owner == request.user:
        messages.error(request, "You can't rent your own item!")
        return redirect('item_detail', pk=item_id)

    # Can't rent an unavailable item
    if not item.available:
        messages.error(request, "This item is not available for rent.")
        return redirect('item_detail', pk=item_id)

    if request.method == 'POST':
        form = RentalRequestForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.item = item
            rental.renter = request.user
            rental.status = 'Pending'
            rental.save()
            messages.success(request, f"Rental request sent to {item.owner.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RentalRequestForm()

    return render(request, 'rentals/rental_request.html', {'form': form, 'item': item})


@login_required
def rental_approve_view(request, rental_id):
    """
    Owner approves a rental request.
    Only the item owner can approve.
    """
    rental = get_object_or_404(Rental, pk=rental_id)

    # Security: only the item owner can approve
    if rental.item.owner != request.user:
        messages.error(request, "You don't have permission to approve this rental.")
        return redirect('dashboard')

    if rental.status != 'Pending':
        messages.error(request, "This rental is not in Pending status.")
        return redirect('dashboard')

    rental.status = 'Approved'
    rental.save()
    messages.success(request, f"Rental approved for {rental.renter.username}!")
    return redirect('dashboard')


@login_required
def rental_reject_view(request, rental_id):
    """
    Owner rejects a rental request.
    Only the item owner can reject.
    """
    rental = get_object_or_404(Rental, pk=rental_id)

    # Security: only the item owner can reject
    if rental.item.owner != request.user:
        messages.error(request, "You don't have permission to reject this rental.")
        return redirect('dashboard')

    if rental.status != 'Pending':
        messages.error(request, "This rental is not in Pending status.")
        return redirect('dashboard')

    rental.status = 'Rejected'
    rental.save()
    messages.success(request, "Rental request rejected.")
    return redirect('dashboard')


@login_required
def rental_complete_view(request, rental_id):
    """
    Mark a rental as completed.
    Owner marks it complete when item is returned.
    Also increments the item's usage_count.
    """
    rental = get_object_or_404(Rental, pk=rental_id)

    # Security: only the item owner can mark as complete
    if rental.item.owner != request.user:
        messages.error(request, "You don't have permission to complete this rental.")
        return redirect('dashboard')

    if rental.status != 'Approved':
        messages.error(request, "Only approved rentals can be completed.")
        return redirect('dashboard')

    rental.status = 'Completed'
    rental.save()

    # Increment usage count on the item (tracks popularity)
    rental.item.usage_count += 1
    rental.item.save()

    messages.success(request, f"Rental completed! '{rental.item.title}' usage count updated.")
    return redirect('dashboard')
