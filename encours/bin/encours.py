# Aider au traitement du fichier des encours venant de Synergy
# pour python 3.
"""v1 : embryon
V2 : objet. A améliorer : éliminer les \n
V3 : les \n sont éliminés. J'ai maintenant une fonction de recherche de mot clés.
v4 : ajout d'un menu. Permet la recherche d'une chaine quelconque.
v5 : permet la recherche d'expressions régulières,Retourne des set. cequi permet de faire des unions.
v6 création de synonymes
v7 : révision le 12/11/2016 ; le trt traite de fichiers entrant en latinou en iso
Le filtrage des lignes inutiles fonctionne pas.
v8 : j'ai fait un comparaison entre les états de fichiers à 2 époques.
v9 : embryon de commentaire sur un dossier.
v10 : mélange de graphique et texte
Utilisation d'un modèle de MVC de
https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
v11 :
v12 : j'ai commencé un rapport automatisé (fonction demo_de_rapport). travail dans train
J'arrive à controler un bouton selon le modèle MVD.
v13 : j'ai révisé la v12, qui fonctionne en mvc.
v14 : devrait fonctionner en VMC
v15 : Les listes restent triées.
v16 : Présente un trt graphique puis un texte de résumé. 
"""
import pdb, re, time, sys, datetime
import tkinter as tk

from bm_u import titrer
import bm_u
import configuration_file as Cf

LIMITE=None # sert pour la mise au point de l'importation de fichier

def debug(msg):
    """Affiche un message sur la sortie erreur. """
    sys.stderr.write(msg+"\n")


DEFAULT_INPUT = Cf.DEFAULT_INPUT_REP

class Encours():

    def __init__(self, filename=DEFAULT_INPUT+"fi59", encoding="latin1"):
        """Crée un objet à partir d'un fichier de synergy."""
        
        self.modified = False
        self.filename = filename
        with open(filename, encoding=encoding) as f:
            self.lines = f.readlines(LIMITE)
            self.lines = [ self.lines[i].replace('\n', '')
                           for i in range(len(self.lines))]
        debug("Lecture du fichier : \"{}\"".format(filename))
        self.entete_fichier = self.lines[4:6]
        debug(self.entete_fichier[0])
        debug(self.entete_fichier[1])
        
        debug("Taille du fichier : {} lignes importées".format(
            str(len(self.lines))))
        
        self.nettoyer_lignes_inutiles()
        self.cas = self.trouver_delimitations()
        self.tous = range(len(self.cas))
        
        debug("{combien} dossiers ont été enregistrés".format(
            combien = str(len(self.cas))))
        self.modified = False
    
    def nettoyer_lignes_inutiles(self):
        """Eliminer les lignes vides et les hauts de pages répétées."""
        maxi = len(self.lines)
        p = re.compile('.*PERIODE DU.*|.*CATEGO.*|.*==========.*')
        lines_cor = []
        for i in range(maxi):
            if (self.lines[i] is ''):
                pass
            elif (p.match(self.lines[i])):
                # print("Regex trouvé en {} : {}  ".format(i, self.lines[i]))
                pass
            else:
                lines_cor.append(self.lines[i])
        self.lines = lines_cor
        
    def trouver_delimitations(self):
        """On trouve les enregistrement entre deux séries de traits.
    Le premier enregitrement ne débute pas par des traits."""
        separateurs = [ x for x in range(0, len(self.lines))
                        if '---' in self.lines[x] ]
        debug("J'ai trouvé {} enregistrements".format(len(separateurs)))
        i = 0
        cas = []
        for indice_du_sep in range(len(separateurs)):
            cas.append(self.lines[i + 1:separateurs[indice_du_sep] + 1])
            i = separateurs[indice_du_sep]
        """On nettoye le premier dossier  A REVOIR"""
        # cas[0]=cas[0][5:]
        return cas
    
    def contient_mot(self, indice_cas, mot):
        """retourne True ou False selon que le mot est contenu
dans une des lignes du cas"""
        for la_ligne in self.cas[indice_cas]:
            if mot in la_ligne:
                return True
        return False

    def contient_regex(self, indice_cas, regex):
        """retourne True ou False selon qu'une expression régulière
est contenue dans une des liges du cas"""

        for la_ligne in self.cas[indice_cas]:
            p = re.compile(regex)
            m = p.match(la_ligne)
            if m:
                return True   
        return False

    def _chercher_indices_contenant_mot(self, mot, type='simple'):
        """Retourne un set d'indice contenant un mot ou une regex."""
        
        if type == 'simple':
            indices = [cas for cas in range(len(self.cas)) \
                     if self.contient_mot(cas,mot)] 
            return set(indices)
        elif type == 'regex':
            indices = [cas for cas in range(len(self.cas)) \
                     if self.contient_regex(cas,mot)]
            return set(indices)
        else:
            return None
        
    def chercher_regex(self,mot):
        """Cherche les indices contenant une regex.

--> set"""
        return self._chercher_indices_contenant_mot(mot, type='regex')

    def chercher_texte(self,mot):
        """Cherche les indices contenant un mot"""
        return self._chercher_indices_contenant_mot(mot, type='simple')

    def get_resume_de_recherche_avec_regex(self, regex, label='', limit=20):
        """Résumé de recherche avec regex"""
        buf = []
        lst_of_cas = list(self.chercher_regex(regex)) # unsorted set
        lst_of_cas.sort()
        buf.append(label)
        buf.append("J'ai trouvé {n} cas avec la regex {reg}".format(
                               n=str(len(lst_of_cas)),reg=regex))
        if len(lst_of_cas) <= limit:
            for cas in lst_of_cas:
                buf.append(self.get_id_nom(cas))
        else:
            buf.append("Extrait des {} premiers dossiers :".format(str(limit)))
            for cas in list(lst_of_cas)[0:20]:
                buf.append(self.get_id_nom(cas))
            buf.append("... suite ...")
        return buf
    
    def print_cas_multiples(self,indices):
        for i in indices:
            self.print_cas(i)

    def get_cas_multiples_id_nom(self,indices):
        """"retourn le l'ID et le nom d'une liste de cas"""
        for i in indices:
            print("indice",i)
            self.get_id_du_cas(int(i))
            
    def print_cas_multiples_id_nom(self,indices): 
        print(self.get_cas_multiples_id_nom(indices))
              
    def print_cas(self, indice_cas):
        """Affiche tout le cas"""
        for i in range(len(self.cas[indice_cas])):
            print(self.cas[indice_cas][i],end=None)


    def get_id_nom(self,indice_cas):
        """retourne la première ligne du cas avec num de dossier et nom"""
        for line in self.cas[indice_cas]:
            if 'Acc :' in line:
                return line
            
    def get_cor_du_cas(self, indice_cas):
        """Retourne le correspondant.
"""
        for line in self.cas[indice_cas]:
            if line.startswith(' CR '):
                return line[0:9]        
        
    def get_id_du_cas(self,indice_cas,verbose=False):
        """retourne le num de dossier"""
        line=self.get_id_nom(indice_cas)
        if verbose:
            print(line)
        return line[6:16]

    def comment_cas(self,indice_cas, msg=''):
        """Ajouter une ligne de commentaire"""
        s="COMMENTAIRE : {} : {}".format(time.strftime('%d/%m/%Y %H:%M',time.localtime()),msg)
        self.cas[indice_cas].insert(-1,s)
        self.modified=True

    def export_cas_multiples(self,indices,filename='',titre='',verbose=True):
        """Export le contenu d'une liste de cas sur un fichier
        """
        if titre == '':
            titre=input("Titre d'entête ? ")
        rep = ''
        if filename=='':
            rep=input("Saisir le nom de fichier, actuellement {}".format(filename))
            if rep=='':
                rep=filename
            else:
                filename=rep
        f=open(filename,'w')
        print("Sauvegarde des données dans \"{}\"".format(filename))
        f.write("\n"+titre+"\n"+"=="*30+"\n\n\n\n") # je recrée le format de sortie de LMX
        for cas_i in indices:
            for i in range(len(self.cas[cas_i])):
               f.write((self.cas[cas_i][i]+ "\n"))
        f.close()
        
    def print_resume(self):
        """Affiche un résumé avec premier, dernier dossier"""
        # pdb.set_trace()
        titrer("Résumé du fichier {}".format(self.filename))
        print("Nombre de cas : {}".format(str(len(self.cas))))
        print("Premier puis dernier dossiers")
        print(self.get_id_nom(0))
        print(self.get_id_nom(len(self.cas) - 1))
        
    def afficherVersion(self):
        print("Version 13")
    
    def close(self):
        if self.modified:
            rep =str(input("""Le ficheir de départ a été modifié (annoté?)
                  Voulez le sauvegarder (Y/N)""")) or 'y'
            if rep.lower() in ['y','o','yes','oui']:
                self.save()

    def save(self):
        """Sauvegarde tout avec les annotations"""
        self.export_cas_multiples(self.tous)

def menu():
    """Un menu de commandes"""
    while True:
        print("""
      Menu:
      1) Lire un fichier
      2) Chercher les cas contenant uen suite de caractères
      3) Clercher les cas contenant une expression régulière
      4) Exporter le résultat des recherches.
      Q) Sortir de ce menu
        """)
        ch=str(input())
        ch=ch.lower()
        print("Votre choix",ch)
        if ch == "1":
              pass
        elif ch =="2":
            mot=input("Chercher ?")
            titrer("Quels sont les dossiers avec résultats "+ mot)
            liste1=fichier.chercher_indices_contenant_mot(mot,type='simple')
            titrer("J'affiche les 3 premiers dossiers")
            fichier.print_cas_multiples(list(liste1)[0:3])
        elif ch =="3":
            mot=input("Regex à chercher ?")
            titrer("Quels sont les dossiers avec résultats "+ mot)
            liste1=fichier.chercher_indices_contenant_mot(mot, type='regex')
            titrer("J'affiche les 3 prremiers dossiers")
            fichier.print_cas_multiples(list(liste1)[0:3])         
        elif ch =="q":
             break
        else:
             print("Choix impossible")

def demo():    
    titrer("premiers enr")
    print(fichier.lines[1:20])
    titrer("Affichage du 3ème dossier")
    fichier.print_cas(3) 
    #menu()

# synonymes pour se simplifier la vie
"""On peut réaliser l'opération suivante :
    A=regex('.*HCON.*')
    print(A)
    B=lettre('ERAEFS')
    C=A.intersection(B)
    export(C)
"""
def demo_export():
    A=texte('BRANDA')
    export(A)


def exemple_comparaison_2_fichiers():
    print()
    fichier2=Encours(filename="fi59_21_oct_2015_utf8",encoding="utf8")
    fichier2.export_cas_multiples(fichier1.tous, filename="export_21_oct_2015",titre="Données au 21 oct 2015")
    print()
    fichier1=Encours(filename="fi59_12_nov_2015",encoding="latin1")
    fichier1.export_cas_multiples(fichier1.tous, filename="export_12_nov_2015",titre="Données au 12 nov 2015")

def exemple_sortie_des_exclus():
    """Dans cet exemple, les dossiers qui appartiennent à une liste et pas à l'autre
sont exportés"""
    verbose=True
    fichier1=Encours(filename="fi59_2015_10_21_utf8",encoding="utf8")
    fichier2=Encours(filename="fi59_2015_11_12",encoding="latin1")
    A=[]
    for cas in range(len(fichier1.cas)):
        num_acc=fichier1.get_id_du_cas(cas)
        if not fichier2.chercher_indices_contenant_mot(num_acc):
            if verbose:
                print("{} a disparu".format(num_acc)) 
            A.append(cas)
    fichier1.export_cas_multiples(A)

def mode_easy():  
    regex=fichier.chercher_regex
    texte=fichier.chercher_texte
    print_m=fichier.print_cas_multiples
    tous=fichier.tous
    export=fichier.export_cas_multiples

    
"""
TRES INTERESSANT
HCON=texte('HCON')
res_attendus=regex(".*Rés.attendus :[^0].*")
for cas in HCON.difference(res_attendus):
	print(fichier.get_id_nom(cas))
"""


def demo_rapport():
    
    A=Model(filename="../save_data/fi59_21_oct_2015_utf8",encoding="latin1")
    # A.export_cas_multiples(fichier1.tous, filename="export_21_oct_2015",titre="Données au 21 oct 2015")
    print()
    B=Model(filename="fi59",encoding="latin1")
    # B.export_cas_multiples(fichier1.tous, filename="export_12_nov_2015",titre="Données au 12 nov 2015")

    titrer("""Différence de B par rapport à A:
           A = {nom_A}
           B = {nom_B}
    ATTENTION : La situation initiales est dans le fichier A
           """
           .format(
                  nom_A=A.filename,
                  nom_B=B.filename))
    print(
"""   A contient {na} fichiers
   B contient {nb} fichiers""".format(na=str(len(A.cas)),nb=str( len(B.cas))))

    diff=len(A.cas)-len(B.cas)
    if diff<0:
        res= "Le nombre de dossiers en cours a donc augmenté de {} cas".format(str(abs(diff)))
    elif diff>0:
        res= "Le nombre de dossiers en cours a donc diminué de {} cas".format(str(diff))
    else:
        res= "Le nombre de dossiers en cours est donc resté identique"
    print(res)
    titrer("""Fichiers ayant disparu dans B par rapport à A""")
    not_in_B=synthese_A_not_in_B(A,B,export=False)
    titrer("""Fichiers de B nouveaux dans B (qui ne sont pas dans A)""")
    not_in_A=synthese_A_not_in_B(B,A)
    titrer("""Fichiers modifiés""")
    synthese_cas_de_B_modifies_dans_A(A,B,not_in_B)
    
    
def synthese_A_not_in_B(A,B,export='interactif'):
    """Affiche les données de A, qui ne sont plus dans B"""    
    # Je veux la liste des cas de A dont l'ID ne fait pas partie de B.
    indices_not_in_B= [cas for cas in range(len(A.cas)) if not B.chercher_texte(A.get_id_du_cas(cas))] 
    titrer("Il y a {} dossiers en moins".format(str(len(indices_not_in_B))))
    print("Leurs indices sont", indices_not_in_B)
    # Pour afficher les cas :
    # A.print_cas_multiples_id_nom(indices_not_in_B)
    # On exporte les cas : 
    exporter=None
    if export==True or export == False:
        exporter=export
    else:
        rep=input("Exporter ?")
        if rep:
            exporter=True
    if exporter:
        A.export_cas_multiples(indices_not_in_B,
                           filename='',
                           titre="Cas disparus du fichier {} \
                     par rapport au fichier {}".format(A.filename,B.filename),
                           verbose=True,
                           )    
    return indices_not_in_B

def synthese_cas_de_B_modifies_dans_A(A, B, not_in_B):
    """Les cas non identiques dans A et B"""
    pass
    
def etude_generique():
    """Une étude générique 1 d'un fichier d'encours"""
    a = Encours()
    a.print_resume()
def print_list(lst):
    """Print une liste"""

    for i in lst:
        print(i)     

def trt_1():
    """Un ensemble de 3 filtres usuels"""
    a = Encours()
    
    a.print_resume()
    print()
    # Dossier complets 
    print_list(a.get_resume_de_recherche_avec_regex(r'.*attendus :0.*',
                           label="Dossiers complets"))
    print()
    # Dossiers avec résultats attendus 
    print_list(a.get_resume_de_recherche_avec_regex(r'.*attendus :[^0].*',
                           label="Dossiers avec résultats attendus"))
    print()

    # Les lignes ci dessous devraient sans doute être incluses
    # dans un fonction get_resume_de_recherche_avec_regex modifée.

    
    # Dossiers avec problèmes d'impression
    regex_impression = r'.*\*.*'
    print_list(a.get_resume_de_recherche_avec_regex(regex_impression, 
                           label="Problèmes d'impression"))
    lst_cas_impression = a.chercher_regex(regex_impression)
    lst_cas_impression = list(lst_cas_impression)
    lst_cas_impression.sort()
    # Dédiéser pour les détails : 
    # a.print_cas_multiples(list(lst_cas_impression))
    # On peut aussi imprimer le service des dossiers avec pb impression
    print("détails :")
    
    for cas in lst_cas_impression:
        print( a.get_cor_du_cas(cas), a.get_id_nom(cas))

def trt_graphe():
    """Présente un graphique général des dossiers encours."""

    a = Encours()
    a.limite = a.tous
    # comprehension list of dates.
    lst_tout = [ get_date_from_id(a.get_id_du_cas(cas)) for cas in a.limite ]
    from graph_encours import graphe
    graphe(lst_tout)
    print("Terminé")
      

def get_date_from_id(id):
    """Retourne la date à parti d'un ID  long 

    >>> get_date_from_id("6071160440")
    '2016-07-11'

    >>> get_date_from_id("60440")
    ValueError: id must be 10 cars

    >>> get_date_from_id(6071160440)
    ValueError: id must be 10 cars
    
"""
    try:
        if len(id) != 10:
             raise ValueError("id must be 10 cars")  
    except:
         ValueError("id must be 10 cars")
    day = id[3:5]
    month = id[1:3]
    year = id[0:1]
    year = '201' + year
    return('-'.join( [year, month, day]))
 
def present_this_programm():
    """Affiche des données sur la date et la version"""
    print("Date de traitement : {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    print()

def _test():
    import dcotest
    doctest.testmod()
    
if __name__ == '__main__':
    """Une étude générique"""
    present_this_programm()
    trt_graphe()
    trt_1()
    
