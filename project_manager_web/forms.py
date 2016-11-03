from django import forms

from project_manager_web.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'start_date', 'end_date']