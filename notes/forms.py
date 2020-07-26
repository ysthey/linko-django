from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Note, Category, Bookmark, Contact, Map

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control rounded-1'}),
        }
    

class NoteForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control rounded-1'}))
   
    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

    class Meta:
        model = Note
        fields = ('title', 'category', 'body')
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control rounded-1'}),  
        'body': forms.Textarea(attrs={'class': 'form-control rounded-1'}),
        }

class LinkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ('title', 'url')
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control rounded-1'}),
        'url': forms.URLInput(attrs={'class': 'form-control rounded-1'}), 
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'contact', 'note')
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control rounded-1'}),
        'email': forms.TextInput(attrs={'class': 'form-control rounded-1'}), 
        'contact': forms.TextInput(attrs={'class': 'form-control rounded-1'}),
        'note': forms.TextInput(attrs={'class': 'form-control rounded-1'}),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Note 
        fields = ('title', 'category', 'body')
        widgets = {

        'title': forms.TextInput(attrs={'class': 'form-control '}),
        'category': forms.Select(attrs={'class': 'form-control'}),      
        'body': forms.Textarea(attrs={'class': 'form-control'}),
        
        }

class UploadForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control rounded-1'}))
    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
    class Meta:
        model = Map
        fields = ('name', 'description', 'category', 'file')
        widgets = {

        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.TextInput(attrs={'class': 'form-control'}),
        'category': forms.Select(attrs={'class': 'form-control'}),      
        'file': forms.FileInput(), 
    
    }

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    widgets = {

        'username': forms.TextInput(attrs={'class': 'form-control'}),
        'password': forms.PasswordInput(attrs={'class': 'form-control',}), 
    
    }
    