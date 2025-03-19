from fileTxt import*
def isDeterministic(automate):
    nonDeterministicReasons = []

    # Vérifier si l'automate est déterministe
    for state in range(automate["numStates"]):
        for symbol in getAlphabet(automate):
            # Trouver les transitions pour cet état et ce symbole
            nextStates = set()
            for transition in automate["transitions"]:
                if transition[0] == state and transition[1] == symbol:
                    nextStates.add(transition[2])
            # Si plus d'une transition existe, ce n'est pas déterministe
            if len(nextStates) > 1:
                nonDeterministicReasons.append(
                    f"État {state} a des transitions multiples pour le symbole '{symbol}' : {nextStates}")
            elif len(nextStates) == 0:
                nonDeterministicReasons.append(f"État {state} n'a pas de transition pour le symbole '{symbol}'.")

            if nonDeterministicReasons:
                return False, nonDeterministicReasons
            return True


# Fonction pour vérifier si l'automate est standard selon la définition donnée
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
        return False, nonStandardReasons
    return True