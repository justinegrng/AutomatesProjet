from fileTxt import*

'''Fonction pour vérifier si l'automate est déterministe'''
def isDeterministic(automate):
    nonDeterministicReasons = []
    numInitialStates = len(automate["initialStates"])

    # Vérifier si l'automate est déterministe
    for state in range(automate["numStates"]):
        for symbol in getAlphabet(automate):
            # Trouver les transitions pour cet état et ce symbole
            nextStates = set()
            for transition in automate["transitions"]:
                if transition[0] == state and transition[1] == symbol:
                    nextStates.add(transition[2])
            # Si plus d'une transition existe, ce n'est pas déterministe
            if numInitialStates !=1 :
                nonDeterministicReasons.append(f"L'automate a {numInitialStates} états d'entrées")
            elif len(nextStates) > 1:
                nonDeterministicReasons.append(
                    f"État {state} a des transitions multiples pour le symbole '{symbol}' : {nextStates}")
            elif len(nextStates) == 0:
                nonDeterministicReasons.append(f"État {state} n'a pas de transition pour le symbole '{symbol}'.")


            if nonDeterministicReasons:
                print(nonDeterministicReasons)
                return False
            return True



'''Fonction pour vérifier si l'automate est standard'''
def isStandard(automate):
    nonStandardReasons = []

    # Vérifier qu'il y a un seul état initial
    if len(automate["initialStates"]) != 1:
        nonStandardReasons.append("L'automate doit avoir un seul état initial.")

    # Vérifier que l'état initial ne peut pas être atteint par une transition
    initialState = automate["initialStates"][0]
    for transition in automate["transitions"]:
        startState, symbol, endState = transition
        if endState == initialState:
            nonStandardReasons.append(
                f"Il existe une transition menant à l'état initial {initialState} à partir de l'état {startState} pour le symbole '{symbol}'.")

    if nonStandardReasons:
        print(nonStandardReasons)
        return False
    return True


'''Fonction pour vérifier si l'automate est complet'''
def isComplete(automate):
    # Récupérer l'alphabet de l'automate
    alphabet = getAlphabet(automate)

    # Vérifier pour chaque état et chaque symbole si une transition existe
    for state in range(automate["numStates"]):
        for symbol in alphabet:
            # Trouver toutes les transitions possibles pour l'état et le symbole
            transitionExists = False
            for transition in automate["transitions"]:
                if transition[0] == state and transition[1] == symbol:
                    transitionExists = True

            # Si aucune transition n'est trouvée pour cet état et symbole, l'automate n'est pas complet
            if not transitionExists:
                print(f"L'état {state} n'a pas de transition pour le symbole '{symbol}'.")
                return False

    # Si toutes les vérifications passent, l'automate est complet
    return True

'''Fonction pour reconnaître un mot'''
def recognizeWord(automate, word):
    """Vérifie si un mot est reconnu par l'automate (déterministe ou non-déterministe)"""

    # Liste des états accessibles depuis les états initiaux
    currentStates = automate["initialStates"][:]

    # Lire chaque symbole du mot
    for symbol in word:
        nextStates = []

        for state in currentStates:
            for transition in automate["transitions"]:
                if transition[0] == state and transition[1] == symbol:
                    if transition[2] not in nextStates:
                        nextStates.append(transition[2])  # Ajouter les nouveaux états accessibles

        # Mettre à jour les états courants
        if not nextStates:  # Si aucun état atteint, le mot est rejeté
            return False

        currentStates = nextStates

    # Vérifier si au moins un état courant est un état final
    for state in currentStates:
        if state in automate["finalStates"]:
            return True

    return False