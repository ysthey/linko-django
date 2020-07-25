import multiprocessing as mp
import zipfile
import os
from concurrent.futures import ThreadPoolExecutor
from django.template.loader import render_to_string
import threading


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

class ArchiveManager:
    __instance = None
    __executor = ThreadPoolExecutor(max_workers=mp.cpu_count())
    ARCH_ROOT = './archives'
    ARCH_TEMP = os.path.join(ARCH_ROOT, 'temp')
    FNAME_TMPL = "archive_{}.zip"
    FILES_HTML = "html/files.html"
    NOTES_HTML = "html/notes.html"
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
                #self.__executor.submit(self.process, file_records, cat)

        if ok is True:
            self.process(file_records, notes, bookmarks, contacts,cat)

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
        print(output_zip)
        homepage_links = {
            'home':'./index.html',
            'notes':'./html/notes.html',
            'bookmarks':'./html/bookmarks.html',
            'contacts':'./html/contacts.html',
            'files':'./html/files.html',
        }
        subpage_links = {
            'home':'../index.html',
            'notes':'./notes.html',
            'bookmarks':'./bookmarks.html',
            'contacts':'./contacts.html',
            'files':'./files.html',
        }
        with zipfile.ZipFile(output_zip, "w") as z:
            # files
            for fr in file_records:
                fn = os.path.basename(fr.file.url)
                cat_path = os.path.join(fr.category,fn)
                arch_path = os.path.join(archdir,cat_path)
                z.write(fr.file.url,arch_path)
                arch_files.append(ArchivedFile(fr.name,fr.category,fr.description,os.path.join('../',cat_path)))
            files_html_str = render_to_string('offline/files.html', {'files':arch_files, 'links':subpage_links})
            z.writestr(os.path.join(archdir,self.FILES_HTML), files_html_str)

            #notes
            notes_html_str = render_to_string('offline/notes.html', {'notes':notes,'links':subpage_links })
            z.writestr(os.path.join(archdir,self.NOTES_HTML), notes_html_str)

            #bookmarks
            bookmarks_html_str = render_to_string('offline/bookmarks.html', {'bookmarks':bookmarks,'links':subpage_links })
            z.writestr(os.path.join(archdir,self.BOOKMARKS_HTML), bookmarks_html_str)

            #contacts
            contacts_html_str = render_to_string('offline/contacts.html', {'contacts':contacts,'links':subpage_links })
            z.writestr(os.path.join(archdir,self.CONTACTS_HTML), contacts_html_str)


            #home
            home_html_str = render_to_string('offline/home.html',{'links':homepage_links})
            z.writestr(os.path.join(archdir,self.HOME_HTML), home_html_str)
        with self.__lock:
            print('done')
            self.__is_running_map.attempt_stop(cat)
            





