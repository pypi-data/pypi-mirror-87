"""
Cette fonction permet d'afficher la table de multiplication en fonction d'un nombre enter au clavier.
Auteur: Ousmane CISSE
Date: 05/12/2020

"""
__version__ = "0.0.1"


#Creation de la fonction
def table_de_multiplication():

    #Recupération de la valeur
    n = int(input("Veuillez entrer un nombre: "))

    #Affichage de la table
    print("La table de multiplication de : ", n," est :")

    #Boucle pour parcourir de 1 à 10 
    for i in range(1,11):
        print(n , " x ", i, " = ",i*n)

if __name__ == "__main__":
    table_de_multiplication()
