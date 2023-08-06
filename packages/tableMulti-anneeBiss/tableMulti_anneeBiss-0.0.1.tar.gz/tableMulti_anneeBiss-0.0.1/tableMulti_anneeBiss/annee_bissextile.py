"""
Cette fonction permet de verifier à partir d'une année entrer au clavier si elle est bissextile ou non
Auteur: Ousmane CISSE
Date: 05/12/2020

"""
__version__ = "0.0.1"




#Création de la foction
def annee_bissextile():
    
    #Recuperation de la valeur
    annee=int(input("Donnez une annee: "))
    
    #Verification de la condition
    if annee%400==0 or (annee%4==0 and annee%100!=0):
        #Affichage
        print("L'année {} est bissextile".format(annee))
    else:
        #Affichage
        print("L'année {} n'est pas bissextile".format(annee))


if __name__ == "__main__":
    annee_bissextile()
