from django import forms
from .models import User


class InviteUserForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'user-selector'}),
        required=False,
    )