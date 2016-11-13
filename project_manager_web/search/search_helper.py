from project_manager_web.models import Project


class SearchHelperResult:
    def __init__(self, project):
        self.project = project


class SearchHelper:
    SEARCH_IN_CHOICES = (
        ('name', 'Name'),
        ('description', 'Description'),
        ('name+description', 'Name and descriptions')
    )

    def __init__(self, search_for, search_in):
        # Fills GET parameters
        self.search_for = search_for
        self.search_in = search_in.split('+')

    def find_results(self):
        search_keywords = {}
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

        return results.all()
