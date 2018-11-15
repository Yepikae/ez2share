from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Repository, Files
from .forms import PasswordForm, RepoForm, FileFieldForm
from django.views.generic.edit import FormView
from django import forms
import time
import os
import zipfile
from io import BytesIO


def upload(request, name):
    context = {}
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
            user = authenticate(username=name, password=password)
            if user is not None:
                login(request, user)
                form = FileFieldForm()
                return render(request, 'ez/upload.html', {'form': form})
            else:
                context['form'] = PasswordForm()
                context['error_message'] = 'Password incorrect.'

    # if a GET (or any other method) we'll create a blank form
    else:
        context['form'] = PasswordForm()
    context['name'] = name
    context['view'] = 'upload'
    return render(request, 'ez/ask_for_connection.html', context)

def upload_files(request):
    user = request.user
    if not user.is_authenticated:
        raise PermissionDenied
    else:
        logout(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FileFieldForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # Save the files & return json
            files = request.FILES.getlist('file_field')
            repository = Repository.objects.get(owner=user)
            for file in files:
                f = Files(repository=repository, file=file)
                f.save()
            return JsonResponse({'success': True})
        else:
            raise PermissionDenied
    # if a GET (or any other method) we'll create a blank form
    else:
        raise PermissionDenied

def ask_for_repo(request, view='upload'):
    context = {}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RepoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            repo_name = form['repository_name'].value()
            try:
                Repository.objects.get(owner__username=repo_name)
                return HttpResponseRedirect(repo_name)
            except Repository.DoesNotExist:
                context['error_message'] = 'Repository does not exist.'

    # if a GET (or any other method) we'll create a blank form
    context['form'] = RepoForm()
    context['view'] = view
    return render(request, 'ez/ask_for_repo.html', context)

def upload_complete(request):
    return render(request, 'ez/upload_complete.html', {})

def download(request, name):
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
            user = authenticate(username=name, password=password)
            if user is not None:
                login(request, user)
                repository = Repository.objects.get(owner=user)
                raw_files = Files.objects.filter(repository=repository)
                files = []
                for file in raw_files:
                    files.append((file.id, file.filename))
                return render(request, 'ez/download.html', {'files': files})
            else:
                raise PermissionDenied

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordForm()
    return render(request,
                  'ez/ask_for_connection.html',
                  {'name': name, 'view': 'download', 'form': form})

def download_files(request):
    user = request.user
    if not user.is_authenticated:
        raise PermissionDenied
    else:
        logout(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        download_ids = request.POST.getlist('download')

        stream = BytesIO()
        temp_zip_file = zipfile.ZipFile(stream, mode='w')
        for id in download_ids:
            file = Files.objects.get(pk=id)
            path = str(file.file)
            name = file.filename
            temp_zip_file.write(path, arcname=name)
        temp_zip_file.close()
        response = HttpResponse(stream.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="'+user.username+'.zip"'
        return response
    # if a GET (or any other method) we'll create a blank form
    else:
        raise PermissionDenied
