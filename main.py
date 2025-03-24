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
    else :
        choice = input("Quel automate vous intéresse ?")
        return os.path.join(directory, "automate%d.txt" % int(choice))


def main():
    automatonFile = chooseAutomat()
    directory = "automates"
    automate = readAutomateFromFile(automatonFile)
    # Obtenir l'alphabet de l'automate
    alphabet = getAlphabet(automate)
    while True:
        printMenu()
        menuChoice(automate)
        choice = input("Voulez-vous continuer ? ")
        if choice.lower() == "oui":
            True
        else:
            print("Au revoir")
            exit(0)


def printMenu():
    print ("1. Afficher l'automate")
    print("2. Est ce que l'automate est déterministe ?")
    print("3. Est ce que l'automate est standard ?")
    print("4. Est ce que l'automate est complet ?")
    print("5. Standardiser l'automate")
    print("6. Compléter l'automate")
    print("7. Déterminiser l'automate")
    print("8. Reconnaître un mot")
    print("9. Minimiser l'automate")
    print("10. Faire le complémentaire de l'automate")
    print("11. Changer d'automate")

def menuChoice(automate):
    choice = input("Choisissez une option: ")
    if choice == "1":
        displayAutomate(automate)
    elif choice == "2":
        print("Déterministe ? : ", isDeterministic(automate))
    elif choice == "3":
        print("Standard ? ", isStandard(automate))
    elif choice == "4":
        print("Complet ?", isComplete(automate))
    elif choice == "5":
        automateStand = standardizeAutomate(automate)
        print("Automate standardisé: ")
        displayAutomate(automateStand)
    elif choice == "6":
        print("Automate complet")
        automateComplet = completeAutomate(automate)
        displayAutomate(automateComplet)
    elif choice == "7":
        print("Automate Déterminisé")
        automateDeterminise = Determinisation(automate)
        displayDeterminisation(automateDeterminise)
    elif choice == "8":
        print("Le mot est reconnu ?")
        mot = input("Entrez un mot: ")
        print(recognizeWord(automate, mot))
    elif choice == "9":
        print("Automate minimisé")
        displayAutomate(Minimisation(automate))
    elif choice == "10":
        print("Automate complémentaire")
        displayAutomate(Complementarisation(automate))
    elif choice == "11":
        automatonFile = chooseAutomat()
        automate = readAutomateFromFile(automatonFile)
        menuChoice(automate)
        print("Automate changé")
    else :
        print("Choix invalide")

if __name__ == "__main__":
    main()