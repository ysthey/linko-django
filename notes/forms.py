from django import forms
from .models import Post, Category, Bookmark, Contacts



def retList():
    choices = Category.objects.all().values_list('name','name')
    choice_list = []
    for item in choices:
        choice_list.append(item)
    return choice_list

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control rounded-1'}),
        }
    

class PostForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control rounded-1'}))
   
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

    class Meta:
        model = Post
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
        model = Contacts
        fields = ('Name', 'Email', 'Contact', 'Note')
        widgets = {
        'Name': forms.TextInput(attrs={'class': 'form-control rounded-1'}),
        'Email': forms.TextInput(attrs={'class': 'form-control rounded-1'}), 
        'Contact': forms.TextInput(attrs={'class': 'form-control rounded-1'}),
        'Note': forms.TextInput(attrs={'class': 'form-control rounded-1'}),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'body')
        widgets = {

        'title': forms.TextInput(attrs={'class': 'form-control '}),
        'category': forms.Select(choices=retList(), attrs={'class': 'form-control'}),      
        'body': forms.Textarea(attrs={'class': 'form-control'}),
        
        }
