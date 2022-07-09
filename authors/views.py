from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from blogs.models import BlogPost

from .forms import AuthorForm
from .models import Author


# Create your views here.
def authors_list(request):
    """Viewing all authors page."""
    authors = Author.objects.all()
    template_name = "authors/authors_page.html"
    context = {"authors": authors}
    return render(request, template_name, context)


def author_detail(request, slug):
    """Viewing individual author's page."""
    author = get_object_or_404(Author, slug=slug)
    author_post = BlogPost.objects.filter(author=author)
    template_name = "authors/author_detail_page.html"
    context = {"author_posts": author_post, "author": author}
    return render(request, template_name, context)


@login_required
def become_author(request):
    """Applying to be an author."""
    if request.method == "POST":
        author_form = AuthorForm(request.POST, request.FILES)
        if author_form.is_valid():
            new_author = author_form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            return redirect(new_author)
    else:
        author_form = AuthorForm()
    template_name = "authors/become_author.html"
    context = {"form": author_form}
    return render(request, template_name, context)


@login_required
def edit_author_profile(request, slug):
    """Editing an author's profile."""
    author = get_object_or_404(Author, slug=slug)
    if request.user == author.user:
        if request.method == "POST":
            form = AuthorForm(instance=author, data=request.POST, files=request.FILES)
            if form.is_valid():
                edit = form.save()
                messages.success(request, "Changes saved.")
                return redirect(edit)
        else:
            form = AuthorForm(instance=author)
    else:
        return HttpResponseForbidden()
    template_name = "authors/author_edit_profile.html"
    context = {"form": form}
    return render(request, template_name, context)


def search_authors(request):
    """Searching for authors."""
    query = request.GET["query"]
    search_result = Author.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query)
    ).distinct()
    template_name = "authors/search_authors.html"
    context = {"searched": query, "search_result": search_result}
    return render(request, template_name, context)
