
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

def getAlphabet(automaton):
    alphabet = set()  # Utilisation d'un ensemble pour éviter les doublons

    for transitions in automaton["transitions"]:
        for symbol in transitions:
            alphabet.add(symbol)

    return alphabet