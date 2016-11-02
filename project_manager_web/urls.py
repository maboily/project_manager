from django.conf.urls import url

from project_manager_web import views

urlpatterns = [
    url(r'^$', views.home),
]