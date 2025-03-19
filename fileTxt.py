# Fonction pour afficher l'automate sous forme de tableau
def readAutomateFromFile(filename):
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


def getAlphabet(automate):
    alphabet = set()
    for transition in automate["transitions"]:
        alphabet.add(transition[1])
    return sorted(list(alphabet))  # Trie les symboles


def displayAutomate(automate):
    """FAIRE ATTENTION A LA SORTIE ET ENTREE AU MEME ENDROIT, PAS AFFICHER"""
    alphabet = getAlphabet(automate)

    # Trier les états : d'abord initiaux, puis les autres
    states = list(automate["initialStates"])  # Récupérer les états initiaux
    for s in range(automate["numStates"]):
        if s not in automate["initialStates"] :
            states.append(s) # Ajouter les autres états triés

    # Largeur des colonnes
    colWidth = 7
    stateColWidth = 9

    # En-tête du tableau
    header = "+----+---------+"
    for a in alphabet:
        header += a.center(colWidth) + "|"
    separator = "+====+=========" + "+=======" * len(alphabet) + "+"

    print(header)
    print(separator)

    for state in states:
        # Définir le type d'état (I = initial, O = final, rien sinon)
        if state in automate["initialStates"]:
            stateType = "I "
        elif state in automate["finalStates"]:
            stateType = "O "
        else:
            stateType = "  "

        row = "| " + stateType.ljust(3) + "| " + str(state).rjust(stateColWidth - 2) + " |" # Assure alignement correct

        for symbol in alphabet:
            # Récupérer toutes les transitions pour cet état et ce symbole
            nextStates = set()
            for transition in automate["transitions"]:
                if transition[0] == state and transition[1] == symbol:
                    nextStates.add(str(transition[2]))

            if nextStates:
                cell = f"{{{','.join(sorted(nextStates))}}}".center(colWidth)
            else:
                cell = " - ".center(colWidth)

            row += cell + "|"

        print(row)
        print("+----+---------+" + "-------+" * len(alphabet))