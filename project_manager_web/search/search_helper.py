from django.db.models import Count, CharField
from django.db.models import Value, IntegerField

from project_manager_web.models import Project


class SearchHelperResult:
    def __init__(self, project):
        self.project = project


class SearchHelper:
    SEARCH_IN_CHOICES = (
        ('name', 'Name'),
        ('description', 'Description'),
        ('progresses', 'Project Progresses'),
        ('name+description', 'Name and descriptions'),
        ('name+description+progresses', 'All')
    )

    def __init__(self, search_for, search_in):
        # Fills GET parameters
        self.search_for = search_for
        self.search_in = search_in.split('+')

    @property
    def find_results(self):
        results = None

        # Name search
        if 'name' in self.search_in:
            if results is None:
                results = Project.objects.filter(name__icontains=self.search_for)
            else:
                results |= Project.objects.filter(name__icontains=self.search_for)

        # Description search
        if 'description' in self.search_in:
            if results is None:
                results = Project.objects.filter(description__icontains=self.search_for)
            else:
                results |= Project.objects.filter(description__icontains=self.search_for)

        # Progresses search
        if 'progresses' in self.search_in:
            if results is None:
                results = Project.objects.filter(projectprogress__notification_text__icontains=self.search_for)
            else:
                results |= Project.objects.filter(projectprogress__notification_text__icontains=self.search_for)

        return results.all().values('name', 'description', 'id').distinct()
