"""
Rentals app models.
A Rental tracks the entire lifecycle of a rental request.
"""

from django.db import models
from django.contrib.auth.models import User
from items.models import Item


class Rental(models.Model):
    """
    Represents a rental transaction between a renter and an item owner.

    Workflow:
        Renter requests → status = 'Pending'
        Owner approves  → status = 'Approved'
        Owner rejects   → status = 'Rejected'
        After use       → status = 'Completed' (item usage_count++)
    """

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    # The item being rented
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='rentals')

    # The person renting (not the owner)
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_rentals')

    # Rental period
    start_date = models.DateField()
    end_date = models.DateField()

    # Current status of the rental
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    # When the request was made
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.renter.username} renting '{self.item.title}' [{self.status}]"

    def total_days(self):
        """Calculate how many days the rental covers."""
        delta = self.end_date - self.start_date
        return max(delta.days, 1)  # Minimum 1 day

    def total_cost(self):
        """Calculate total rental cost = daily_rate × number of days."""
        return self.item.daily_rate * self.total_days()
