from django.contrib import admin
from .models import Post, Category, Bookmark, Contacts
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Bookmark)
admin.site.register(Contacts)