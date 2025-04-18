import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class NFA:
    def __init__(self, states, alphabet, start_state, accept_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def get_epsilon_closure(self, states):
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
        self.base_input = ""
        self.infinite_mode = tk.BooleanVar()

        self.create_widgets()

    def create_widgets(self):
        self.states = {'q0', 'q1', 'q2', 'q3', 'q4'}
        self.alphabet = {'0', '1', 'a', 'b'}
        self.start_state = 'q0'
        self.accept_states = {'q3', 'q4'}
        self.transitions = {
            ('q0', '0'): {'q1'},
            ('q0', 'a'): {'q2'},
            ('q1', '1'): {'q3'},
            ('q2', 'b'): {'q4'},
            ('q1', '0'): {'q1', 'q2'},
            ('q2', 'a'): {'q2', 'q1'},
            ('q0', None): {'q0'},
            ('q3', '0'): {'q3'},
            ('q3', '1'): {'q4'},
            ('q4', 'a'): {'q3'},
            ('q4', 'b'): {'q4'},
            ('q1', 'a'): set(),
            ('q2', '0'): set(),
        }
        self.nfa = NFA(self.states, self.alphabet, self.start_state, self.accept_states, self.transitions)

        self.label = tk.Label(self.root, text="Cadena de entrada (ej: 01ab):")
        self.label.pack()

        self.entry = tk.Entry(self.root, font=("Courier", 16), textvariable=self.input_string)
        self.entry.pack()

        self.infinite_checkbox = tk.Checkbutton(self.root, text="Modo cadena infinita", variable=self.infinite_mode)
        self.infinite_checkbox.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Iniciar Simulación", command=self.start_simulation)
        self.start_button.pack(pady=5)

        self.next_button = tk.Button(self.root, text="Siguiente Paso", command=self.next_step, state=tk.DISABLED)
        self.next_button.pack(pady=5)

        self.prev_button = tk.Button(self.root, text="Paso Anterior", command=self.prev_step, state=tk.DISABLED)
        self.prev_button.pack(pady=5)

        self.reset_button = tk.Button(self.root, text="Reiniciar", command=self.reset_simulation, state=tk.DISABLED)
        self.reset_button.pack(pady=5)

        self.output = tk.Label(self.root, text="", font=("Courier", 20))
        self.output.pack(pady=10)

        self.state_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.state_label.pack()

        self.reason_label = tk.Label(self.root, text="", font=("Arial", 12), fg="red")
        self.reason_label.pack(pady=5)

        self.transition_table_label = tk.Label(self.root, text="Tabla de Transiciones:", font=("Arial", 12, "bold"))
        self.transition_table_label.pack(pady=5)

        columns = ["Paso", "Símbolo", "Estados Previos", "Transición", "Nuevos Estados"]
        self.transition_table = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for col in columns:
            self.transition_table.heading(col, text=col)
            self.transition_table.column(col, width=120, anchor="center")
        self.transition_table.pack(pady=10)

    def start_simulation(self):
        tape_input = self.input_string.get().strip()
        if not tape_input and not self.infinite_mode.get():
            return

        self.base_input = tape_input if not self.infinite_mode.get() else (tape_input or "01ab")

        self.simulation_steps = []
        initial_states = self.nfa.get_epsilon_closure({self.nfa.start_state})
        self.simulation_steps.append(("Inicio", "", frozenset({self.nfa.start_state}), "", initial_states))
        self.update_output(initial_states)
        self.next_button.config(state=tk.NORMAL)
        self.prev_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
        self.current_step_index = 0
        self.reason_label.config(text="")
        self.populate_simulation_steps_table()

    def next_step(self):
        if self.infinite_mode.get():
            symbol = self.base_input[self.current_step_index % len(self.base_input)]
        else:
            input_str = self.input_string.get()
            if self.current_step_index >= len(input_str):
                return
            symbol = input_str[self.current_step_index]

        previous_states = self.simulation_steps[-1][4]

        if symbol not in self.nfa.alphabet:
            self.output.config(text=f"Símbolo '{symbol}' no en el alfabeto.")
            self.next_button.config(state=tk.DISABLED)
            return

        next_states, used_transitions = self.nfa.simulate_step(previous_states, symbol)
        if next_states is None or not next_states:
            self.output.config(text=f"Cadena rechazada en símbolo '{symbol}'")
            self.reason_label.config(text="No hay transición válida desde los estados actuales.")
            self.next_button.config(state=tk.DISABLED)
            return

        transition_str = ", ".join([f"({s}, '{a}') -> {d}" for (s, a), d in used_transitions])
        self.simulation_steps.append((f"Paso {self.current_step_index + 1}", symbol, previous_states, transition_str, next_states))
        self.update_output(next_states)
        self.current_step_index += 1
        self.populate_simulation_steps_table()

        if not self.infinite_mode.get():
            input_str = self.input_string.get()
            if self.current_step_index == len(input_str):
                if any(state in self.nfa.accept_states for state in next_states):
                    self.state_label.config(text=f"Cadena aceptada. Estados finales: {sorted(list(next_states))}")
                    self.reason_label.config(text="")
                else:
                    self.state_label.config(text=f"Cadena rechazada. Estados finales: {sorted(list(next_states))}")
                    self.reason_label.config(text="Ninguno de los estados finales es de aceptación.")
                self.next_button.config(state=tk.DISABLED)

        self.prev_button.config(state=tk.NORMAL)

    def prev_step(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.update_output(self.simulation_steps[self.current_step_index][4])
            self.populate_simulation_steps_table()
            self.next_button.config(state=tk.NORMAL)
            self.reason_label.config(text="")
            if self.current_step_index == 0:
                self.prev_button.config(state=tk.DISABLED)

    def reset_simulation(self):
        self.input_string.set("")
        self.simulation_steps = []
        self.current_step_index = -1
        self.output.config(text="")
        self.state_label.config(text="")
        self.reason_label.config(text="")
        self.populate_simulation_steps_table()
        self.next_button.config(state=tk.DISABLED)
        self.prev_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)

    def update_output(self, current_states):
        self.output.config(text=f"Estados actuales: {sorted(list(current_states))}")
        self.state_label.config(text=f"Estado actual (conjunto): {sorted(list(current_states))}")

    def populate_simulation_steps_table(self):
        for row in self.transition_table.get_children():
            self.transition_table.delete(row)
        for step_data in self.simulation_steps:
            self.transition_table.insert("", "end", values=step_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = NFA_GUI(root)
    root.mainloop()
