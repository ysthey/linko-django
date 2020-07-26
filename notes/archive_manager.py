import multiprocessing as mp
import urllib
import zipfile
import os
from concurrent.futures import ThreadPoolExecutor
from django.template.loader import render_to_string
import threading
import glob
homepage_links = {
    'home':'./index.html',
    'notes':'./html/notes.html',
    'bookmarks':'./html/bookmarks.html',
    'contacts':'./html/contacts.html',
    'files':'./html/files.html',
    'scripts':'./scripts',
    'images':'./images',
    }
subpage_links = {
    'home':'../index.html',
    'notes':'./notes.html',
    'bookmarks':'./bookmarks.html',
    'contacts':'./contacts.html',
    'files':'./files.html',
    'scripts':'../scripts',
    'images':'../images',
    }
subsubpage_links = {
    'home':'../../index.html',
    'notes':'../notes.html',
    'bookmarks':'../bookmarks.html',
    'contacts':'../contacts.html',
    'files':'../files.html',
    'scripts':'../../scripts',
    'images':'../../images',
    }



class IsRunningMap:
    def __init__(self):
        self.map = {}
    def is_running(self,k):
        isrunning = False
        m = self.map
        if k in m:
            isrunning = m[k]
        else:
            isrunning = False
        return isrunning

    def attempt_run(self, k):
        succeed = False
        m = self.map
        if k in m:
            if m[k] != True:
                m[k] = True
                succeed = True
        else:
            m[k] = True
            succeed = True
        return succeed

    def attempt_stop(self, k):
        succeed = False
        m = self.map
        if k in m:
            if m[k] == True:
                m[k] = False
                succeed = True
        return succeed




class ArchivedFile:
    def __init__(self, name, category, description, path):
        self.name = name
        self.path = path
        self.description = description
        self.category = category
    def basename(self):
        return os.path.basename(self.path)

class ArchivedNote:
    def __init__(self, title, category, body, created_date, path):
        self.title= title
        self.body= body
        self.created_date = created_date
        self.category = category
        self.path = path

class ArchivedLink:
    def __init__(self, title, category, url, created_date ):
        self.title = title
        self.url = url
        self.created_date = created_date
        self.category = category

class ArchivedContact:
    def __init__(self, name, email, contact, note, created_date, category):
        self.name = name
        self.email = email
        self.contact = contact
        self.note = note
        self.created_date = created_date
        self.category = category






class ArchiveManager:
    __instance = None
    __executor = ThreadPoolExecutor(max_workers=mp.cpu_count())
    ARCH_ROOT = './archives'
    ARCH_TEMP = os.path.join(ARCH_ROOT, 'temp')
    FNAME_TMPL = "archive_{}.zip"
    FILES_HTML = "html/files.html"
    CATS_FILES_HTML = "html/files_{}.html"
    CATS_NOTES_HTML = "html/notes_{}.html"
    CATS_LINKS_HTML = "html/links_{}.html"
    CATS_CONTACTS_HTML = "html/contacts_{}.html"
    NOTES_HTML = "html/notes.html"
    NOTE_HTML = "html/notes/note_{}.html"
    BOOKMARKS_HTML = "html/bookmarks.html"
    CONTACTS_HTML = "html/contacts.html"
    HOME_HTML = "index.html"
    __is_running_map = IsRunningMap()
    __lock = threading.Lock()

    @staticmethod 
    def get_instance():
        """ Static access method. """
        if ArchiveManager.__instance == None:
            ArchiveManager()
        return ArchiveManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if ArchiveManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ArchiveManager.__instance = self

    def archive(self, file_records, notes, bookmarks,contacts, cat='all'):
        ok = False
        with self.__lock:
            if self.__is_running_map.attempt_run(cat):
                ok= True

        if ok is True:
            self.__executor.submit(self.process, file_records, notes, bookmarks, contacts, cat)
            #self.process(file_records, notes, bookmarks, contacts,cat)

    def is_archiving(self, cat='all'):
        res = False
        with self.__lock:
            res = self.__is_running_map.is_running(cat)
        return res
    
    def get_clone_file(self,cat='all'):
        out_dir= os.path.join(self.ARCH_ROOT, cat)
        output_zip = os.path.join(out_dir, self.FNAME_TMPL.format(cat))
        if os.path.exists(output_zip) and os.path.isfile(output_zip):
            return output_zip
        return None


    def process(self, file_records, notes, bookmarks, contacts, cat):
        out_dir= os.path.join(self.ARCH_ROOT, cat)
        os.makedirs(out_dir, exist_ok=True)
        output_zip = os.path.join(out_dir, self.FNAME_TMPL.format(cat))
        archdir='archive_{}'.format(cat)
        arch_files = []
        arch_notes = []
        arch_links= []
        arch_contacts= []
        arch_cats_notes = {}
        arch_cats_files = {}
        arch_cats_links= {}
        arch_cats_contacts= {}

        static_files = [(x, os.path.join(archdir,x.replace('./offline_statics/',''))) for x in glob.iglob("./offline_statics/**/*.*",recursive=True) if os.path.isfile(x) ]
        print(static_files)

        with zipfile.ZipFile(output_zip, "w") as z:
            for src,dst in static_files:
                z.write(src,dst)

            # files
            for fr in file_records:
                filepath = urllib.parse.unquote(fr.file.url,encoding='utf8')
                fn = os.path.basename(filepath)
                cat_path = os.path.join(fr.category,fn)
                arch_path = os.path.join(archdir,cat_path)
                z.write(filepath,arch_path)
                arch_file = ArchivedFile(fr.name,fr.category,fr.description,os.path.join('../',cat_path))
                if fr.category in arch_cats_files:
                    arch_cats_files[fr.category].append(arch_file)
                else:
                    arch_cats_files[fr.category] = [arch_file]
                arch_files.append(arch_file)

            #files by cats
            for k, v in arch_cats_files.items():
                files_html_str = render_to_string('offline/files.html', {'page_title':k , 'files':v, 'links':subpage_links})
                z.writestr(os.path.join(archdir,self.CATS_FILES_HTML.format(k)), files_html_str)
                

            #allfiles

            arch_files.sort(key=lambda x:x.name)
            files_html_str = render_to_string('offline/files.html', {'page_title':'Your Files', 'files':arch_files, 'links':subpage_links})
            z.writestr(os.path.join(archdir,self.FILES_HTML), files_html_str)

            #notes
            for note in notes:
                arch_note = ArchivedNote(note.title,note.category,note.body, note.created_date, os.path.join('notes','note_{}.html'.format(note.id)))
                note_html_str = render_to_string('offline/note.html', {'note':note,'links':subsubpage_links })
                if note.category in arch_cats_notes:
                    arch_cats_notes[note.category].append(arch_note)
                else:
                    arch_cats_notes[note.category] = [arch_note]
                arch_notes.append(arch_note)
                z.writestr(os.path.join(archdir,self.NOTE_HTML.format(note.id)), note_html_str)


            for k, v in arch_cats_notes.items():
                notes_html_str = render_to_string('offline/notes.html', {'page_title':k , 'notes':v, 'links':subpage_links})
                z.writestr(os.path.join(archdir,self.CATS_NOTES_HTML.format(k)), notes_html_str)

            arch_notes.sort(key=lambda x:x.title)
            notes_html_str = render_to_string('offline/notes.html', {'page_title':'Your Notes' ,'notes':arch_notes,'links':subpage_links })
            z.writestr(os.path.join(archdir,self.NOTES_HTML), notes_html_str)


            #bookmarks
            for bookmark in bookmarks:
                arch_link= ArchivedLink(bookmark.title,bookmark.category,bookmark.url,bookmark.created_date )
                if bookmark.category in arch_cats_links:
                    arch_cats_links[bookmark.category].append(arch_link)
                else:
                    arch_cats_links[bookmark.category] = [arch_link]
                arch_links.append(arch_link)

            for k, v in arch_cats_links.items():
                links_html_str = render_to_string('offline/bookmarks.html', {'page_title':k , 'bookmarks':v, 'links':subpage_links})
                z.writestr(os.path.join(archdir,self.CATS_LINKS_HTML.format(k)), links_html_str)


            arch_links.sort(key=lambda x:x.title)
            bookmarks_html_str = render_to_string('offline/bookmarks.html', {'page_title':'Your Bookmarks' ,'bookmarks':bookmarks,'links':subpage_links })
            z.writestr(os.path.join(archdir,self.BOOKMARKS_HTML), bookmarks_html_str)

            #contacts
            for contact in contacts:
                arch_contact = ArchivedContact(contact.name,contact.email,contact.contact,contact.note,contact.created_date,contact.category)
                if contact.category in arch_cats_contacts:
                    arch_cats_contacts[contact.category].append(arch_contact)
                else:
                    arch_cats_contacts[contact.category] = [arch_contact]
                arch_links.append(arch_contact)

            for k, v in arch_cats_contacts.items():
                contacts_html_str = render_to_string('offline/contacts.html', {'page_title':k , 'contacts':v, 'links':subpage_links})
                z.writestr(os.path.join(archdir,self.CATS_CONTACTS_HTML.format(k)), contacts_html_str)


            arch_contacts.sort(key=lambda x:x.name)
            contacts_html_str = render_to_string('offline/contacts.html', {'page_title':'Your Contacts', 'contacts':contacts,'links':subpage_links })
            z.writestr(os.path.join(archdir,self.CONTACTS_HTML), contacts_html_str)


            #home
            home_html_str = render_to_string('offline/home.html',{'links':homepage_links})
            z.writestr(os.path.join(archdir,self.HOME_HTML), home_html_str)
        with self.__lock:
            print('done')
            self.__is_running_map.attempt_stop(cat)
            





