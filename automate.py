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

def Determinisation(automate):
    # Permet de déterminiser un automate sans renommer les états

    initialStates = automate["initialStates"]

    new_states = {}
    new_transitions = []
    queue = [tuple(sorted(automate["initialStates"]))]
    new_initial_state = queue[0]
    new_final_states = set()

    alphabet = getAlphabet(automate)

    print("\nDébut de l'algorithme de déterminisation :")
    print(f"\n\nÉtats initiaux : {queue}")

    while queue:
        current_set = queue.pop(0)
        if current_set not in new_states:
            new_states[current_set] = current_set

        print(f"\n Traitement de l'ensemble d'états {current_set}")

        for symbol in alphabet:
            next_set = tuple(sorted([
                int(state_to) if isinstance(state_to, str) and state_to.isdigit() else state_to
                for state_from, sym, state_to in automate["transitions"]
                if state_from in current_set and sym == symbol
            ], key=lambda x: str(x)))

            print(f"- Transition avec '{symbol}' mène à {next_set}")
            if next_set:
                if next_set not in new_states:
                    new_states[next_set] = next_set
                    queue.append(next_set)
                    print(f"Ajout d'un nouvel état : {next_set}")
                new_transitions.append((current_set, symbol, next_set))
                if set(next_set) & set(automate["finalStates"]):
                    new_final_states.add(next_set)
                    print(f"L'état {next_set} est final")

    afd = {
        "numStates": len(new_states),
        "initialStates": {new_initial_state},
        "finalStates": new_final_states,
        "transitions": new_transitions
    }

    print("\nFin de l'algorithme de déterminisation")
    print("\n Automate déterminisé")
    return afd




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




