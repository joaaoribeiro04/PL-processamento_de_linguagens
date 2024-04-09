import json
import sys


def process_expression(expr):
    if "simb" in expr:
        return build_simple_afnd(expr["simb"])
    op = expr["op"]  
    args = expr["args"]
    if op == "alt":
        return build_alternative_afnd([process_expression(arg) for arg in args])
    elif op == "seq":
        return build_sequence_afnd([process_expression(arg) for arg in args])
    elif op == "kle":
        return build_kleene_afnd(process_expression(args[0]))


def build_simple_afnd(simb):
    return {
        "states": [0, 1],
        "initial_state": 0,
        "final_states": [1],
        "transitions": [{"from": 0, "to": 1, "symbol": simb}],
    }


def build_alternative_afnd(afnds):
    new_initial_state = 0
    new_final_state = 1
    states = [new_initial_state, new_final_state]
    transitions = []
    final_states = [new_final_state]
    offset = 1

    for afnd in afnds:
        offset = max(states) + 1
        states.extend([state + offset for state in afnd["states"]])
        transitions.extend(
            [
                {
                    "from": transition["from"] + offset,
                    "to": transition["to"] + offset,
                    "symbol": transition["symbol"],
                }
                for transition in afnd["transitions"]
            ]
        )
        transitions.append(
            {
                "from": new_initial_state,
                "to": afnd["initial_state"] + offset,
                "symbol": None,
            }
        )  # ε-transition
        for final_state in afnd["final_states"]:
            transitions.append(
                {"from": final_state + offset, "to": new_final_state, "symbol": None}
            )  # ε-transition

    return {
        "states": list(set(states)),
        "initial_state": new_initial_state,
        "final_states": final_states,
        "transitions": transitions,
    }


def build_sequence_afnd(afnds):
    states = []
    transitions = []
    initial_state = None
    final_states = []
    offset = 0

    for i, afnd in enumerate(afnds):
        if i == 0:  # First AFND
            initial_state = offset
        else:  # Non-first AFNDs
            transitions.append(
                {
                    "from": prev_final_state,
                    "to": afnd["initial_state"] + offset,
                    "symbol": None,
                }
            )  # ε-transition

        states.extend([state + offset for state in afnd["states"]])
        transitions.extend(
            [
                {
                    "from": transition["from"] + offset,
                    "to": transition["to"] + offset,
                    "symbol": transition["symbol"],
                }
                for transition in afnd["transitions"]
            ]
        )
        prev_final_state = (
            afnd["final_states"][0] + offset
        )  # Assuming single final state for simplicity
        offset = max(states) + 1

    final_states = [prev_final_state]

    return {
        "states": list(set(states)),
        "initial_state": initial_state,
        "final_states": final_states,
        "transitions": transitions,
    }


def build_kleene_afnd(afnd):
    new_initial_state = 0
    new_final_state = max(afnd["states"]) + 1
    states = [state for state in afnd["states"]]
    states.append(new_initial_state)
    states.append(new_final_state)
    transitions = afnd["transitions"].copy()

    transitions.append(
        {"from": new_initial_state, "to": afnd["initial_state"], "symbol": None}
    )  # ε-transition
    for final_state in afnd["final_states"]:
        transitions.append(
            {"from": final_state, "to": afnd["initial_state"], "symbol": None}
        )  # ε-transition
    transitions.append(
        {"from": new_initial_state, "to": new_final_state, "symbol": None}
    )  # ε-transition

    return {
        "states": list(set(states)),
        "initial_state": new_initial_state,
        "final_states": [new_final_state],
        "transitions": transitions,
    }

def main():
    if len(sys.argv) != 4:
        print("Uso: python er_main.py arquivo_er.json --output afnd.json")
        return
    
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[3]

    # Ler a expressão regular do arquivo JSON
    with open(arquivo_entrada, 'r') as f:
        er_json = json.load(f)

    # Processar a expressão e construir o AFND
    afnd = process_expression(er_json)

    with open(arquivo_saida, 'w') as f:
        json.dump(afnd, f, indent=4)

if __name__ == "__main__":
    main()