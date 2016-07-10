# file : bm_u_for_ftp.py

"""Une classe pour récupérer des données par FTP."""

import ftplib,  shutil
import configuration_file as Cf

DEFAULT_OUTPUT = r"../"
class FtpSurServeur():
    """Outil très limité pour récupérer un seul fichier par FTP.

Exemple d'utilisation
           file ='le_nom_du_fichier'
           ObjFtp=FtpSurServeur()
           ObjFtp.download("/reptmp/tmp2", file)
"""
    
    def __init__(self):
        self.mdp=input("Mot de passe ?")
        self.connexionFtp = ftplib.FTP(Cf.FTP_ADRESS,
                                       Cf.FTP_USER, self.mdp)
        
    def download(self,directory,file):
        self.connexionFtp.cwd(directory)
        # On ouvre un fichier et on écrit dedans ce qui est récupéré par ftp
        f = open(file,"wb")
        self.connexionFtp.retrbinary("RETR " + file,f.write)
        f.close()
        print("Chargement de {} terminé".format(file))
        
# Exemple d'utilisation de la classe : 
    
def downloadfi59():
    downloadfiXX(59)

def downloadfi60():
    downloadfiXX(60)
    
def downloadfiXX(XX):
    """Un très petit outil de chargement FTP des fichiers nommé fiXX"""

    file='fi'+str(XX)
    ObjFtp=FtpSurServeur()
    ObjFtp.download(Cf.TMP_REP ,file)
    shutil.copy(file,DEFAULT_OUTPUT+file)
