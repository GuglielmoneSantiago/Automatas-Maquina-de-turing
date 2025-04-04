import tkinter as tk
from tkinter import ttk

class TuringMachine:
    def __init__(self, tape, transitions, initial_state, final_states):
        self.tape = list(tape)
        self.head = 0
        self.state = initial_state
        self.transitions = transitions
        self.final_states = final_states
        if "_" not in self.tape:
            self.tape.append("_")

    def step(self):
        if self.state in self.final_states:
            return False

        symbol = self.tape[self.head]
        key = (self.state, symbol)
        if key in self.transitions:
            new_state, new_symbol, move = self.transitions[key]
            self.tape[self.head] = new_symbol
            self.state = new_state

            if move == "R":
                self.head += 1
                if self.head >= len(self.tape):
                    self.tape.append("_")
            elif move == "L":
                if self.head > 0:
                    self.head -= 1
            return True
        else:
            return False

# GUI
class TuringGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Turing")

        self.label = tk.Label(root, text="Cinta de entrada (ej: 0000):")
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

        # Tabla de transiciones
        self.transition_table_label = tk.Label(root, text="Tabla de Transiciones:", font=("Arial", 12, "bold"))
        self.transition_table_label.pack(pady=5)

        self.transition_table = ttk.Treeview(root, columns=("state", "symbol", "new_state", "write", "move"), show="headings", height=5)
        for col in self.transition_table["columns"]:
            self.transition_table.heading(col, text=col.capitalize())
            self.transition_table.column(col, width=90, anchor="center")
        self.transition_table.pack(pady=10)

    def start_simulation(self):
        tape_input = self.entry.get().strip()
        if tape_input == "":
            return

        self.transitions = {
            ("q0", "0"): ("q0", "1", "R"),
            ("q0", "1"): ("q0", "0", "R"),
            ("q0", "_"): ("qf", "_", "S")
        }

        self.tm = TuringMachine(tape_input, self.transitions, "q0", {"qf"})
        self.update_output()
        self.populate_transition_table()
        self.step_button.config(state=tk.NORMAL)

    def populate_transition_table(self):
        for row in self.transition_table.get_children():
            self.transition_table.delete(row)
        for (state, symbol), (new_state, write, move) in self.transitions.items():
            self.transition_table.insert("", "end", values=(state, symbol, new_state, write, move))

    def step(self):
        if self.tm.step():
            self.update_output()
        else:
            self.update_output()
            self.state_label.config(text=f"Estado final alcanzado: {self.tm.state}")
            self.step_button.config(state=tk.DISABLED)

    def update_output(self):
        display = ""
        for i, symbol in enumerate(self.tm.tape):
            if i == self.tm.head:
                display += f"[{symbol}]"
            else:
                display += f" {symbol} "
        self.output.config(text=display)
        self.state_label.config(text=f"Estado actual: {self.tm.state}")

# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    app = TuringGUI(root)
    root.mainloop()