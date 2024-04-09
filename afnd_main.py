import json
import sys

def epsilon_closure(states, transitions, current_states):
    closure = set(current_states)
    stack = list(current_states)
    
    while stack:
        state = stack.pop()
        for transition in transitions:
            if transition['from'] == state and transition['symbol'] is None:
                new_state = transition['to']
                if new_state not in closure:
                    closure.add(new_state)
                    stack.append(new_state)
    
    return sorted(list(closure))

def move(states, transitions, current_states, symbol):
    moved_states = set()
    for state in current_states:
        for transition in transitions:
            if transition['from'] == state and transition['symbol'] == symbol:
                moved_states.add(transition['to'])
    return sorted(list(moved_states))

def convert_afnd_to_afd(states, initial_state, final_states, transitions):
    afnd_afd = {
        "states": [],
        "initial_state": None,
        "final_states": [],
        "transitions": []
    }
    
    queue = [epsilon_closure(states, transitions, [initial_state])]
    afnd_afd["states"].append(queue[0])
    afnd_afd["initial_state"] = queue[0]
    
    while queue:
        current_states = queue.pop(0)
        
        for symbol in ['a', 'b']:  # considering alphabet a, b
            next_states = epsilon_closure(states, transitions, move(states, transitions, current_states, symbol))
            if next_states:
                if next_states not in afnd_afd["states"]:
                    queue.append(next_states)
                    afnd_afd["states"].append(next_states)
                
                afnd_afd["transitions"].append({"from": current_states, "to": next_states, "symbol": symbol})
    
    for state in afnd_afd["states"]:
        if any(s in state for s in final_states):
            afnd_afd["final_states"].append(state)
    
    return afnd_afd

def process_expression(expression_json):
    # Processar a expressão e construir o AFND
    # Substitua esta função pela lógica adequada para processar a expressão regular
    pass

def main():
    if len(sys.argv) != 4:
        print("Uso: python afnd_main.py arquivo_afnd.json --output afd.json")
        return
    
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[3]

    # Ler o AFND do arquivo JSON
    with open(arquivo_entrada, 'r') as f:
        afnd_data = json.load(f)

    # Convert AFND to AFD
    afd_data = convert_afnd_to_afd(afnd_data["states"], afnd_data["initial_state"], afnd_data["final_states"], afnd_data["transitions"])

    # Escrever o AFD no arquivo JSON de saída
    with open(arquivo_saida, 'w') as f:
        json.dump(afd_data, f, indent=4)

    print("AFD successfully written to", arquivo_saida)

if __name__ == "__main__":
    main()
