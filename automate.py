from fileTxt import *
from detection import *


def standardizeAutomate(automate):
    """ETAT INITIAL NOTER I"""
    if isStandard(automate):
        print("L'automate est déjà standard")
        return automate
    # Créer un nouvel état i (ajouté comme état initial)
    newInitialState = max(automate["numStates"], max(automate["finalStates"], default=-1) + 1)

    # Créer le nouvel automate standardisé
    standardAutomate = {
        "alphabetSize": automate["alphabetSize"],
        "numStates": automate["numStates"] + 1,  # Ajouter un état supplémentaire
        "initialStates": [newInitialState],  # L'état i devient le seul état initial
        "finalStates": automate["finalStates"],  # Les états finaux sont les mêmes
        "transitions": []
    }

    # Vérifier si l'automate C accepte le mot vide
    # On considère que l'automate reconnaît le mot vide s'il y a une transition 'e' partant d'un état initial
    acceptEpsilon = False
    for transition in automate["transitions"]:
        if transition[0] in automate["initialStates"] and transition[1] == 'e':  # Transition epsilon
            acceptEpsilon = True

    # Si l'automate reconnaît le mot vide, on ajoute l'état final comme état terminal
    if acceptEpsilon:
        standardAutomate["finalStates"].append(newInitialState)

    # Ajouter les transitions de l'état i vers les anciens états initiaux
    for initialStates in automate["initialStates"]:
        for transition in automate["transitions"]:
            if transition[0] == initialStates:  # Si la transition vient d'un état initial
                standardAutomate["transitions"].append((newInitialState, transition[1], transition[2]))

    # Ajouter les autres transitions existantes de l'automate original à l'automate standard
    for transition in automate["transitions"]:
        standardAutomate["transitions"].append(transition)

    return standardAutomate

# Compléter l'automate avec les transitions manquantes
def completeAutomate(automate):
    """ESSAYER ETAT POUBELLE ECRIT p DANS LES ETATS"""
    # Récupère alphabet
    alphabet = getAlphabet(automate)

    # Ajout état poubelle
    trapState = 'p'
    automate["numStates"] += 1

    # Ajouter boucle sur états poubelle
    for symbol in alphabet :
        automate["transitions"].append((trapState, symbol, trapState))

    # Compléter transitions pour chaque état
    for state in range(automate["numStates"]):
        # Pour chaque de l'alphabet
        for symbol in alphabet:
            # Vérifier si transition existe pour ce symbole
            hasTransition = False
            for transition in automate["transitions"]:
                if transition[0] == state and transition[1] == symbol:
                    hasTransition = True

            if not hasTransition:
                automate["transitions"].append((state, symbol, trapState))

    if trapState in automate["finalStates"]:
        automate["finalStates"].remove(trapState)

    return automate


def Determinisation(automate):
    initialStates = automate["initialStates"]
    alphabet = getAlphabet(automate)

    newStates = {}  # Dictionnaire des nouveaux états
    newTransitions = []  # Liste des nouvelles transitions
    queue = [tuple(sorted(initialStates))]  # File des états à traiter
    newFinalStates = set()  # Nouveaux états finaux

    print(f"États initiaux : {formatState(queue[0])}")

    while queue:
        currentSet = queue.pop(0)  # Récupère l'ensemble d'états en cours
        currentStateStr = formatState(currentSet)  # Format propre

        if currentStateStr not in newStates:
            newStates[currentStateStr] = len(newStates)

        print(f"\nTraitement de l'ensemble d'états {currentStateStr}")

        for symbol in alphabet:
            # Calcul des états atteints avec 'symbol'
            nextSet = sorted({
                int(stateTo) if isinstance(stateTo, str) and stateTo.isdigit() else stateTo
                for stateFrom, sym, stateTo in automate["transitions"]
                if stateFrom in currentSet and sym == symbol
            })

            if nextSet:  # S'il y a un état atteint
                nextStateStr = formatState(nextSet)  # Format propre

                print(f"- Transition avec '{symbol}' mène à {nextStateStr}")

                if nextStateStr not in newStates:
                    newStates[nextStateStr] = len(newStates)
                    queue.append(tuple(nextSet))  # Ajout à la file d'attente
                    print(f"Ajout d'un nouvel état : {nextStateStr}")

                newTransitions.append((currentStateStr, symbol, nextStateStr))

                # Vérifie si cet état doit être final
                if set(nextSet) & set(automate["finalStates"]):
                    newFinalStates.add(nextStateStr)
                    print(f"L'état {nextStateStr} est final")

    # Création de l'automate déterminisé
    afd = {
        "numStates": len(newStates),
        "initialStates": [formatState(initialStates)],
        "finalStates": list(newFinalStates),
        "transitions": newTransitions
    }


    if not isComplete(afd):
        afdComplet = completeAutomate(afd)  # Complétion de l'automate si nécessaire
    else:
        afdComplet = afd

    print("\nAutomate déterminisé")
    return afdComplet


def formatState(stateSet):
    """ Formate un ensemble d'états correctement """
    if len(stateSet) == 1:
        return str(stateSet[0])  # Affiche sans parenthèses ni virgule si un seul état
    return f"({', '.join(map(str, stateSet))})"  # Affiche avec parenthèses et virgules sinon


def Minimisation(automate):

    print("Début de l'algorithme de minimisation :\n")

    states = set()
    for t in automate["transitions"]:
        states.update([t[0], t[2]])

    final_states = set(tuple(s) if isinstance(s, (list, set)) else (s,) for s in automate["finalStates"])
    non_final_states = set(states) - final_states

    print(f"Les états terminaux sont : {final_states}")
    print(f"Les états non terminaux sont : {non_final_states}\n")

    partitions = [final_states, non_final_states]
    print(f"La partition initiale θ0 est : {partitions}\n")

    alphabet = getAlphabet(automate)

    stable = False
    iteration = 1
    while not stable:
        new_partitions = []
        print(f"Séparation de la partition précédente :")
        for group in partitions:
            subgroup_map = {}
            for state in group:
                signature = []
                for symbol in alphabet:
                    target = next((t[2] for t in automate["transitions"]
                                   if t[0] == state and t[1] == symbol), None)
                    for i, g in enumerate(partitions):
                        if target in g:
                            signature.append(i)
                            break
                    else:
                        signature.append(None)
                signature = tuple(signature)
                subgroup_map.setdefault(signature, set()).add(state)
            new_partitions.extend(subgroup_map.values())

        if new_partitions == partitions:
            print(f"\nLa partition finale est donc θ{iteration} = θf = {new_partitions}\n")
            stable = True
        else:
            print(f"\nNouvelles partitions θ{iteration} : {new_partitions}\n")
            partitions = new_partitions
            iteration += 1

    print("Fin de l'algorithme de minimisation.\n")
    return automate  # (à remplacer si tu veux retourner l'automate minimisé)