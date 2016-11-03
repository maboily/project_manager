from django.conf.urls import url

from project_manager_web import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^projects/$', views.projects),
    url(r'^logout/$', views.do_logout)
]