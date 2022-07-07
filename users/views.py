from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import RegisterUserForm


# Create your views here.
def RegisterUser(request):
    """Register a new user."""
    if request.method == "POST":
        form = RegisterUserForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("blogs:index")
    else:
        form = RegisterUserForm()
    context = {"form": form}
    return render(request, "registration/register.html", context)
