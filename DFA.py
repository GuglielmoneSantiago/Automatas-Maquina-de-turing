import tkinter as tk
from tkinter import ttk

class DFA:
    def __init__(self, transitions, initial_state, final_states):
        self.transitions = transitions
        self.state = initial_state
        self.initial_state = initial_state
        self.final_states = final_states
        self.input_string = ""
        self.position = 0

    def reset(self, input_string):
        self.input_string = input_string
        self.position = 0
        self.state = self.initial_state

    def step(self):
        if self.position >= len(self.input_string):
            return False

        symbol = self.input_string[self.position]
        if (self.state, symbol) in self.transitions:
            self.state = self.transitions[(self.state, symbol)]
            self.position += 1
            return True
        else:
            return False

    def is_accepting(self):
        return self.state in self.final_states

# GUI
class DFAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de DFA - Reconoce '0' seguido de '1'")

        self.label = tk.Label(root, text="Ingrese una cadena (0's y 1's):")
        self.label.pack()

        self.entry = tk.Entry(root, font=("Courier", 16))
        self.entry.pack()

        self.start_button = tk.Button(root, text="Iniciar Simulación", command=self.start_simulation)
        self.start_button.pack(pady=5)

        self.step_button = tk.Button(root, text="Paso a Paso", command=self.step, state=tk.DISABLED)
        self.step_button.pack(pady=5)

        self.output = tk.Label(root, text="", font=("Courier", 20))
        self.output.pack(pady=10)

        self.state_label = tk.Label(root, text="", font=("Arial", 14))
        self.state_label.pack()

        self.transition_table_label = tk.Label(root, text="Tabla de Transiciones:", font=("Arial", 12, "bold"))
        self.transition_table_label.pack(pady=5)

        self.transition_table = ttk.Treeview(root, columns=("state", "symbol", "new_state"), show="headings", height=6)
        for col in self.transition_table["columns"]:
            self.transition_table.heading(col, text=col.capitalize())
            self.transition_table.column(col, width=100, anchor="center")
        self.transition_table.pack(pady=10)

    def start_simulation(self):
        input_string = self.entry.get().strip()
        if input_string == "":
            return

        # Validar que solo haya '0' y '1'
        for c in input_string:
            if c not in ("0", "1"):
                self.state_label.config(text="Error: Solo se permiten 0's y 1's.")
                return

        self.transitions = {
            ("q0", "0"): "q1",
            ("q0", "1"): "q0",
            ("q1", "0"): "q1",
            ("q1", "1"): "q2",
            ("q2", "0"): "q2",
            ("q2", "1"): "q2"
        }

        self.dfa = DFA(self.transitions, "q0", {"q2"})
        self.dfa.reset(input_string)
        self.update_output()
        self.populate_transition_table()
        self.step_button.config(state=tk.NORMAL)

    def populate_transition_table(self):
        for row in self.transition_table.get_children():
            self.transition_table.delete(row)
        for (state, symbol), new_state in self.transitions.items():
            self.transition_table.insert("", "end", values=(state, symbol, new_state))

    def step(self):
        if self.dfa.step():
            self.update_output()
        else:
            self.update_output()
            if self.dfa.is_accepting():
                self.state_label.config(text=f"Cadena ACEPTADA en estado: {self.dfa.state}")
            else:
                self.state_label.config(text=f"Cadena RECHAZADA en estado: {self.dfa.state}")
            self.step_button.config(state=tk.DISABLED)

    def update_output(self):
        display = ""
        for i, symbol in enumerate(self.dfa.input_string):
            if i == self.dfa.position:
                display += f"[{symbol}]"
            else:
                display += f" {symbol} "
        self.output.config(text=display)
        self.state_label.config(text=f"Estado actual: {self.dfa.state}")

# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    app = DFAGUI(root)
    root.mainloop()
