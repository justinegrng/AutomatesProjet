from fileTxt import *

def chooseAutomat():
    files = [f for f in os.listdir() if f.startswith("automate") and f.endswith(".txt")]

    if not files:
        print("Pas de fichier trouvé.")
        return None

    while True:
        choice = input("Quel automate vous intéresse ? (number): ")
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return files[int(choice) - 1]
        print("Choix invalide.")


def main():
    # automatonFile = chooseAutomat()

    # Exemple d'utilisation
    filename = ("automate22.txt")
    automate = readAutomatonFromFile(filename)

    # Obtenir l'alphabet de l'automate
    alphabet = getAlphabet(automate)


if __name__ == "__main__":
    main()
