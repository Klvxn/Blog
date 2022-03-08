from django.views import generic
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
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
        return BlogPost.objects.order_by('date_added')

@login_required
def create_post(request):
    """Creating a new post."""

    if request.User != request.user:
        raise Http404
    if request.method != 'POST':
        form = BlogForm()

    else:
        form = BlogForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.User = request.user
            new_post.save()
            return HttpResponseRedirect(reverse('blogs:index'))

    context = {'form': form}
    return render(request, 'blogs/create_post.html', context)


@login_required
def edit_post(request, post_id):
    """Editing an existing post."""
    post = BlogPost.objects.get(id=post_id)

    if request.method != 'POST':
        form = BlogForm(instance=post)

    else:
        form = BlogForm(instance=post, data=request.POST)
        if form.is_valid():

            form.save()
            
            return HttpResponseRedirect(reverse('blogs:index'))

    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)
