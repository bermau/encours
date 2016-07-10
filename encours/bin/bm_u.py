"""Utilitaires divers"""

DEFAULT_OUTPUT = r"../output/"

def  titrer(msg):
    "Afficher un titre"
    L=len(msg)
    print('*' * L)
    print(msg)
    print('*' * L)

def readakey(msg=''):
    "Attendre la pression d'une touche"
    if msg is not '':
        print(msg)
    print("Taper une touche pour conti:nuer ; Ctrl + C pour arrêter)")
    input()


    
    
    
