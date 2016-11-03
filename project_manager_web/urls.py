from django.conf.urls import url

from project_manager_web import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^projects/$', views.projects),
    url(r'^projects/add/$', views.add_project),
    url(r'^projects/(?P<project_id>\w+)/edit/$', views.edit_project),
    url(r'^logout/$', views.do_logout)
]