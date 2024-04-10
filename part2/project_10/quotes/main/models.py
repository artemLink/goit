from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=255)
    born_date = models.DateField()
    born_location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.fullname

class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()
    tags = models.JSONField()
