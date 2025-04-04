import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class NFA:
    def __init__(self, states, alphabet, start_state, accept_states, transitions):
        """
        Inicializa el Autómata Finito No Determinista (AFND).

        Args:
            states (set): Conjunto de estados.
            alphabet (set): Conjunto de símbolos del alfabeto de entrada.
            start_state (str): Estado inicial del autómata.
            accept_states (set): Conjunto de estados de aceptación.
            transitions (dict): Función de transición, un diccionario donde la clave es una tupla
                                (estado actual, símbolo de entrada) y el valor es un conjunto de
                                posibles siguientes estados. Para transiciones epsilon (sin consumir entrada),
                                la clave es (estado actual, None).
        """
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def get_epsilon_closure(self, states):
        """
        Calcula la clausura epsilon de un conjunto de estados.
        """
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            epsilon_transitions = self.transitions.get((state, None), set())
            for next_state in epsilon_transitions:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return frozenset(closure)

    def simulate_step(self, current_states, symbol):
        """
        Realiza un paso de la simulación del AFND.
        """
        if symbol not in self.alphabet and symbol is not None:
            return None

        next_states = set()
        used_transitions = []
        for state in current_states:
            possible_transitions = self.transitions.get((state, symbol), set())
            if possible_transitions:
                next_states.update(possible_transitions)
                for next_s in possible_transitions:
                    used_transitions.append(((state, symbol), next_s))

        return self.get_epsilon_closure(next_states), used_transitions

class NFA_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Autómata Finito No Determinista (AFND)")

        self.nfa = None
        self.input_string = tk.StringVar()
        self.simulation_steps = []
        self.current_step_index = -1

        self.create_widgets()

    def create_widgets(self):
        # Definición del AFND con alfabeto {0, 1, a, b}
        self.states = {'q0', 'q1', 'q2', 'q3'}
        self.alphabet = {'0', '1', 'a', 'b'}
        self.start_state = 'q0'
        self.accept_states = {'q3'}
        self.transitions = {
            ('q0', '0'): {'q1'},
            ('q0', 'a'): {'q2'},
            ('q1', '1'): {'q3'},
            ('q2', 'b'): {'q3'},
            ('q1', '0'): {'q1'},
            ('q2', 'a'): {'q2'},
            ('q0', None): {'q0'},
            ('q3', '0'): {'q3'},
            ('q3', '1'): {'q3'},
            ('q3', 'a'): {'q3'},
            ('q3', 'b'): {'q3'},
        }
        self.nfa = NFA(self.states, self.alphabet, self.start_state, self.accept_states, self.transitions)

        self.label = tk.Label(self.root, text="Cadena de entrada (ej: 01ab):")
        self.label.pack()

        self.entry = tk.Entry(self.root, font=("Courier", 16))
        self.entry.pack()

        self.start_button = tk.Button(self.root, text="Iniciar Simulación", command=self.start_simulation)
        self.start_button.pack(pady=5)

        self.next_button = tk.Button(self.root, text="Siguiente Paso", command=self.next_step, state=tk.DISABLED)
        self.next_button.pack(pady=5)

        self.prev_button = tk.Button(self.root, text="Paso Anterior", command=self.prev_step, state=tk.DISABLED)
        self.prev_button.pack(pady=5)

        self.output = tk.Label(self.root, text="", font=("Courier", 20))
        self.output.pack(pady=10)

        self.state_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.state_label.pack()

        # Tabla de transiciones
        self.transition_table_label = tk.Label(self.root, text="Tabla de Transiciones:", font=("Arial", 12, "bold"))
        self.transition_table_label.pack(pady=5)

        columns = ["Paso", "Símbolo", "Estados Previos", "Transición", "Nuevos Estados"]
        self.transition_table = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for col in columns:
            self.transition_table.heading(col, text=col)
            self.transition_table.column(col, width=120, anchor="center")
        self.transition_table.pack(pady=10)

        self.populate_transition_table()

    def populate_transition_table(self):
        for row in self.transition_table.get_children():
            self.transition_table.delete(row)
        sorted_transitions = sorted(self.nfa.transitions.items(), key=lambda item: (item[0][0], item[0][1] or ''))
        # No vamos a mostrar todas las reglas estáticas aquí, sino los pasos de la simulación

    def start_simulation(self):
        tape_input = self.entry.get().strip()
        if not tape_input:
            return

        self.simulation_steps = []
        initial_states = self.nfa.get_epsilon_closure({self.nfa.start_state})
        self.simulation_steps.append(("Inicio", "", frozenset({self.nfa.start_state}), "", initial_states))
        self.update_output(initial_states)
        self.next_button.config(state=tk.NORMAL)
        self.prev_button.config(state=tk.DISABLED)
        self.input_string.set(tape_input)
        self.current_step_index = 0
        self.populate_simulation_steps_table()

    def next_step(self):
        input_str = self.input_string.get()
        if self.current_step_index < len(input_str):
            symbol = input_str[self.current_step_index]
            previous_states = self.simulation_steps[-1][4]  # Obtener los estados del paso anterior

            if previous_states is None:
                self.output.config(text="Error durante la simulación.")
                self.next_button.config(state=tk.DISABLED)
                return

            if symbol not in self.nfa.alphabet:
                self.output.config(text=f"Símbolo '{symbol}' no en el alfabeto.")
                self.next_button.config(state=tk.DISABLED)
                return

            next_states, used_transitions = self.nfa.simulate_step(previous_states, symbol)

            if next_states is None:
                self.output.config(text="No hay transición definida.")
                self.next_button.config(state=tk.DISABLED)
                return

            transition_str = ""
            if used_transitions:
                transition_str = ", ".join([f"({state}, '{sym}') -> {next_s}" for (state, sym), next_s in used_transitions])

            self.simulation_steps.append((f"Paso {self.current_step_index + 1}", symbol, previous_states, transition_str, next_states))
            self.update_output(next_states)
            self.current_step_index += 1
            self.populate_simulation_steps_table()

            if self.current_step_index == len(input_str):
                if any(state in self.nfa.accept_states for state in next_states):
                    self.state_label.config(text=f"Cadena aceptada. Estados finales: {sorted(list(next_states))}")
                else:
                    self.state_label.config(text=f"Cadena rechazada. Estados finales: {sorted(list(next_states))}")
                self.next_button.config(state=tk.DISABLED)
        elif self.current_step_index == len(input_str):
            final_states = self.simulation_steps[-1][4]
            if final_states:
                if any(state in self.nfa.accept_states for state in final_states):
                    self.state_label.config(text=f"Cadena aceptada. Estados finales: {sorted(list(final_states))}")
                else:
                    self.state_label.config(text=f"Cadena rechazada. Estados finales: {sorted(list(final_states))}")
            self.next_button.config(state=tk.DISABLED)

        self.prev_button.config(state=tk.NORMAL)

    def prev_step(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.update_output(self.simulation_steps[self.current_step_index][4])
            self.populate_simulation_steps_table()
            self.next_button.config(state=tk.NORMAL)
            if self.current_step_index == 0:
                initial_states = self.nfa.get_epsilon_closure({self.nfa.start_state})
                self.update_output(initial_states)
                self.prev_button.config(state=tk.DISABLED)
        elif self.current_step_index == 0:
            initial_states = self.nfa.get_epsilon_closure({self.nfa.start_state})
            self.update_output(initial_states)
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.NORMAL)

    def update_output(self, current_states):
        self.output.config(text=f"Estados actuales: {sorted(list(current_states))}")
        self.state_label.config(text=f"Estado actual (conjunto): {sorted(list(current_states))}")

    def populate_simulation_steps_table(self):
        for row in self.transition_table.get_children():
            self.transition_table.delete(row)
        for step_data in self.simulation_steps:
            self.transition_table.insert("", "end", values=step_data)

# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    app = NFA_GUI(root)
    root.mainloop()