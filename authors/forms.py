from django import forms

from .models import Author


# Forms
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = (
            "user",
            "slug",
        )
