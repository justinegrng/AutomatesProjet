from fileTxt import *
from detection import*
from automate import *
import os
def chooseAutomat():
    directory = "automates"
    files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    if not files:
        print("Pas de fichier trouvé.")
        return None

    while True:
        choice = input("Quel automate vous intéresse ? (number): ")
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return os.path.join(directory, files[int(choice) - 1])
        print("Choix invalide.")


def main():
    # automatonFile = chooseAutomat()

    # Exemple d'utilisation
    directory = "automates"
    filename = os.path.join(directory, "automate5.txt")
    automate = readAutomateFromFile(filename)

    # Obtenir l'alphabet de l'automate
    alphabet = getAlphabet(automate)

    displayAutomate(automate)
    print("Déterministe ? : ", isDeterministic(automate))
    print("Standard ? ", isStandard(automate))
    print("Complet ?", isComplete(automate))

    automateStand = standardizeAutomate(automate)
    print("Automate standardisé: ")
    displayAutomate(automateStand)

    print("Automate complet")
    automateComplet = completeAutomate(automate)
    displayAutomate(automateComplet)
if __name__ == "__main__":
    main()
