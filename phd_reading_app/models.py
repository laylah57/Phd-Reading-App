from django.db import models

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class ReadingItem(models.Model):
    title = models.CharField(max_length=30)
    subtitle = models.CharField(max_length=30)
    year_published = models.DateField()
    created_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
