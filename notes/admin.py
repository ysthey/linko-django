from django.contrib import admin
from .models import Note, Category, Bookmark, Contact, Map
# Register your models here.

admin.site.register(Note)
admin.site.register(Category)
admin.site.register(Bookmark)
admin.site.register(Contact)
admin.site.register(Map)