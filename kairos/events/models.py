from django.db import models

# Create your models here.

# Note: Fields relate to specific form inputs
#       egs: TextField -> textarea, CharField -> input of type text 

class Event(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField() 
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True) # Date timestamp added every event creation

    def __str__(self):
        return self.title