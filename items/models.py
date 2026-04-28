"""
Items app models.
An Item is something a user lists for rental.
"""

from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    """
    Represents a rental item listed by a user.
    """

    # Categories a user can choose from
    CATEGORY_CHOICES = [
        ('Tools', 'Tools'),
        ('Electronics', 'Electronics'),
        ('Books', 'Books'),
        ('Clothing', 'Clothing'),
        ('Other', 'Other'),
    ]

    # Who listed this item
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')

    # Price per day in rupees (integer keeps it simple)
    daily_rate = models.PositiveIntegerField(help_text="Price per day in ₹")

    # Optional image upload (stored in media/item_images/)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)

    # Is the item currently available for rent?
    available = models.BooleanField(default=True)

    # How many times has this item been rented and completed?
    usage_count = models.PositiveIntegerField(default=0)

    # When was this listing created?
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (by {self.owner.username})"
