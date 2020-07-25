from django.urls import path
from django.conf.urls  import url, include
from .views import download_clone,check_archive_status,CloneView, CategoryViewSet, CategoryFilesView, download_file, searchfiles, FilesView, searchlinks, searchcontacts, search, HomePage, HomeView, NotesDetailView, AddNoteView, UpdateNoteView, AddCategoryView, CategoryView, LinkView, AddLinkView, AddContactView,ContactsView, model_form_upload
from notes.forms import UserLoginForm
from django.contrib.auth import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'categoryapi', CategoryViewSet)

urlpatterns = [  
    path('', HomePage, name='homepage'),
    path('notes/', HomeView.as_view(), name="home"),
    path('notes/<int:pk>', NotesDetailView.as_view(), name='note-detail'),
    path('addnote/', AddNoteView.as_view(), name='add_note'),
    path('addcateogry/', AddCategoryView.as_view(), name='add_category'),
    path('notes/edit/<int:pk>', UpdateNoteView.as_view(), name='update-note'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('categoryfiles/<str:cats>/', CategoryFilesView, name='categoryfiles'),
    url(r'^', include(router.urls), name="categoryapi"),

    #bookmarks

    path('bookmarks/', LinkView.as_view(), name='bookmarks'),
    path('addbookmark/', AddLinkView.as_view(), name='add_link'),

    #contacts 
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('addcontact/', AddContactView.as_view(), name='add_contact'),

    path('search/', search , name='search'),
    path('searchbkms/', searchlinks , name='searchbkms'),
    path('searchcts/', searchcontacts , name='searchcts'),
    path('searchfiles/', searchfiles, name='searchfiles'),

    #files
    path('files/', FilesView.as_view(), name='files'),
    path('upload/', model_form_upload , name='uploads'),
    path('download/<int:pk>', download_file, name='download'),
    path('clone/', CloneView, name='clone'),
    path('check_archive_status/', check_archive_status, name='check_archive_status'),
    path('download_clone', download_clone, name='download_clone'),

    path('login/', views.LoginView.as_view(template_name="login.html",authentication_form=UserLoginForm), name='login')

]