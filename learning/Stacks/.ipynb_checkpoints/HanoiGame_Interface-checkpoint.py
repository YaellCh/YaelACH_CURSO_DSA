import tkinter as tk
from tkinter import messagebox
from StackHanoi import Stack

root = tk.Tk()
root.title("Torres de Hanoi")

canvas = tk.Canvas(root, width=600, height=400, bg="lightgray")
canvas.pack()

info_label = tk.Label(root, text="Bienvenido a las Torres de Hanoi", font=("Arial", 14))
info_label.pack()

move_count_label = tk.Label(root, text="Movimientos: 0", font=("Arial", 12))
move_count_label.pack()

optimal_moves_label = tk.Label(root, text="Número óptimo de movimientos: 0", font=("Arial", 12))
optimal_moves_label.pack()

warning_label = tk.Label(root, text="", font=("Arial", 12))
warning_label.pack()

disk_input_label = tk.Label(root, text="Número de discos (máximo 8):", font=("Arial", 12))
disk_input_label.pack()

disk_input = tk.Entry(root)
disk_input.pack()

start_button = tk.Button(root, text="Iniciar Juego", command=lambda: start_game())
start_button.pack()

left_button = tk.Button(root, text="Pila Izquierda", command=lambda: select_stack(0))
left_button.pack(side="left", padx=10)

middle_button = tk.Button(root, text="Pila Media", command=lambda: select_stack(1))
middle_button.pack(side="left", padx=10)

right_button = tk.Button(root, text="Pila Derecha", command=lambda: select_stack(2))
right_button.pack(side="left", padx=10)

stacks = [Stack("Izquierda"), Stack("Media"), Stack("Derecha")]
num_disks = 0
num_optimal_moves = 0
move_count = 0
selected_stack = None

def start_game():
    global num_disks, num_optimal_moves, move_count, selected_stack
    try:
        num_disks = int(disk_input.get())
        if (num_disks < 3) or (num_disks > 8):
            raise ValueError
    except ValueError:
        warning_label.config(text="Por favor, ingresa un número válido de discos (máximo 8).", fg="red", font=("Arial", 12))
        return

    num_optimal_moves = (2 ** num_disks) - 1
    optimal_moves_label.config(text=f"Número óptimo de movimientos: {num_optimal_moves}")
    info_label.config(text=f"Juego iniciado con {num_disks} discos.")
    warning_label.config(text="", font=("Arial", 12))
    start_button.config(state="disabled")
    disk_input.config(state="disabled")

    stacks[0].top_item = None
    for disk in range(num_disks, 0, -1):
        stacks[0].push(disk)

    move_count = 0
    update_move_count()
    render_game()

def get_stack_items(stack_index):
    stack = stacks[stack_index]
    items = []
    pointer = stack.top_item
    while pointer:
        items.append(pointer.get_value())
        pointer = pointer.get_next_node()
    items.reverse()
    return items

def render_game():
    canvas.delete("all")
    render_stack(0, 150)
    render_stack(1, 300)
    render_stack(2, 450)

def render_stack(stack_index, x_position):
    stack_items = get_stack_items(stack_index)
    y_position = 300
    for i, disk in enumerate(stack_items):
        canvas.create_rectangle(x_position - disk * 15, y_position - i * 25, 
                                x_position + disk * 15, y_position - (i + 1) * 25, fill="green")
        canvas.create_text(x_position, y_position - i * 25 - 12, text=str(disk), fill="white")

def update_move_count():
    move_count_label.config(text=f"Movimientos: {move_count}")

def select_stack(stack_index):
    global selected_stack, move_count
    if (selected_stack is None):
        selected_stack = stack_index
        warning_label.config(text=f"Seleccionaste la pila {['Izquierda', 'Media', 'Derecha'][stack_index]}. Ahora selecciona una pila destino.", fg="blue", font=("Arial", 12))
    else:
        from_stack = stacks[selected_stack]
        to_stack = stacks[stack_index]

        if (is_valid_move(from_stack, to_stack)):
            disk = from_stack.pop()
            to_stack.push(disk)
            move_count += 1
            update_move_count()
            check_win()
        else:
            warning_label.config(text="Movimiento no válido.", fg="red", font=("Arial", 12))

        selected_stack = None
    render_game()

def is_valid_move(from_stack, to_stack):
    if (from_stack.get_size() == 0):
        return False
    if (to_stack.get_size() > 0) and (from_stack.peek() > to_stack.peek()):
        return False
    return True

def check_win():
    if (stacks[2].get_size() == num_disks):
        render_game()
        warning_label.config(text=f"¡Felicidades! ¡Completaste el juego en {move_count} movimientos!", fg="green", font=("Arial", 14, "bold"))

root.mainloop()
