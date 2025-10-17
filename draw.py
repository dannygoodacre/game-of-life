import tkinter as tk
from pathlib import Path

def draw(initial_state_file, width, height, cell_size):
    root = tk.Tk()

    root.title("Conway's Game of Life (stopped)")

    window_width = width * cell_size
    window_height = height * cell_size

    root.geometry(f"{window_width}x{window_height}")

    canvas = tk.Canvas(root, width=window_width, height=window_height, bg="black")
    canvas.pack()
    canvas.focus_set()

    states = [[0 for _ in range(width)] for _ in range(height)]

    grid = [["black" for _ in range(width)] for _ in range(height)]

    ids = [[None for _ in range(width)] for _ in range(height)]
    
    is_ticking = False

    delay = 100

    try:
        filename = Path(initial_state_file)

        if filename.is_file():
            with filename.open("r") as f:
                for y, line in enumerate(f):
                    for x, c in enumerate(line.strip()):
                        if x < width and y < height:
                            states[y][x] = int(c)
                            grid[y][x] = "white" if states[y][x] else "black"

    except IndexError:
        pass

    for y in range(height):
        for x in range(width):
            x1 = x * cell_size
            x2 = x1 + cell_size

            y1 = y * cell_size
            y2 = y1 + cell_size

            ids[y][x] = canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill=grid[y][x])

    def on_click(event):
        col = event.x // cell_size
        row = event.y // cell_size

        if 0 <= row < height and 0 <= col < width:
            grid[row][col] = "white" if grid[row][col] == "black" else "black"

            states[row][col] = 1 - states[row][col]

            canvas.itemconfig(ids[row][col], fill=grid[row][col])

    def cell_tick(x, y):
        live_count = 0

        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if i == y and j == x:
                    continue

                ii = i % height
                jj = j % width

                live_count += states[ii][jj]

        current_state = states[y][x]

        if not current_state and live_count == 3:
            return 1

        if current_state and (live_count < 2 or live_count > 3):
            return 0

        if current_state and (live_count == 2 or live_count == 3):
            return 1

        return current_state

    def tick():
        new_states = [[0 for _ in range(width)] for _ in range(height)]

        for row in range(height):
            for col in range(width):
                new_states[row][col] = cell_tick(col, row)

                grid[row][col] = "white" if new_states[row][col] else "black"

                canvas.itemconfig(ids[row][col], fill=grid[row][col])

        nonlocal states
        states = new_states

        if is_ticking:
            root.after(delay, tick)

    def start(_):
        nonlocal is_ticking

        if is_ticking:
            root.title("Conway's Game of Life (stopped)")

            is_ticking = False

        else:
            root.title("Conway's Game of Life (running)")

            is_ticking = True

            tick()

    def save_state(_):
        with open("state.txt", "w") as f:
            for row in states:
                f.write("".join(map(str, row)) + "\n")

    def speed_up(_):
        nonlocal delay

        if delay - 10 <= 0:
            return

        delay -= 10

    def slow_down(_):
        nonlocal delay

        delay += 50

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<Button-2>", save_state)
    canvas.bind("<Button-3>", start)
    canvas.bind("<Key-plus>", speed_up)
    canvas.bind("<Key-minus>", slow_down)

    root.mainloop()
