from django.shortcuts import render
import string
import django.utils.text
from rest_framework import viewsets
from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Note, Category, Bookmark, Contact, Map
from .forms import NoteForm, UpdateForm, LinkForm, ContactForm, CategoryForm, UploadForm
from .serializers import CategorySerializer
from django.db.models.functions import Length, Upper, Lower
from django.shortcuts import redirect
from django.http import HttpResponseNotFound,HttpResponse, JsonResponse
from .archive_manager import ArchiveManager
import os
import urllib

import mimetypes

# Create your views here.

def HomePage(request):
    return render(request, "homepage.html")


class HomeView(ListView):    
    model = Note 
    template_name = 'home.html'
    ordering = [Lower('category')]
    paginate_by = 10

    def get_context_data(self,*args, **kwargs):
        cat_menu = Category.objects.all()       
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

class FilesView(ListView):    
    model = Map
    template_name = 'files.html'
    ordering = [Lower('name')]
    paginate_by = 10



class LinkView(ListView):
    model = Bookmark
    template_name = 'bookmarks.html'
    ordering = [Lower('title')]
    paginate_by = 10

class ContactsView(ListView):
    model = Contact
    template_name = 'contacts.html'
    ordering = [Lower('name')]
    paginate_by = 10

class NotesDetailView(DetailView):
    model = Note 
    template_name = 'note_details.html'

class AddNoteView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'add_note.html'
    #fields = '__all__'

class AddLinkView(CreateView):
    model = Bookmark
    form_class = LinkForm
    template_name = 'addbookmark.html'

    def get_success_url(self):
        return reverse('bookmarks')

class AddContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'addcontact.html'

    def get_success_url(self):
        return reverse('contacts')

class AddCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'add_category.html'
    

class UpdateNoteView(UpdateView):
    model = Note
    form_class = UpdateForm
    template_name = 'update_note.html'
    #fields = ['title', 'body']



def CloneView(request, cats='all'):

    bookmarks = Bookmark.objects.all().order_by('title')

    contacts = Contact.objects.all().order_by('name')

    notes = Note.objects.all().order_by('title')

    if cats != 'all':
        files = Map.objects.filter(category=cats.replace('-', ' ')).order_by('name')
    else:
        files = Map.objects.all().order_by('name')

    ArchiveManager.get_instance().archive(files, notes, bookmarks, contacts, cats)
    return render(request, 'clone.html', {"category": cats})

def check_archive_status(request,cats='all'):
    result = {"ready": not ArchiveManager.get_instance().is_archiving(cats)}
    return  JsonResponse(result)

def download_clone(request,cats='all'):
    # fill these variables with real values
    fl_path = ArchiveManager.get_instance().get_clone_file(cats)
    if fl_path == None:
        return HttpResponseNotFound()

    filename = os.path.basename(fl_path)

    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def CategoryView(request, cats):
    category_notes = Note.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html', {'title':cats.title().replace('-', ' '), 'category_notes':category_notes,'cats':cats})


def CategoryFilesView(request, cats):
    category_files = Map.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categoriesfiles.html', {'title':cats.title().replace('-', ' '), 'category_files':category_files, 'cats':cats})

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer




def search(request):
    search = request.GET['search']
    object_list = Note.objects.filter(Q(title__icontains=search) | Q(category__icontains=search))
    params = {'object_list': object_list}
    return render(request, 'search.html', params)

def searchlinks(request):
    search = request.GET['search']
    object_list = Bookmark.objects.filter(Q(url__icontains=search) | Q(title__icontains=search))
    params = {'object_list': object_list}
    return render(request, 'searchbkms.html', params)

def searchcontacts(request):
    search = request.GET['search']
    object_list = Contact.objects.filter(Q(email__icontains=search) | Q(name__icontains=search))
    params = {'object_list': object_list}
    return render(request, 'searchcts.html', params)

def searchfiles(request):
    search = request.GET['search']
    object_list = Map.objects.filter(Q(name__icontains=search) | Q(category__icontains=search)  | Q(description__icontains=search))
    params = {'object_list': object_list}
    return render(request, 'searchfiles.html', params)


def model_form_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('files')
    else:
        form = UploadForm()
    return render(request, 'form_upload.html', {
        'form': form
    })

def download_file(request, pk=0):
    # fill these variables with real values
    myfile = Map.objects.get(pk=int(pk))
    fl_path = urllib.parse.unquote(myfile.file.url,encoding='utf8')
    
    filename = os.path.basename(myfile.file.url)

    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response