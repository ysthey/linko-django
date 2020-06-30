from django.shortcuts import render
import string
import django.utils.text
from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Category, Bookmark, Contacts
from .forms import PostForm, UpdateForm, LinkForm, ContactForm

# Create your views here.

def HomePage(request):
    return render(request, "homepage.html")

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-created_date']
    paginate_by = 10

    def get_context_data(self,*args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

class LinkView(ListView):
    model = Bookmark
    template_name = 'bookmarks.html'
    ordering = ['-created_date']
    paginate_by = 10

class ContactsView(ListView):
    model = Contacts
    template_name = 'contacts.html'
    ordering = ['-created_date']
    paginate_by = 10

class NotesDetailView(DetailView):
    model = Post
    template_name = 'note_details.html'

class AddNoteView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_note.html'
    #fields = '__all__'

class AddLinkView(CreateView):
    model = Bookmark
    form_class = LinkForm
    template_name = 'addbookmark.html'

    def get_success_url(self):
        return reverse('bookmarks')

class AddContactView(CreateView):
    model = Contacts
    form_class = ContactForm
    template_name = 'addcontact.html'

    def get_success_url(self):
        return reverse('contacts')

class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'

class UpdateNoteView(UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = 'update_note.html'
    #fields = ['title', 'body']

def CategoryView(request, cats):
    category_notes = Post.objects.filter(category=cats.replace(" ", "-"))

    return render(request, 'categories.html', {'cats':cats.title().replace("-", " "), 'category_notes':category_notes})


def search(request):
    search = request.GET['search']
    object_list = Post.objects.filter(title__icontains=search)
    params = {'object_list': object_list}
    return render(request, 'search.html', params)