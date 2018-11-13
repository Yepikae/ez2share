from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Repository
from .forms import PasswordForm

def upload(request, name):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PasswordForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            password = form['repository_password'].value()
            print(password)
            print(name)
            user = authenticate(username=name, password=password)
            if user is not None:
                return render(request, 'ez/upload.html', {})
            else:
                raise PermissionDenied

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordForm()
    return render(request,
                  'ez/ask_for_connection.html',
                  {'name': name, 'view': 'upload', 'form': form})
