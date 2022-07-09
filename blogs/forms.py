from django import forms

from .models import BlogPost, Comment


# Forms
class BlogForm(forms.ModelForm):
    source = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={"placeholder": "Link to post source."}),
    )

    class Meta:
        model = BlogPost
        fields = ["title", "text", "source"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["username", "text"]
