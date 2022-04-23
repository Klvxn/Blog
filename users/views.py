from django.shortcuts import render, redirect
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def RegisterUser(request):
    """Register a new user."""
    if request.method == 'POST':
         # Process completed form
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in and redirect to homepage. 
            login(request, new_user)
            return redirect('blogs:index') 
    else:
        # Display blank registration form
        form = UserCreationForm()
    context = {'form':form}
    return render(request, 'registration/register.html', context)
