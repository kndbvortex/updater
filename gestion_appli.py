from win32api import GetFileVersionInfo, LOWORD, HIWORD
import win32com.shell.shell as shell
import urllib.request
import requests
import tqdm


def get_online_version(lien):
    if connexion_on() == True:
        reponse = requests.get(lien)
        page_html = reponse.text 
        reponse = ''
        dict_lien = {'Informer': '', 'BnR': '', 'Passage': '','Report': '', 'Schooling': '', 'TimeTable': ''}
        page_html = page_html.split('td')
        for e in page_html:
            if '<a' in e and '</a>':
                name = e.split('"')[1]
                if '%' in name:
                    a = name.split('%')
                    nom, version = a[1][2:] ,a[2][2:-4]
                    dict_lien[nom] = version if version > dict_lien[nom] else dict_lien[nom]
        return dict_lien
    else :
        return {'Informer': 'Non connecté', 'BnR': 'Non connecté', 'Passage': 'Non connecté','Report': 'Non connecté', 'Schooling': 'Non connecté', 'TimeTable': 'Non connecté'}


def connexion_on():
    try:
        urllib.request.urlopen('https://www.google.com', timeout = 3)
        return True
    except urllib.request.URLError : 
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


def silent_installation(setup_location):
    '''setup_location est le chemin absolue du setup'''
    command = 'start /w ' + setup_location + ' /S'
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+ command)


def telechargeur(url):
    '''Télégarger une ressource au bout de l'url dans le chemin '''
    if connexion_on() :
        reponse = requests.get(url, stream = True)
        nom_fichier =  url.split('/')[-1]

        if reponse.status_code == requests.codes.ok:
            with open(nom_fichier,'wb') as flux:
                taille_fichier = reponse.headers.get('content-length')
                if taille_fichier is None:
                    flux.write(reponse.content)
                else:
                    for partie in tqdm.tqdm(iterable = reponse.iter_content(chunk_size = 1024), total = int(taille_fichier) / 1024, unit = 'KB'):
                        flux.write(partie)
            print("Télégargement effectué avec succès")
    else :
        return None

if __name__ == "__main__":
    print(get_online_version('https://infolab-technologies.com/setup/'))
    print(connexion_on())
    #shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+ 'start /w C:\\Users\\Kndb#\\Documents\\executable_windows\\Wireshark-win64-3.2.2.exe /S')
