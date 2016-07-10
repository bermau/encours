# file : menu_mvc
"""Un essai d'application graphique pour gérer quelqeus commandes.

But général :
- lancer un ftp pour récupérer des fichiers.
- lancer le traitement de certaines commandes dans un terminal.

La configuration de ce programme est dans configuration_file.py, dont je mets
une copie sous le nom configuration_file.sample.py


"""


# pour python 3.
# v1 : fonctione mais avec plein de classes qu'il faut maintenant externer
# but v 2 : externer les classes en modules

import pdb, re, time
import tkinter as tk
import menus

LIMITE = None # sert pour la mise au point de l'importation de fichier

from bm_u import titrer
import bm_u,  encours

DEFAULT_INPUT = r"../input/"

class Graphe(tk.Frame):
    """Graphe central avec surtout le graphique ; 
    """
    def __init__(self,boss=None):
        tk.Frame.__init__(self,boss)
        self.boss = boss # indispensable ? pour réutiliser boss dans les méthodes de la classe
        self.largeur = boss.largeur
        self.hauteur = boss.hauteur
        self.can = tk.Canvas(self, bg='white', width=boss.largeur,
                             height=boss.hauteur, borderwidth=2)
        self.can.grid(row=0, column=0)
        
class SidePanel(tk.Frame):
    def __init__(self, root):
        self.frame1=tk.Frame.__init__(self,root)
        self.frame2 = tk.Frame(self, root )
        self.frame2.grid(sticky=tk.N)
        self.plotBut = tk.Button(self.frame2, text="Version")
        self.plotBut.grid(sticky=tk.W)
        self.clearButton = tk.Button(self.frame2, text="Clear")
        self.clearButton.grid(sticky=tk.W)
               
class ViewType1(tk.Frame):
    
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        # La fenêtre
        self.largeur, self.hauteur=800,400 # size of the window. 
        self.master.title("Interface général")
        # construction des différentes zones de la fenêtre
        self.leMenu = menus.MenuBar(self) # barre de menu réroulant en haut
        self.leGraphe = Graphe(self) # le graphique
        self.sidepanel = SidePanel(self) # panneau en haut (à déplacer)
        # positionnements des élements déclarés ci-dessus
##        self.leMenu.grid(row=1,column=1, sticky=tk.W, columnspan=10)
##        self.leGraphe.grid(row=2, column=2, columnspan=7,sticky=tk.W)
##        self.sidepanel.grid(row=2,column=3) # pas de méthode grid()

        self.leMenu.grid(row=1, column=3, sticky=tk.W)
        self.leGraphe.grid(row=2, column=3)
        self.sidepanel.grid(row=2,column=2) # pas de méthode grid()
        # placer les objets avant de commencer
        self.grid()

    def lire_fichier(self):
        pass
        filename =  tk.filedialog.askopenfilename(
            initialdir = "E:/Images", title = "choose your file",
            filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if filename != None:
            print("This excel file has been selected", filename)

    def afficherVersion(self):
        msg = "Version du programme: 0.10 \nnov 2015"
        s = "Version de Tk :{tk} \nVersion de Tcl :{tcl}".format(tk=tk.TkVersion,tcl=tk.TclVersion)
        msg = msg + "\n" + s
        # msg=self.extraireVersionDuFichier("/home/bertrand/Bureau/ctrl_partiel/gestcqe_31/readme2.txt")
        # msg=self.extraireVersionDuFichier("readme.txt")
        print(msg) # pose problème dans le terminal windows. )
        tk.messagebox.showinfo("Version", msg)

    def quit(self):
        print("Bye...")
        c.tkroot.destroy()
       
class Controller():
    def __init__(self):
        self.tkroot=tk.Tk()
        # self.model=encours.Encours(filename=DEFAULT_INPUT+"fi59",encoding="latin1")
        self.view=ViewType1(self.tkroot)
        # ici il faut définir les menus.
        self.view.sidepanel.plotBut.bind("<Button>",self.aff_version)
        self.view.leMenu.toolMenu.entryconfig(1, command=self.downloadFi58)
        # self.view.leMenu.toolMenu.entryconfig(2, state=tk.DISABLED)

    def aff_version(self,event):
        #self.model.afficherVersion()
        self.view.afficherVersion() # idem mais en mode graphique.

    def downloadFi58(self):
        bm_u.downloadfiXX(58)

    def run(self):
        self.tkroot.title("Traitement des encours")
        self.tkroot.deiconify()
        self.tkroot.mainloop()        

if __name__ == '__main__':
    c = Controller()  
    c.run()
    # ou plus simple :
    # Controller().run()     




