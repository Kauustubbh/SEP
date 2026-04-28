"""
Form for creating a rental request.
"""

from django import forms
from .models import Rental


class RentalRequestForm(forms.ModelForm):
    """Form to request a rental - just need start and end dates."""

    class Meta:
        model = Rental
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        """Validate that end_date is after start_date."""
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and end:
            if end <= start:
                raise forms.ValidationError("End date must be after start date.")

        return cleaned_data
