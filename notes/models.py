from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime,date

# Create your models here.
MAX_CATEGORY_LENGTH = 100
MAX_TITLE_LENGTH = 100
MAX_CONTACT_LENGTH = 100
MAX_NAME_LENGTH = 255 
MAX_EMAIL_LENGTH = 255 
MAX_URL_LENGTH = 255 

class Category(models.Model):
    name = models.CharField(max_length= MAX_CATEGORY_LENGTH, unique=True, blank=False)

    def __str__(self):
        return self.name
    

class Note(models.Model):
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    body = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=MAX_CATEGORY_LENGTH, default='')

    def __str__(self):
        return self.title + ' | ' + str(self.category)

    def get_absolute_url(self):
        return reverse('note-detail', kwargs={'pk': self.id})

class Bookmark(models.Model):
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    url = models.URLField(max_length=MAX_URL_LENGTH)
    created_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=MAX_CATEGORY_LENGTH, default='')
    description= models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    email = models.EmailField(max_length=MAX_EMAIL_LENGTH, null=True, blank=True)
    contact = models.CharField(max_length=MAX_CONTACT_LENGTH, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=MAX_CATEGORY_LENGTH, default='')
    
    def __str__(self):
        return self.name


class Map(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    description= models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='media')
    category = models.CharField(max_length=MAX_CATEGORY_LENGTH, default='')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name