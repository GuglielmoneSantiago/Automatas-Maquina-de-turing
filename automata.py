class TuringMachine:
    def __init__(self, tape, transitions, initial_state, final_states):
        self.tape = list(tape)  # Cinta representada como una lista
        self.head = 0  # Posición del cabezal de lectura/escritura
        self.state = initial_state  # Estado actual
        self.transitions = transitions  # Tabla de transición
        self.final_states = final_states  # Conjunto de estados finales

    def step(self):
        """Ejecuta un paso en la Máquina de Turing."""
        symbol = self.tape[self.head]  # Leer símbolo actual
        if (self.state, symbol) in self.transitions:
            new_state, new_symbol, move = self.transitions[(self.state, symbol)]
            self.tape[self.head] = new_symbol  # Escribir nuevo símbolo
            self.state = new_state  # Cambiar de estado
            
            # Mover cabezal
            if move == "R":
                self.head += 1
                if self.head >= len(self.tape):  # Expansión de cinta si es necesario
                    self.tape.append("_")  # Se usa "_" como símbolo en blanco
            elif move == "L":
                if self.head > 0:
                    self.head -= 1
            return True
        return False  # No hay más transiciones posibles

    def run(self):
        """Ejecuta la Máquina de Turing hasta llegar a un estado final."""
        while self.state not in self.final_states:
            if not self.step():
                break  # Detener si no hay más transiciones
        return "".join(self.tape)  # Devolver contenido de la cinta

# Definición de una máquina simple que cambia '0' por '1'
tape = "0000_"  # Cinta de entrada
transitions = {
    ("q0", "0"): ("q0", "1", "R"),
    ("q0", "_"): ("qf", "_", "S")  # Estado final cuando encuentra '_'
}
initial_state = "q0"
final_states = {"qf"}

tm = TuringMachine(tape, transitions, initial_state, final_states)
resultado = tm.run()
print("Resultado de la cinta:", resultado)
