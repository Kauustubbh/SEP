"""
Forms for creating and editing items.
"""

from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    """Form for creating or editing an item listing."""

    class Meta:
        model = Item
        # 'owner' is set automatically in the view, not by the user
        fields = ['title', 'description', 'category', 'daily_rate', 'image', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
