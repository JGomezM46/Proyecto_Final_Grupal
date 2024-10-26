import tkinter as tk
from tkinter import scrolledtext

class TuringMachine:
    def __init__(self, tape, initial_state):
        self.tape = tape
        self.head_position = 0
        self.state = initial_state
        self.transitions = {}

    def add_transition(self, current_state, read_symbol, next_state, write_symbol, direction):
        self.transitions[(current_state, read_symbol)] = (next_state, write_symbol, direction)

    def step(self):
        read_symbol = self.tape[self.head_position]
        key = (self.state, read_symbol)

        if key in self.transitions:
            next_state, write_symbol, direction = self.transitions[key]
            self.tape[self.head_position] = write_symbol
            self.state = next_state
            if direction == 'R':
                self.head_position += 1
                if self.head_position == len(self.tape):
                    self.tape.append('B')  # Usar 'B' en lugar de ' ' para espacios vacíos
            elif direction == 'L':
                self.head_position = max(0, self.head_position - 1)
            return True  # máquina corriendo
        return False  # máquina se detiene

    def get_tape_content(self):
        tape_str = ''.join(self.tape)

        # cabezal iniciando
        if self.head_position < 0:
            return '[' + ' ' + ']' + tape_str

        # cabezal final de la cinta
        if self.head_position >= len(tape_str):
            return tape_str + '[' + ' ' + ']' 

        # cabezal dentro del rango de la cinta
        return tape_str[:self.head_position] + '[' + tape_str[self.head_position] + ']' + tape_str[self.head_position + 1:]

class TuringMachineSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Turing")

        # Variables de entrada
        self.states_input = tk.Entry(root)
        self.alphabet_input = tk.Entry(root)
        self.input_string = tk.Entry(root)
        self.current_state_input = tk.Entry(root)
        self.read_symbol_input = tk.Entry(root)
        self.next_state_input = tk.Entry(root)
        self.write_symbol_input = tk.Entry(root)
        self.direction_input = tk.Entry(root)

        # Botones
        self.add_transition_button = tk.Button(root, text="Agregar Transición", command=self.agregar_transicion)
        self.start_button = tk.Button(root, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.step_button = tk.Button(root, text="Paso a Paso", command=self.ejecutar_paso)
        self.reset_button = tk.Button(root, text="Reiniciar", command=self.reiniciar)  # Botón de reinicio

        # Área para ingresar datos
        self.tape_display = scrolledtext.ScrolledText(root, width=40, height=5)
        self.process_display = scrolledtext.ScrolledText(root, width=40, height=10)

        # Posicionan
        self.setup_layout()

        self.turing_machine = None
        self.tape = []

    def setup_layout(self):
        tk.Label(self.root, text="Estados (separados por comas):").grid(row=0, column=0)
        self.states_input.grid(row=0, column=1)

        tk.Label(self.root, text="Alfabeto (separado por comas):").grid(row=1, column=0)
        self.alphabet_input.grid(row=1, column=1)

        tk.Label(self.root, text="Cadena de Entrada:").grid(row=2, column=0)
        self.input_string.grid(row=2, column=1)
        self.start_button.grid(row=3, columnspan=2, pady=10)  # Botón iniciar aquí

        tk.Label(self.root, text="Estado Actual:").grid(row=4, column=0)
        self.current_state_input.grid(row=4, column=1)

        tk.Label(self.root, text="Símbolo leído:").grid(row=5, column=0)
        self.read_symbol_input.grid(row=5, column=1)

        tk.Label(self.root, text="Próximo Estado:").grid(row=6, column=0)
        self.next_state_input.grid(row=6, column=1)

        tk.Label(self.root, text="Símbolo a escribir:").grid(row=7, column=0)
        self.write_symbol_input.grid(row=7, column=1)

        tk.Label(self.root, text="Dirección (L/R):").grid(row=8, column=0)
        self.direction_input.grid(row=8, column=1)

        # Colocar botones de agregar transición y paso a paso en la misma línea
        self.add_transition_button.grid(row=9, column=0, pady=10)
        self.step_button.grid(row=9, column=1, pady=10)

        self.reset_button.grid(row=10, columnspan=2, pady=10)  # Botón reiniciar aquí

        tk.Label(self.root, text="Cinta de la Máquina de Turing:").grid(row=11, column=0)
        self.tape_display.grid(row=12, column=0, columnspan=2)

        tk.Label(self.root, text="Proceso de Simulación:").grid(row=13, column=0)
        self.process_display.grid(row=14, column=0, columnspan=2)

    def agregar_transicion(self):
        current_state = self.current_state_input.get()
        read_symbol = self.read_symbol_input.get()
        next_state = self.next_state_input.get()
        write_symbol = self.write_symbol_input.get()
        direction = self.direction_input.get()

        if self.turing_machine:
            self.turing_machine.add_transition(current_state, read_symbol, next_state, write_symbol, direction)
            self.process_display.insert(tk.END, f"Transición agregada: {current_state} -> {next_state}\n")
        else:
            self.process_display.insert(tk.END, "Inicia la simulación antes de agregar transiciones.\n")

        # Limpiar entradas
        self.current_state_input.delete(0, tk.END)
        self.read_symbol_input.delete(0, tk.END)
        self.next_state_input.delete(0, tk.END)
        self.write_symbol_input.delete(0, tk.END)
        self.direction_input.delete(0, tk.END)

    def iniciar_simulacion(self):
        self.tape = list(self.input_string.get()) + ['B']
        initial_state = self.states_input.get().split(',')[0]
        self.turing_machine = TuringMachine(self.tape, initial_state)
        self.tape_display.delete('1.0', tk.END)
        self.tape_display.insert(tk.END, self.turing_machine.get_tape_content())
        self.process_display.insert(tk.END, f"Simulación Iniciada con estado: {initial_state}\n")

    def ejecutar_paso(self):
        if self.turing_machine:
            running = self.turing_machine.step()
            self.tape_display.delete('1.0', tk.END)
            self.tape_display.insert(tk.END, self.turing_machine.get_tape_content())
            self.process_display.insert(tk.END, f"Estado Actual: {self.turing_machine.state}\n")

            if not running:
                if self.turing_machine.state == 'q_accept':
                    self.process_display.insert(tk.END, "Cadena aceptada.\n")
                else:
                    self.process_display.insert(tk.END, "Cadena rechazada.\n")
        else:
            self.process_display.insert(tk.END, "Debes iniciar la simulación antes de ejecutar los pasos.\n")

    def reiniciar(self):
        # Limpiar las entradas y las salidas
        self.states_input.delete(0, tk.END)
        self.alphabet_input.delete(0, tk.END)
        self.input_string.delete(0, tk.END)
        self.current_state_input.delete(0, tk.END)
        self.read_symbol_input.delete(0, tk.END)
        self.next_state_input.delete(0, tk.END)
        self.write_symbol_input.delete(0, tk.END)
        self.direction_input.delete(0, tk.END)

        self.tape_display.delete('1.0', tk.END)
        self.process_display.delete('1.0', tk.END)

        # Reiniciar la máquina
        self.turing_machine = None
        self.tape = []

# Ejecutar la aplicación
root = tk.Tk()
app = TuringMachineSimulator(root)
root.mainloop()
