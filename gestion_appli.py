from win32api import GetFileVersionInfo, LOWORD, HIWORD
import win32com.shell.shell as shell
import urllib.request
import requests
import tqdm
import time, os
from socket import timeout

def get_online_version(lien):
    if connexion_on() == True:
        reponse = requests.get(lien)
        page_html = reponse.text 
        reponse = ''
        dict_lien = {'Informer': ('',''), 'BnR': ('', ''), 'Passage': ('', ''),'Report': ('', ''), 'Schooling': ('', ''), 'TimeTable': ('', '')}
        page_html = page_html.split('td')
        for e in page_html:
            if '<a' in e and '</a>' in e:
                name = e.split('"')[1]
                if '%' in name:
                    a = name.split('%')
                    nom, version = a[1][2:] ,a[2][2:-4]
                    lien_telechargement = 'https://infolab-technologies.com/setup/' + name
                    dict_lien[nom] = (version, lien_telechargement) if version > dict_lien[nom][0] else (dict_lien[nom][0], lien_telechargement)
        return dict_lien
    else :
        return {'Informer': ('Non connecté',''), 'BnR': ('Non connecté',''), 'Passage': ('Non connecté',''),\
                'Report': ('Non connecté', ''), 'Schooling': ('Non connecté', ''),\
                'TimeTable': ('Non connecté', '')}

def connexion_on():
    try:
        urllib.request.urlopen('https://www.google.com', timeout = 3)
        return True
    except urllib.request.URLError : 
        return False
    except timeout:
        return False

def get_version_number(filename):
    '''filename est le chemin vers l'exécutable de l'application installer'''
    try:
        #cette fonction retourne un dictionnaire de données ayant des info sur la version
        info = GetFileVersionInfo (filename, "\\") 
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version =  '{}.{}.{}'.format(HIWORD (ms), LOWORD (ms), HIWORD (ls))
        version += str(LOWORD (ls)) if str(LOWORD (ls)) != '0' else ''
        return version

    except:
        return 'Application inconnue'

def silent_uninstallation(uninstall_location):
    try:
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c "'+ uninstall_location + '" /VERYSILENT')
    except:
        pass

def silent_installation(setup_location):
    '''setup_location est le chemin absolue du setup'''
    try:
        command = '"' + setup_location + '" /VERYSILENT'    
        print(command)
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+ command)
    except:
        pass

def mis_a_jour(setup_path, uninstall_path):
    silent_uninstallation(uninstall_path)
    time.sleep(8)
    silent_installation(setup_path)
    
def telechargeur(url):
    '''Télégarger une ressource au bout de l'url dans le chemin '''
    if connexion_on() :
        reponse = requests.get(url, stream = True)
        nom_fichier =  'Downloads/' + url.split('/')[-1]
        if reponse.status_code == requests.codes.ok:
            with open(nom_fichier,'wb') as flux:
                taille_fichier = int(reponse.headers.get('content-length'))
                if taille_fichier is None:
                    flux.write(reponse.content)
                else:
                    c = 0
                    for partie in  reponse.iter_content(chunk_size = 512):
                        c += len(partie)
                        flux.write(partie)
                        print(c * 100/taille_fichier, "%")
            print("Télégargement effectué avec succès")
    else :
        return None

if __name__ == "__main__":
    '''
    print(get_online_version('https://infolab-technologies.com/setup/'))
    print(connexion_on())
    a = 'C:\\Users\\Kndb#\\Documents\\programmation\\python\\projet_reseau\\SAGEES%20Informer%202019.0.3.exe'
    b = r'C:\\Program Files (x86)\\INFOLAB Technologies\\SAGEES Informer\\unins000.exe'
    #mis_a_jour(a, b)
    silent_uninstallation(b)
    if not os.path.exists('Downloads') :
        print("j'existe")
    '''
    try :
        print(1/0)
    except:
        print("error")
    silent_installation('C:\\Users\\Kndb#\\Documents\\programmation\\python\\projet_reseau\\SAGEES Report 2019.0.32.exe')