from  django import forms
from django.forms.models import model_to_dict

from .models import BlogPost


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text']
       
        