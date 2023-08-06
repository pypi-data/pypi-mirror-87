import os
from time import sleep
# The screen clear function

# fonction de nettoyage de l'ecran
def nettoyer_ecran():

    # pour mac ou linux(ici, os.name c'est 'posix')
   if os.name == 'posix':

      _ = os.system('clear')

    # pour windows
   else:

      _ = os.system('cls')

# fonction de saisie d'une valeur positive
def saisir_valeur_positive():

    while True:

        val = int(input("Entrez une annee entre 1000 et > 1000 : "))

        if val >= 1000:

            nettoyer_ecran()
            return val

        else:

            print("La valeur saisie n'est pas valide, veuillez reprendre")
            sleep(3)
            nettoyer_ecran()

# fonction renvoie vrai ou faux si la valeur est bissextille
def est_bissextille(annee):

    if(annee%4==0 and annee%100!=0 or annee%400==0):

        print(annee, "est une annee bissextille")

    else:

        print(annee, "n'est pas une annee bissextille")

annee = saisir_valeur_positive()
est_bissextille(annee)
