"""
Forms for the users app.
Registration form combines User fields + Profile fields.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegisterForm(UserCreationForm):
    """
    Registration form.
    Inherits username + password fields from UserCreationForm.
    Adds email and community_name fields.
    """
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")
    community_name = forms.CharField(
        max_length=100,
        required=False,
        help_text="E.g., North Campus, Block A"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        """Save user and create their Profile automatically."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create profile linked to this user
            Profile.objects.create(
                user=user,
                community_name=self.cleaned_data.get('community_name', '')
            )
        return user
