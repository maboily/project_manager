from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render


# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from project_manager_web.forms import ProjectForm, ProjectProgressForm, SearchForm
from project_manager_web.models import Project, ProjectProgress
from project_manager_web.search.search_helper import SearchHelper


class HomeView(TemplateView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, self.template_name, {
                'form': self.form_class()
            })

    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            form = self.form_class(data=request.POST)

            if form.is_valid():
                login(request, form.get_user())

                return HttpResponseRedirect(reverse('projects.index'))
            else:
                return render(request, self.template_name, {
                    'form': form
                })


class LogoutView(TemplateView):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse('home'))


@login_required
def projects(request):
    projects_list = Project.objects.all()

    paginator = Paginator(projects_list, 10)
    page = request.GET.get('project_page')
    try:
        projects_obj = paginator.page(page)
    except PageNotAnInteger:
        projects_obj = paginator.page(1)
    except EmptyPage:
        projects_obj = paginator.page(paginator.num_pages)

    return render(request, 'projects/index.html', {'projects': projects_obj})


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
    project_progresses_list = project.projectprogress_set.all().order_by('-date')

    paginator = Paginator(project_progresses_list, 5)
    page = request.GET.get('progress_page')
    try:
        project_progresses = paginator.page(page)
    except PageNotAnInteger:
        project_progresses = paginator.page(1)
    except EmptyPage:
        project_progresses = paginator.page(paginator.num_pages)

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


@login_required
def search_project(request):
    if request.GET.get('search_text') is not None and request.GET.get('search_in') is not None:
        form = SearchForm(request.GET)

        helper_instance = SearchHelper(search_for=form.data['search_text'], search_in=form.data['search_in'])
        results_list = helper_instance.find_results()

        paginator = Paginator(results_list, 10)
        page = request.GET.get('search_page')
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
    else:
        form = SearchForm()
        results = None

    return render(request, 'projects/search.html', {'form': form, 'results': results})
