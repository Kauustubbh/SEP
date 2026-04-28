"""
Users app models.
We extend Django's built-in User model with a Profile model.
This keeps auth simple while adding community-specific fields.
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Extends the built-in User model with extra fields.
    One Profile exists per User (OneToOneField).
    """
    # Link to Django's built-in User (login, password, email handled there)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Trust score: a simple reputation metric (default 5.0 out of 10)
    trust_score = models.FloatField(default=5.0)

    # Community name: e.g., "North Campus", "Engineering Block"
    community_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
