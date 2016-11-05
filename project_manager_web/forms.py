from django import forms

from project_manager_web.models import Project, ProjectProgress


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'start_date', 'end_date']


class ProjectProgressForm(forms.ModelForm):
    class Meta:
        model = ProjectProgress
        fields = ['notification_text']
