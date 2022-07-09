from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from authors.models import Author

from .forms import BlogForm, CommentForm
from .models import BlogPost


# Create your views here.
def index_view(request):
    """Home page"""
    posts = BlogPost.objects.all().order_by("-date_added")
    authors = Author.objects.all()
    paginator = Paginator(posts, 11)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    template_name = "blogs/index.html"
    context = {"posts_list": page_obj, "recent_posts": posts[:7], "authors": authors}
    return render(request, template_name, context)


def post_detail(request, slug, pk):
    """Viewing an individual post and it's comments."""
    post = get_object_or_404(BlogPost, slug=slug, pk=pk)
    comment_count = post.comment_set.all()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(post)
    else:
        comment_form = CommentForm()
    template_name = "blogs/post_detail.html"
    context = {"form": comment_form, "post": post, "comment_count": comment_count}
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
        if not hasattr(request.user, "author"):
            messages.warning(
                request,
                "You are not a verified author. Only verified authors can create a post.",
            )
        form = BlogForm()
    template_name = "blogs/create_post.html"
    context = {"form": form}
    return render(request, template_name, context)


@login_required
def edit_post(request, slug, pk):
    """Editing an existing post."""
    post = get_object_or_404(BlogPost, slug=slug, pk=pk)
    if request.user.is_superuser or post.author.user == request.user:
        if request.method == "POST":
            form = BlogForm(instance=post, data=request.POST)
            if form.is_valid():
                edit = form.save(commit=False)
                edit.slug = slugify(edit.title)
                edit.save()
                messages.success(request, "Post updated successfully.")
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
    if request.user.is_superuser or post.author.user == request.user:
        if request.method == "POST":
            post.delete()
            return redirect("blogs:index")
    else:
        return HttpResponseForbidden()
    template_name = "blogs/delete_post.html"
    context = {"post": post}
    return render(request, template_name, context)


def search_posts(request):
    """Searching for posts."""
    query = request.GET["query"]
    search_post_result = BlogPost.objects.filter(
        Q(title__icontains=query) | Q(text__icontains=query)
    ).distinct()
    template_name = "blogs/search_posts.html"
    context = {"search": search_post_result, "searched": query}
    return render(request, template_name, context)
