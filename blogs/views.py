from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.text import slugify
from django.contrib import messages

from .models import BlogPost, Author
from .forms import AuthorForm, BlogForm, CommentForm


# Create your views here.
def IndexView(request):
    """Home page"""
    posts = BlogPost.objects.all().order_by("-date_added")
    authors = Author.objects.all()
    paginator = Paginator(posts, 11)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    template_name = "blogs/index.html"
    context = {"posts_list": page_obj, "all_posts": posts[:5], "authors": authors}
    return render(request, template_name, context)


def PostDetail(request, slug, pk):
    """Viewing an individual post and it's comments."""
    posts = get_object_or_404(BlogPost, slug=slug, pk=pk)
    comment_count = posts.comment_set.all()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = posts
            new_comment.save()
            return redirect(posts)
    else:
        comment_form = CommentForm()
    template_name = "blogs/post_detail.html"
    context = {"form": comment_form, "posts": posts, "comment_count": comment_count}
    return render(request, template_name, context)


@login_required
def create_post(request):
    """Creating a new post."""
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(new_post.title)
            if hasattr(request.user, "author"):
                author = get_object_or_404(Author, user=request.user)
                new_post.author = author
                new_post.save()
                messages.success(request, "Your post was submitted successfully.")
                return redirect("blogs:index")
            else:
                template_name = "blogs/not_author_error.html"
                return render(request, template_name)
    else:
        if not hasattr(request.user, "author"):
            messages.warning(
                request,
                "You are not an author! Only verified authors can create a post.",
            )
        form = BlogForm()
    template_name = "blogs/create_post.html"
    context = {"form": form}
    return render(request, template_name, context)


@login_required
def edit_post(request, slug, pk):
    """Editing an existing post."""
    post = get_object_or_404(BlogPost, slug=slug, pk=pk)
    if post.author.user == request.user:
        if request.method == "POST":
            form = BlogForm(instance=post, data=request.POST)
            if form.is_valid():
                edit = form.save(commit=False)
                edit.slug = slugify(edit.title)
                edit.save()
                return redirect(edit)
        else:
            form = BlogForm(instance=post)
    else:
        return HttpResponseForbidden()
    template_name = "blogs/edit_post.html"
    context = {"post": post, "form": form}
    return render(request, template_name, context)


@login_required
def delete_post(request, slug, pk):
    """Deleting an existing post."""
    post = get_object_or_404(BlogPost, slug=slug, pk=pk)
    if post.author.user == request.user:
        if request.method == "POST":
            post.delete()
            return redirect("blogs:index")
    else:
        return HttpResponseForbidden()
    template_name = "blogs/delete_post.html"
    context = {"post": post}
    return render(request, template_name, context)


def search(request):
    """Searching for post or an author."""
    query = request.GET["query"]
    search_post_result = BlogPost.objects.filter(
        Q(title__icontains=query) | Q(text__icontains=query)
    ).distinct()
    search_author_result = Author.objects.filter(
        Q(firstname__icontains=query) | Q(lastname__icontains=query)
    ).distinct()
    template_name = "blogs/search.html"
    context = {
        "search": search_post_result,
        "searched": query,
        "search_author": search_author_result,
    }
    return render(request, template_name, context)


def authors(request):
    """Viewing all authors page."""
    authors = Author.objects.all()
    template_name = "blogs/authorspage.html"
    context = {"authors": authors}
    return render(request, template_name, context)


def author(request, firstname, lastname):
    """Viewing individual author's page."""
    author = get_object_or_404(Author, firstname=firstname, lastname=lastname)
    author_post = BlogPost.objects.filter(author=author)
    template_name = "blogs/authorpage.html"
    context = {"author_posts": author_post, "author": author}
    return render(request, template_name, context)


@login_required
def beauthor(request):
    """Applying to be an author."""
    if request.method == "POST":
        author_form = AuthorForm(request.POST)
        if author_form.is_valid():
            new_author = author_form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            return redirect(new_author)
    else:
        author_form = AuthorForm()
    template_name = "blogs/becomeauthor.html"
    context = {"form": author_form}
    return render(request, template_name, context)


@login_required
def edit_author_profile(request, firstname, lastname):
    """Editing an author's profile."""
    author = get_object_or_404(Author, firstname=firstname, lastname=lastname)
    if author.user == request.user:
        if request.method == "POST":
            edit_form = AuthorForm(instance=author, data=request.POST)
            if edit_form.is_valid():
                edit = edit_form.save()
                messages.success(request, "`Changes saved.` -")
                return redirect(edit)
        else:
            edit_form = AuthorForm(instance=author)
    else:
        return HttpResponseForbidden()
    template_name = "blogs/author_edit_profile.html"
    context = {"form": edit_form}
    return render(request, template_name, context)
