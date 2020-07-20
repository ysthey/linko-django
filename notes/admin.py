from django.contrib import admin
from .models import Post, Category, Bookmark, Contacts, Map
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Bookmark)
admin.site.register(Contacts)
admin.site.register(Map)