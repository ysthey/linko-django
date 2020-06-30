from django import forms
from .models import Post, Category, Bookmark, Contacts

choices = Category.objects.all().values_list('name','name')

choice_list = []

for item in choices:
    choice_list.append(item)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'category', 'body')
        widgets = {

        'title': forms.TextInput(attrs={'class': 'form-control rounded-0'}),
        'author': forms.Select(attrs={'class': 'form-control'}),
        'category': forms.Select(choices=choice_list, attrs={'class': 'form-control rounded-0'}),      
        'body': forms.Textarea(attrs={'class': 'form-control rounded-0'}),
        }

class LinkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ('title', 'url')
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control rounded-0'}),
        'url': forms.URLInput(attrs={'class': 'form-control rounded-0'}), 
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ('Name', 'Email', 'Contact', 'Note')
        widgets = {
        'Name': forms.TextInput(attrs={'class': 'form-control rounded-0'}),
        'Email': forms.TextInput(attrs={'class': 'form-control rounded-0'}), 
        'Contact': forms.TextInput(attrs={'class': 'form-control rounded-0'}),
        'Note': forms.TextInput(attrs={'class': 'form-control rounded-0'}),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'body')
        widgets = {

        'title': forms.TextInput(attrs={'class': 'form-control '}),
        'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),      
        'body': forms.Textarea(attrs={'class': 'form-control'}),
        
        }
