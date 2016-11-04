from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render


# Create your views here.
from project_manager_web.forms import ProjectForm
from project_manager_web.models import Project


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())

            return HttpResponseRedirect('/projects/')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def do_logout(request):
    logout(request)

    return HttpResponseRedirect('/')


@login_required
def projects(request):
    projects = Project.objects.all

    return render(request, 'projects/index.html', {'projects': projects})


@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/projects/')
    else:
        form = ProjectForm()

    return render(request, 'projects/add.html', {'form': form})


@login_required
def view_project(request, project_id):
    project = Project.objects.get(pk=project_id)

    return render(request, 'projects/view.html', {'project': project})


@login_required
def edit_project(request, project_id):
    project = Project.objects.get(pk=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/projects/')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/edit.html', {'form': form})
