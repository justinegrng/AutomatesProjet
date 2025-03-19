# Fonction de lecture du fichier d'automate
def readAutomatonFromFile(filename):
    with open(filename, "r") as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]

    alphabetSize = int(lines[0])
    numStates = int(lines[1])
    initialStates = list(map(int, lines[2].split()[1:]))
    finalStates = list(map(int, lines[3].split()[1:]))

    transitions = []
    for line in lines[5:]:
        startState, symbol, endState = line.split()
        transitions.append((int(startState), symbol, int(endState)))

    automate = {
        "alphabetSize": alphabetSize,
        "numStates": numStates,
        "initialStates": initialStates,
        "finalStates": finalStates,
        "transitions": transitions
    }
    return automate


# Fonction pour obtenir l'alphabet de l'automate
def getAlphabet(automaton):
    alphabet = set()  # Utilisation d'un ensemble pour éviter les doublons
    for transitions in automaton["transitions"]:
        alphabet.add(transitions[1])  # On ne garde que le symbole (la lettre)
    return list(alphabet)


# Fonction pour afficher l'automate sous forme de tableau
def displayAutomate(automaton):
    # Récupération des états et de l'alphabet
    states = list(range(automaton["numStates"]))
    alphabet = getAlphabet(automaton)

    # Affichage de l'en-tête du tableau
    print("+-----+---------+" + "".join([f" {a}   |" for a in alphabet]))
    print("+=====+=========+" + "======" * len(alphabet))

    # Affichage des transitions pour chaque état
    for state in states:
        stateType = "I" if state in automaton["initialStates"] else "O" if state in automaton["finalStates"] else " "
        print(f"| {stateType}   |       {state} |", end="")

        for symbol in alphabet:
            # On cherche la transition pour cet état et ce symbole
            transition_found = False
            for transition in automaton["transitions"]:
                if transition[0] == state and transition[1] == symbol:
                    print(f" {transition[2]}   |", end="")
                    transition_found = True
                    break
            if not transition_found:
                print(" -   |", end="")
        print("\n+-----+---------+" + "-----" * len(alphabet))