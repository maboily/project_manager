from django.contrib import admin

# Register your models here.
from project_manager_web.models import Project, ProjectProgress

admin.site.register(Project)
admin.site.register(ProjectProgress)
