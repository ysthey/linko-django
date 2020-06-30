from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime,date

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')
    

class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255, default='tax-returns')

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('home')

class Bookmark(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=250)
    created_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255, default='none')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')

class Contacts(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=254, null=True, blank=True)
    Contact = models.CharField(max_length=100, null=True, blank=True)
    Note = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('home')

    