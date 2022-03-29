from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import BlogPost
from .forms import BlogForm


# Create your views here.
class IndexView(generic.ListView):
    model = BlogPost
    context_object_name = 'all_posts_list'
    template_name = 'blogs/index.html'

    def get_queryset(self):
        return BlogPost.objects.order_by('-date_added')


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
            return HttpResponseRedirect(reverse('blogs:index'))

    context = {'form': form}
    return render(request, 'blogs/create_post.html', context)


@login_required(login_url='/registration/login/')
def edit_post(request, post_id):
    """Editing an existing post."""
    post = BlogPost.objects.get(id=post_id)
    if post.owner != request.user:
        return HttpResponse('Access denied. You can\'t ')
    else:
        if request.method != 'POST':
            form = BlogForm(instance=post)
        else:
            form = BlogForm(instance=post, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('blogs:index'))
        
    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)


@login_required(login_url='/registration/login/')
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.owner != request.user:
        return HttpResponse('Request Denied')
    else:
        if request.method == 'POST':
            post.delete()
            return redirect('blogs:index')

    context = {'post':post}
    return render (request, 'blogs/delete_post.html', context)