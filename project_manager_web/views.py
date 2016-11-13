from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render


# Create your views here.
from project_manager_web.forms import ProjectForm, ProjectProgressForm
from project_manager_web.models import Project, ProjectProgress


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
            new_project = form.save()

            messages.add_message(request, messages.INFO, "Project '" + new_project.name + "' added.")
            return HttpResponseRedirect('/projects/')
    else:
        form = ProjectForm()

    return render(request, 'projects/add.html', {'form': form})


@login_required
def view_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    project_progresses = project.projectprogress_set.all().order_by('-date')

    return render(request, 'projects/view.html', {'project': project, 'project_progresses': project_progresses})


@login_required
def delete_project(request, project_id):
    project_to_delete = Project.objects.get(pk=project_id)
    project_to_delete.delete()

    messages.add_message(request, messages.INFO, "Project '" + project_to_delete.name + "' deleted.")
    return HttpResponseRedirect('/projects/')


@login_required
def edit_project(request, project_id):
    project = Project.objects.get(pk=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()

            messages.add_message(request, messages.INFO, "Project '" + project.name + "' saved.")
            return HttpResponseRedirect('/projects/')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/edit.html', {'form': form})


@login_required
def add_project_progress(request, project_id):
    if request.method == 'POST':
        form = ProjectProgressForm(request.POST)

        if form.is_valid():
            project_progress_instance = form.save(commit=False)
            project_progress_instance.project_id = project_id
            project_progress_instance.save()

            messages.add_message(request, messages.INFO, "New project progress added successfully.")
            return HttpResponseRedirect('/projects/' + project_id + '/')
    else:
        form = ProjectProgressForm()

    return render(request, 'projects/progresses/add.html', {'form': form})


@login_required
def delete_project_progress(request, project_id, project_progress_id):
    project_progress_to_delete = ProjectProgress.objects.get(id=project_progress_id, project_id=project_id)
    project_progress_to_delete.delete()

    messages.add_message(request, messages.INFO, "Project progress deleted.")
    return HttpResponseRedirect('/projects/' + project_id + '/')


@login_required
def edit_project_progress(request, project_id, project_progress_id):
    project_progress = ProjectProgress.objects.get(pk=project_progress_id)

    if request.method == 'POST':
        form = ProjectProgressForm(request.POST, instance=project_progress)

        if form.is_valid():
            form.save()

            messages.add_message(request, messages.INFO, "Project progress saved.")
            return HttpResponseRedirect('/projects/' + project_id + '/')
    else:
        form = ProjectProgressForm(instance=project_progress)

    return render(request, 'projects/progresses/edit.html', {'form': form})


def polymer_date_picker(request):
    return render(request, 'polymer/date-picker.html')
