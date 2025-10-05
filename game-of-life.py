import tkinter as tk
from pathlib import Path
import sys

def draw_grid(n, cell_size):
    root = tk.Tk()
    root.title("Conway's Game of Life")
    
    window_size = n * cell_size
    
    root.geometry(f"{window_size}x{window_size}")
    
    canvas = tk.Canvas(root, width=window_size, height=window_size, bg="black")
    canvas.pack()

    states = [[0 for _ in range(n)] for _ in range(n)]
    grid = [["black" for _ in range(n)] for _ in range(n)]

    ids = [[None for _ in range(n)] for _ in range(n)]

    try:
        filename = Path(sys.argv[1])
    
        if filename.is_file():
            with filename.open("r") as f:
                for y, line in enumerate(f):
                    for x, c in enumerate(line.strip()):
                        states[y][x] = int(c)
                        
                for y in range(n):
                    for x in range(n):
                        grid[y][x] = "white" if states[y][x] else "black"
    except IndexError:
        pass
    
    for y in range(n):
        for x in range(n):
            x1 = x * cell_size
            x2 = x1 + cell_size

            y1 = y * cell_size
            y2 = y1 + cell_size

            ids[y][x] = canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill=grid[y][x])

    def on_click(event):
        col = event.x // cell_size
        row = event.y // cell_size

        if 0 <= row < n and 0 <= col < n:
            grid[row][col] = "white" if grid[row][col] == "black" else "black"

            states[row][col] = 1 if states[row][col] == 0 else 0

            canvas.itemconfig(ids[row][col], fill=grid[row][col])

    def cell_tick(x, y):
        live_count = 0

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i == x and j == y) or i < 0 or j < 0 or i >= n or j >= n:
                    continue
                
                live_count += states[i][j]

        current_state = states[x][y]
    
        if not current_state and live_count == 3:
            return 1

        if current_state and (live_count < 2 or live_count > 3):
            return 0
        
        if current_state and (live_count == 2 or live_count == 3):
            return 1
    
        return current_state

    is_ticking = False

    def tick():
        new_states = [[0 for _ in range(n)] for _ in range(n)]

        for row in range(n):
            for col in range(n):
                new_states[row][col] = cell_tick(row, col)
                grid[row][col] = "white" if new_states[row][col] else "black"
                

                canvas.itemconfig(ids[row][col], fill=grid[row][col])

        nonlocal states
        states = new_states

        if is_ticking:
            root.after(100, tick)
        
    def start(_):
        nonlocal is_ticking

        if is_ticking:
            is_ticking = False

        else:
            is_ticking = True
            tick()
            
    def save_state(_):
        nonlocal states

        with open("state.txt", "w") as f:
            for row in states:
                f.write("".join(map(str, row)) + "\n")

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<Button-2>", save_state)
    canvas.bind("<Button-3>", start)

    root.mainloop()

draw_grid(100, 20)
