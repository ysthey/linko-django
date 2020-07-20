from django.urls import path
from .views import FilesPage, searchlinks, searchcontacts, search, HomePage, HomeView, NotesDetailView, AddNoteView, UpdateNoteView, AddCategoryView, CategoryView, LinkView, AddLinkView, AddContactView,ContactsView, model_form_upload
from notes.forms import UserLoginForm
from django.contrib.auth import views

urlpatterns = [  
    path('', HomePage, name='homepage'),
    path('notes/', HomeView.as_view(), name="home"),
    path('notes/<int:pk>', NotesDetailView.as_view(), name='note-detail'),
    path('addnote/', AddNoteView.as_view(), name='add_note'),
    path('addcateogry/', AddCategoryView.as_view(), name='add_category'),
    path('notes/edit/<int:pk>', UpdateNoteView.as_view(), name='update-note'),
    path('category/<str:cats>/', CategoryView, name='category'),

    #bookmarks

    path('bookmarks/', LinkView.as_view(), name='bookmarks'),
    path('addbookmark/', AddLinkView.as_view(), name='add_link'),

    #contacts 
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('addcontact/', AddContactView.as_view(), name='add_contact'),

    path('search/', search , name='search'),
    path('searchbkms/', searchlinks , name='searchbkms'),
    path('searchcts/', searchcontacts , name='searchcts'),

    path('files/', FilesPage , name='filepage'),
    path('upload/', model_form_upload , name='uploads'),

     path('login/', views.LoginView.as_view(template_name="login.html",authentication_form=UserLoginForm), name='login')

]