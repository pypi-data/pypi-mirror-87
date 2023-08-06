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

        val = int(input("Entrez un nombre > 1: "))

        if val > 1:

            nettoyer_ecran()
            return val

        else:

            print("La valeur saisie n'est pas valide, veuillez reprendre")
            sleep(2)
            nettoyer_ecran()

# fonction de multiplication
def table_multiplication(nombre):

  print("La table de multiplication de ", nombre," est :")

  for i in range(1,10):

    print(i , " x ", nombre, " = ",i*nombre)

nombre = saisir_valeur_positive()
table_multiplication(nombre)
