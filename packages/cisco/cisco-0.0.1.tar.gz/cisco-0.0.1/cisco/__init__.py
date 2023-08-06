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


"""
Cette fonction permet de verifier à partir d'une année entrer au clavier si elle est bissextile ou non
Auteur: Ousmane CISSE
Date: 05/12/2020

"""


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
