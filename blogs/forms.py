from  django import forms
from django.shortcuts import get_object_or_404
from .models import Author, BlogPost, Comment


class BlogForm(forms.ModelForm):
    source = forms.URLField(required=False, widget=forms.URLInput(attrs={'placeholder':'Link to post source.'}))
    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'source']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ('user',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['username', 'text']

       
        