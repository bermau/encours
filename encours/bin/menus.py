# -*- coding: utf-8 -*-
from tkinter import *  # (sur python 3.1 le module s'appèle tkinter)
import bm_u, bm_u_for_ftp
#from configuration_file import * # mon parametrage
#import demo_graph

"""Menus :
Fichier
-lire un fichier dans A,B,C
-sauver un fichier de A, B, C

Outils
-recup du fi59 par ftp

"""

class MenuBar(Frame):
    # tres important : transmettre boss !!
    """Définition de toute la Barre des menus déroulant"""
    def __init__(self, boss=None):
        Frame.__init__(self, boss, borderwidth =2)  
        # Menu Fichier
        menuFichier=Menubutton(self, text='Fichier', underline=0)
        menuFichier.pack(side=LEFT)
        menu1=Menu(menuFichier)
        menu1.add_command(label='Sauver les données', underline=0)
        menu1.add_command(label='Quitter', underline=0, command=boss.quit)
        menuFichier.configure(menu=menu1)
        # Menu Importation : Paramétrage : importer tous les fichiers
        menuCVMPL=Menubutton(self, text='Paramétrage', underline=0)
        menuCVMPL.pack(side=LEFT,padx=5)
        ListMenuCVMPL=Menu(menuCVMPL)
        ListMenuCVMPL.add_command(label='Créer la structure de la base', underline=0)
        ListMenuCVMPL.add_command(label='Importer tous les contrôles', underline=0)
        ListMenuCVMPL.add_command(label='Mettre la base zero', underline=0)
        ListMenuCVMPL.add_command(label='Afficher les données', underline=0)
        menuCVMPL.configure(menu=ListMenuCVMPL)
        # Menu Outils :
        toolMenuButton=Menubutton(self, text='Outils', underline=0)
        toolMenuButton.pack(side=LEFT,padx=5)
        self.toolMenu=Menu(toolMenuButton)
        self.toolMenu.add_command(label='FTP_fi58_(amazilia)', underline=0)
        self.toolMenu.add_command(label='FTP_fi59 (encours)', underline=0,
                                  command=bm_u_for_ftp.downloadfi59)
        self.toolMenu.add_command(label='FTP_fi60', underline=0,
                                  command=bm_u_for_ftp.downloadfi60)
        self.toolMenu.add_separator()
        self.menuVar1=self.toolMenu.add_command(label='Variable 1', underline=0)
        toolMenuButton.configure(menu=self.toolMenu)
        # Menu Divers et tests.
        menuTests=Menubutton(self, text='Tests',underline=0)
        menuTests.pack(side=LEFT,padx=5)
        menuitems4=Menu(menuTests)
        menuitems4.add_separator()
        menuitems4.add_command(label='Version', underline=0,command=boss.afficherVersion)
        menuTests.configure(menu=menuitems4)


