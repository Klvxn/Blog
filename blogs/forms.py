from  django import forms

from .models import Author, BlogPost, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ('user',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['username', 'text']

       
        