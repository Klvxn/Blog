from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import BlogPost
from .forms import BlogForm, CommentForm


# Create your views here.
def IndexView(request):
    posts = BlogPost.objects.all().order_by('-date_added')
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'posts_list':page_obj, 'all_posts':posts}
    return render(request, 'blogs/index.html', context )


def PostDetail(request, pk):
    posts = get_object_or_404(BlogPost, pk=pk)
    comment_count = posts.comment_set.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)    
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            if posts.owner == request.user:
                new_comment.username = request.user
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
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs:index')
    context = {'form': form}
    return render(request, 'blogs/create_post.html', context)


@login_required(login_url='/registration/login/')
def edit_post(request, post_id):
    """Editing an existing post."""
    post = get_object_or_404(BlogPost, id=post_id)
    if post.owner != request.user:
        return HttpResponse('<h1> (ERROR) Access denied. </h1>')
    else:
        if request.method != 'POST':
            form = BlogForm(instance=post)
        else:
            form = BlogForm(instance=post, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('blogs:index')
    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)


@login_required(login_url='/registration/login/')
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.owner != request.user:
        return HttpResponse('<h1> (ERROR) Request denied. </h1>')
    else:
        if request.method == 'POST':
            post.delete()
            return redirect('blogs:index')
    context = {'post':post}
    return render (request, 'blogs/delete_post.html', context)
        