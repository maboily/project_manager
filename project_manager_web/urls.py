from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from project_manager_web import views
from project_manager_web.views import HomeView, LogoutView

project_progresses_patterns = [
    url(r'^progresses/add', views.add_project_progress, name='projects.progresses.add'),
    url(r'^progresses/delete/(?P<project_progress_id>\w+)', views.delete_project_progress, name='projects.progresses.delete'),
    url(r'^progresses/edit/(?P<project_progress_id>\w+)', views.edit_project_progress, name='projects.progresses.edit'),
]

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^projects/$', views.projects, name='projects.index'),
    url(r'^projects/add/$', views.add_project, name='projects.add'),
    url(r'^projects/search/$', views.search_project, name='projects.search'),
    url(r'^projects/(?P<project_id>\w+)/$', views.view_project, name='projects.view'),
    url(r'^projects/(?P<project_id>\w+)/', include(project_progresses_patterns)),
    url(r'^projects/delete/(?P<project_id>\w+)/$', views.delete_project, name='projects.delete'),
    url(r'^projects/edit/(?P<project_id>\w+)/$', views.edit_project, name='projects.edit'),
    url(r'^logout/$', LogoutView.as_view(), name='logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
