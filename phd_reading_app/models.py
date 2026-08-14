from django.db import models

# Create your models here.
class Status(models.TextChoices):
    TO_READ = 'to_read', 'To Read'
    READING = 'reading', 'Reading'
    COMPLETED = 'completed', 'Completed'
    ABANDONED = 'abandoned', 'Abandoned'

class ReadingItem(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150, blank=True)
    type = models.CharField(max_length=30, blank=True)
    year_published = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.TO_READ,
    )
    tags = models.ManyToManyField('Tag', blank=True)
    authors = models.ManyToManyField('Author')

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
