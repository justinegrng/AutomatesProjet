from fileTxt import *
from detection import *


def standardizeAutomate(automate):
    """ETAT INITIAL NOTER I"""
    if isStandard(automate):
        print("L'automate est déjà standard")
        return
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

