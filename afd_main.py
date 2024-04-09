import json
import sys
import os
from graphviz import Digraph

class AFD:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.initial_state = None
        self.final_states = set()
        self.transitions = {}

    def load_from_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.states = set(data['states'])
            self.alphabet = set(data['alphabet'])
            self.initial_state = data['initial_state']
            self.final_states = set(data['final_states'])
            self.transitions = data['transitions']

    def draw_graphviz(self):
        # Definir o caminho para o executável dot usando a variável de ambiente PATH
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
        
        dot = Digraph()
        dot.attr(rankdir='LR')
        dot.node('start', shape='point')
        dot.edge('start', self.initial_state)
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)
        for from_state, transitions in self.transitions.items():
            for symbol, to_state in transitions.items():
                dot.edge(from_state, to_state, label=symbol)
        dot.render('afd_graph', format='png', cleanup=True)
        dot.save('afd_graph.dot')

    def save_path(self, word, path):
        with open('path.txt', 'w') as file:
            file.write(f"Word: {word}\nPath: {'->'.join(path)}")

    def recognize_word(self, word):
        current_state = self.initial_state
        path = [current_state]
        for symbol in word:
            if symbol not in self.alphabet:
                return f"'{word}' não é reconhecida\n[símbolo '{symbol}' não pertence ao alfabeto]"
            if current_state not in self.transitions or symbol not in self.transitions[current_state]:
                return f"'{word}' não é reconhecida\n[símbolo '{symbol}' não possui transição a partir do estado '{current_state}']"
            current_state = self.transitions[current_state][symbol]
            path.append(current_state)
        if current_state in self.final_states:
            self.save_path(word, path)
            return f"'{word}' é reconhecida\n[ caminho {'->'.join(path)}]"
        else:
            return f"'{word}' não é reconhecida\n[caminho {'->'.join(path)}, {current_state} não é final]"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python afd_main.py <file.json> [-graphviz | -rec <word>]")
        sys.exit(1)

    afd = AFD()
    afd.load_from_json(sys.argv[1])

    if "-graphviz" in sys.argv:
        afd.draw_graphviz()
        print("Graphviz representation generated as 'afd_graph.png' and 'afd_graph.dot'")
    elif "-rec" in sys.argv:
        word_index = sys.argv.index("-rec") + 1
        if word_index < len(sys.argv):
            word = sys.argv[word_index]
            result = afd.recognize_word(word)
            print(result)
        else:
            print("No word provided for recognition.")
    else:
        print("Invalid command.")
