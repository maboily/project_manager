from django import forms
from django.forms import models

from project_manager_web.models import Project, ProjectProgress
from project_manager_web.search.search_helper import SearchHelper
from project_manager_web.widgets import CustomVueDatePickerInput


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'start_date', 'end_date']


class ProjectProgressForm(forms.ModelForm):
    class Meta:
        model = ProjectProgress
        fields = ['notification_text', 'date']
        widgets = {
            "date": CustomVueDatePickerInput()
        }


class SearchForm(forms.Form):
    search_text = forms.CharField(label='Search text')
    search_in = forms.ChoiceField(label='Search in', choices=SearchHelper.SEARCH_IN_CHOICES)
