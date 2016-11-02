from django.db import models


# Create your models here.
from django.utils import timezone


# Reference: http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Update timestamps on save
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(TimestampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Project(TimestampedModel):
    STATUS_CHOICES = (
        ('Not started', 'Not started'),
        ('In Progress', 'In Progress'),
        ('Halted', 'Halted'),
        ('Finished', 'Finished'),
        ('Abandonned', 'Abandonned')
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=40, choices=STATUS_CHOICES)


class ProjectProgress(TimestampedModel):
    notification_text = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
