from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.text import slugify
from django.contrib.auth.models import User
from .models import BlogPost, Author
from .forms import AuthorForm, BlogForm, CommentForm


# Create your views here.
def IndexView(request):
    posts = BlogPost.objects.all().order_by('-date_added')
    authors = Author.objects.all()
    paginator = Paginator(posts, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts_list':page_obj,
        'all_posts':posts,
        'authors': authors}
    return render(request, 'blogs/index.html', context )


def PostDetail(request, slug):
    posts = get_object_or_404(BlogPost, slug=slug)
    comment_count = posts.comment_set.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)    
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = posts
            new_comment.save()
            return redirect(posts)
    else:
        comment_form = CommentForm()
    context = {'form':comment_form, 'posts':posts, 'comment_count':comment_count}
    return render(request, "blogs/post_detail.html", context)


@login_required(login_url='/registration/login')
def create_post(request):
    """Creating a new post."""
    if request.method != 'POST':
        form = BlogForm()
    else:
        form = BlogForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(new_post.title)
            author = Author(user=request.user,)
            new_post.author = author.user
            new_post.save()
            return redirect('blogs:index')
    context = {'form': form}
    return render(request, 'blogs/create_post.html', context)


@login_required(login_url='/registration/login/')
def edit_post(request, slug):
    """Editing an existing post."""
    post = get_object_or_404(BlogPost, slug=slug)
    if post.author.user == request.user:
        if request.method == 'POST':
            form = BlogForm(instance=post, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('blogs:index')    
        else:
            form = BlogForm(instance=post)
    else:
        return HttpResponse('<h1> (ERROR) Access denied. </h1>')
    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)


@login_required(login_url='/registration/login/')
def delete_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if post.author.user == request.user:
        if request.method == 'POST':
            post.delete()
            return redirect('blogs:index')
    else:
        return HttpResponse('<h1> (ERROR) Request denied. </h1>')
    context = {'post':post}
    return render (request, 'blogs/delete_post.html', context)
        
        
def authors(request):
    authors = Author.objects.all()
    context = {'authors':authors}
    return render(request, 'blogs/authorspage.html', context)


def author(request, firstname, lastname):
    author = get_object_or_404(Author, firstname=firstname, lastname=lastname)
    author_post = BlogPost.objects.filter(author=author)
    context = {
        'author_posts':author_post,
        'author':author }
    return render(request, 'blogs/authorpage.html', context)


@login_required(login_url='/registration/login/')
def beauthor(request):
    if request.method == "POST":
        author_form = AuthorForm(request.POST)
        if author_form.is_valid():
            new_author = author_form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            return redirect(new_author)
    else:
        author_form = AuthorForm()
    context = {'form':author_form}
    return render(request, 'blogs/becomeauthor.html', context)


def search(request):
    query = request.GET['query']
    search_post_result = BlogPost.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
    search_author_result = Author.objects.filter(Q(firstname__contains=query) | Q(lastname__contains=query))
    context={'search':search_post_result, 'searched':query, 'search_author':search_author_result}
    return render(request, 'blogs/search.html', context )
