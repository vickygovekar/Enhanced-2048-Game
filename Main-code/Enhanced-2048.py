import random
import time
import copy
import tkinter as tk
from tkinter import messagebox, ttk
import math

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("Enhanced 2048")
        self.master.geometry("600x750")
        self.master.resizable(False, False)
        
        # Game constants
        self.GRID_SIZE = 4
        self.CELL_SIZE = 100
        self.CELL_PADDING = 10
        
        # Game variables
        self.score = 0
        self.high_score = 0
        self.moves = 0
        self.game_over = False
        self.game_won = False
        self.time_left = 60  # For timed mode
        self.timed_mode = False
        self.timer_running = False
        
        # Undo feature
        self.undo_limit = 3
        self.undo_count = self.undo_limit
        self.previous_states = []
        
        # Features
        self.chaos_mode = False
        self.chaos_frequency = 10  # Trigger chaos every X moves
        
        # Special tiles
        self.special_tiles = {}  # (row, col): {'type': 'bomb', 'turns': 3}
        self.special_types = ['bomb', 'swapper', 'frozen']
        self.special_chance = 0.08  # 8% chance of a special tile
        
        # Missions
        self.missions = [
            {"description": "Merge a 64 tile", "goal_value": 64, "type": "merge", "completed": False},
            {"description": "Make 3 merges in one move", "goal_value": 3, "type": "combo", "completed": False},
            {"description": "Reach 500 points", "goal_value": 500, "type": "score", "completed": False}
        ]
        self.current_mission = random.choice(self.missions)
        self.combo_count = 0
        
        # Theme variables
        self.themes = {
            "Classic": {
                "bg": "#bbada0",
                "empty": "#cdc1b4",
                "colors": {
                    2: ("#776e65", "#eee4da"),
                    4: ("#776e65", "#ede0c8"),
                    8: ("#f9f6f2", "#f2b179"),
                    16: ("#f9f6f2", "#f59563"),
                    32: ("#f9f6f2", "#f67c5f"),
                    64: ("#f9f6f2", "#f65e3b"),
                    128: ("#f9f6f2", "#edcf72"),
                    256: ("#f9f6f2", "#edcc61"),
                    512: ("#f9f6f2", "#edc850"),
                    1024: ("#f9f6f2", "#edc53f"),
                    2048: ("#f9f6f2", "#edc22e"),
                    'bomb': ("#ffffff", "#000000"),
                    'swapper': ("#000000", "#00aaff"),
                    'frozen': ("#000000", "#b0c4de")
                }
            },
            "Dark": {
                "bg": "#2c3e50",
                "empty": "#34495e",
                "colors": {
                    2: ("#ffffff", "#1abc9c"),
                    4: ("#ffffff", "#16a085"),
                    8: ("#ffffff", "#3498db"),
                    16: ("#ffffff", "#2980b9"),
                    32: ("#ffffff", "#9b59b6"),
                    64: ("#ffffff", "#8e44ad"),
                    128: ("#ffffff", "#f1c40f"),
                    256: ("#ffffff", "#f39c12"),
                    512: ("#ffffff", "#e67e22"),
                    1024: ("#ffffff", "#d35400"),
                    2048: ("#ffffff", "#e74c3c"),
                    'bomb': ("#ffffff", "#7f8c8d"),
                    'swapper': ("#000000", "#2ecc71"),
                    'frozen': ("#ffffff", "#95a5a6")
                }
            },
            "Space": {
                "bg": "#0a0a2a",
                "empty": "#1a1a3a",
                "colors": {
                    2: ("#ffffff", "#3a3a5a"),
                    4: ("#ffffff", "#4a4a6a"),
                    8: ("#ffffff", "#5f5f8f"),
                    16: ("#ffffff", "#6f6f9f"),
                    32: ("#ffffff", "#8a8aaf"),
                    64: ("#ffffff", "#aaaaff"),
                    128: ("#f9f6f2", "#ccccff"),
                    256: ("#f9f6f2", "#5050ff"),
                    512: ("#f9f6f2", "#3030ff"),
                    1024: ("#f9f6f2", "#0000ff"),
                    2048: ("#f9f6f2", "#0000aa"),
                    'bomb': ("#ffffff", "#ff0000"),
                    'swapper': ("#000000", "#00ffff"),
                    'frozen': ("#ffffff", "#8888ff")
                }
            }
        }
        self.current_theme = "Classic"
        
        # Initialize grid
        self.grid = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        
        # Create UI
        self.create_widgets()
        
        # Start new game
        self.new_game()
        
        # Bind keys
        self.master.bind("<Key>", self.key_press)
                # keyboard shortcut: T to cycle themes
        self.master.bind("<t>", self._cycle_theme)
        self.master.bind("<T>", self._cycle_theme)

    def _cycle_theme(self, event):
        keys = list(self.themes.keys())
        idx = keys.index(self.current_theme)
        new = keys[(idx + 1) % len(keys)]
        self.change_theme(new)
        self._highlight_active_swatch()

        
    def create_widgets(self):
        # Top frame for scores and controls
        self.top_frame = tk.Frame(self.master, bg="#faf8ef")
        self.top_frame.pack(fill="x", padx=10, pady=10)
        
        # Title and score
        self.title_label = tk.Label(self.top_frame, text="2048+", font=("Arial", 30, "bold"), bg="#faf8ef", fg="#776e65")
        self.title_label.grid(row=0, column=0, pady=5)
        
        self.score_frame = tk.Frame(self.top_frame, bg="#bbada0", padx=15, pady=10, relief="raised", borderwidth=0)
        self.score_frame.grid(row=0, column=1, padx=10)
        
        tk.Label(self.score_frame, text="SCORE", font=("Arial", 10), bg="#bbada0", fg="#eee4da").pack()
        self.score_label = tk.Label(self.score_frame, text="0", font=("Arial", 16, "bold"), bg="#bbada0", fg="#ffffff")
        self.score_label.pack()
        
        self.highscore_frame = tk.Frame(self.top_frame, bg="#bbada0", padx=15, pady=10, relief="raised", borderwidth=0)
        self.highscore_frame.grid(row=0, column=2, padx=10)
        
        tk.Label(self.highscore_frame, text="BEST", font=("Arial", 10), bg="#bbada0", fg="#eee4da").pack()
        self.highscore_label = tk.Label(self.highscore_frame, text="0", font=("Arial", 16, "bold"), bg="#bbada0", fg="#ffffff")
        self.highscore_label.pack()
        
        # Timer frame
        self.timer_frame = tk.Frame(self.top_frame, bg="#bbada0", padx=15, pady=10, relief="raised", borderwidth=0)
        self.timer_frame.grid(row=0, column=3, padx=10)
        
        tk.Label(self.timer_frame, text="TIME", font=("Arial", 10), bg="#bbada0", fg="#eee4da").pack()
        self.time_label = tk.Label(self.timer_frame, text="60", font=("Arial", 16, "bold"), bg="#bbada0", fg="#ffffff")
        self.time_label.pack()
        
        # Controls and info frame
        self.controls_frame = tk.Frame(self.master, bg="#faf8ef")
        self.controls_frame.pack(fill="x", padx=10, pady=5)
        
        self.new_game_btn = tk.Button(self.controls_frame, text="New Game", font=("Arial", 12), bg="#8f7a66", fg="#ffffff", 
                                    command=self.new_game, relief="flat", padx=10, pady=5)
        self.new_game_btn.grid(row=0, column=0, padx=5)
        
        self.undo_btn = tk.Button(self.controls_frame, text=f"Undo ({self.undo_count})", font=("Arial", 12), bg="#8f7a66", fg="#ffffff", 
                                command=self.undo_move, relief="flat", padx=10, pady=5)
        self.undo_btn.grid(row=0, column=1, padx=5)
        
        self.hint_btn = tk.Button(self.controls_frame, text="Hint", font=("Arial", 12), bg="#8f7a66", fg="#ffffff", 
                                command=self.get_hint, relief="flat", padx=10, pady=5)
        self.hint_btn.grid(row=0, column=2, padx=5)
        
        # Toggle features
        self.features_frame = tk.Frame(self.master, bg="#faf8ef")
        self.features_frame.pack(fill="x", padx=10, pady=5)
        
        # Theme swatches — clickable color buttons
        swatch_frame = tk.Frame(self.features_frame, bg=self.features_frame['bg'])
        swatch_frame.grid(row=0, column=1, padx=5)

        tk.Label(self.features_frame, text="Theme:", font=("Arial",12),
                 bg=self.features_frame['bg'], fg="#776e65")\
            .grid(row=0, column=0, padx=5)

        self.theme_buttons = {}
        col = 0
        for name, data in self.themes.items():
            # use the board bg as the swatch color
            sw = tk.Button(swatch_frame,
                           bg=data['bg'],
                           width=3, height=1,
                           relief="raised", bd=2,
                           command=lambda n=name: self.change_theme(n))
            sw.grid(row=0, column=col, padx=2)
            self.theme_buttons[name] = sw
            col += 1

        # show which is active
        self._highlight_active_swatch()
        
        # Chaos mode toggle
        self.chaos_var = tk.BooleanVar(value=self.chaos_mode)
        self.chaos_check = tk.Checkbutton(self.features_frame, text="Chaos Mode", variable=self.chaos_var, 
                                        font=("Arial", 12), bg="#faf8ef", fg="#776e65", command=self.toggle_chaos)
        self.chaos_check.grid(row=0, column=2, padx=10)
        
        # Timed mode toggle
        self.timed_var = tk.BooleanVar(value=self.timed_mode)
        self.timed_check = tk.Checkbutton(self.features_frame, text="Timed Mode", variable=self.timed_var, 
                                        font=("Arial", 12), bg="#faf8ef", fg="#776e65", command=self.toggle_timed)
        self.timed_check.grid(row=0, column=3, padx=10)
        
        # Mission display
        self.mission_frame = tk.Frame(self.master, bg="#faf8ef", padx=10, pady=5)
        self.mission_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(self.mission_frame, text="Current Mission:", font=("Arial", 12, "bold"), bg="#faf8ef", fg="#776e65").pack(anchor="w")
        self.mission_label = tk.Label(self.mission_frame, text="", font=("Arial", 12), bg="#faf8ef", fg="#776e65")
        self.mission_label.pack(anchor="w")
        
        # Main game grid frame
        self.canvas_frame = tk.Frame(self.master, bg="#bbada0", padx=10, pady=10)
        self.canvas_frame.pack(padx=10, pady=10)
        
        # Create game grid cells
        self.cells = []
        for i in range(self.GRID_SIZE):
            row = []
            for j in range(self.GRID_SIZE):
                cell_frame = tk.Frame(self.canvas_frame, width=self.CELL_SIZE, height=self.CELL_SIZE, 
                                    bg="#cdc1b4", padx=self.CELL_PADDING, pady=self.CELL_PADDING)
                cell_frame.grid(row=i, column=j, padx=self.CELL_PADDING, pady=self.CELL_PADDING)
                cell_number = tk.Label(cell_frame, text="", font=("Arial", 24, "bold"), bg="#cdc1b4", fg="#776e65")
                cell_number.place(relx=0.5, rely=0.5, anchor="center")
                row.append(cell_number)
            self.cells.append(row)
            
        # Set minimum size for each row/column
        for i in range(self.GRID_SIZE):
            self.canvas_frame.grid_rowconfigure(i, minsize=self.CELL_SIZE + 2*self.CELL_PADDING)
            self.canvas_frame.grid_columnconfigure(i, minsize=self.CELL_SIZE + 2*self.CELL_PADDING)
            
        # Instructions
        self.instructions_frame = tk.Frame(self.master, bg="#faf8ef", padx=10, pady=5)
        self.instructions_frame.pack(fill="x", padx=10, pady=5)
        
        instructions_text = "How to play: Use arrow keys to move tiles. When two tiles with the same number touch, they merge!"
        instructions_text += "\nSpecial tiles: 💣 Bomb (clears surrounding), 🌀 Swapper (swaps with adjacent), 🧊 Frozen (can't move)"
        
        self.instructions_label = tk.Label(self.instructions_frame, text=instructions_text, 
                                         font=("Arial", 10), bg="#faf8ef", fg="#776e65", justify="left")
        self.instructions_label.pack(anchor="w")
    def _highlight_active_swatch(self):
        for name, btn in self.theme_buttons.items():
            if name == self.current_theme:
                btn.config(relief="sunken", bd=4)
            else:
                btn.config(relief="raised", bd=2)

    def new_game(self):
        # Reset game variables
        self.grid = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.score = 0
        self.moves = 0
        self.game_over = False
        self.game_won = False
        self.special_tiles = {}
        self.combo_count = 0
        self.update_score_display()
        
        # Reset undo
        self.previous_states = []
        self.undo_count = self.undo_limit
        self.undo_btn.config(text=f"Undo ({self.undo_count})")
        
        # Reset time if timed mode
        self.time_left = 60
        self.time_label.config(text=str(self.time_left))
        if self.timed_mode and not self.timer_running:
            self.timer_running = True
            self.update_timer()
        
        # Pick a random mission
        self.current_mission = random.choice(self.missions)
        self.current_mission["completed"] = False
        self.update_mission_display()
        
        # Add initial tiles
        self.add_new_tile()
        self.add_new_tile()
        
        # Update the display
        self.update_grid_display()
        
    def add_new_tile(self):
        # Find all empty cells
        empty_cells = [(i, j) for i in range(self.GRID_SIZE) for j in range(self.GRID_SIZE) if self.grid[i][j] == 0]
        
        if not empty_cells:
            return False
            
        # Choose random empty cell
        i, j = random.choice(empty_cells)
        
        # 90% chance for 2, 10% chance for 4
        self.grid[i][j] = 2 if random.random() < 0.9 else 4
        
        # Check if we should make it a special tile
        if random.random() < self.special_chance:
            special_type = random.choice(self.special_types)
            self.special_tiles[(i, j)] = {
                'type': special_type,
                'turns': 3 if special_type == 'frozen' else -1  # Frozen lasts 3 turns, others until used
            }
        
        return True
        
    def update_grid_display(self):
        theme = self.themes[self.current_theme]
        
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                cell = self.cells[i][j]
                cell_value = self.grid[i][j]
                
                if (i, j) in self.special_tiles:
                    special_type = self.special_tiles[(i, j)]['type']
                    # Adjust font size based on value
                    if cell_value == 0:
                        font_size = 24
                        cell_text = ""
                    else:
                        if cell_value < 100:
                            font_size = 24
                        elif cell_value < 1000:
                            font_size = 20
                        else:
                            font_size = 16
                        
                        # Display text with emoji prefix
                        if special_type == 'bomb':
                            cell_text = f"💣 {cell_value}"
                        elif special_type == 'swapper':
                            cell_text = f"🌀 {cell_value}"
                        elif special_type == 'frozen':
                            cell_text = f"🧊 {cell_value}"
                        else:
                            cell_text = str(cell_value)
                    
                    # Set colors based on special tile type
                    fg, bg = theme["colors"].get(special_type, ("#ffffff", "#000000"))
                else:
                    # Normal tiles
                    if cell_value == 0:
                        font_size = 24
                        cell_text = ""
                        fg, bg = "#776e65", theme["empty"]
                    else:
                        # Adjust font size based on value
                        if cell_value < 100:
                            font_size = 24
                        elif cell_value < 1000:
                            font_size = 20
                        else:
                            font_size = 16
                        
                        cell_text = str(cell_value)
                        # Get colors from theme
                        fg, bg = theme["colors"].get(cell_value, ("#f9f6f2", "#3c3a32"))
                
                cell.config(text=cell_text, font=("Arial", font_size, "bold"), bg=bg, fg=fg)
                cell.master.config(bg=bg)
        
        # Update canvas background
        self.canvas_frame.config(bg=theme["bg"])
        
    def key_press(self, event):
        if self.game_over:
            return
            
        # Save current state for undo
        self.save_state()
        
        key = event.keysym
        moved = False
        self.combo_count = 0  # Reset combo counter for mission tracking
        
        if key == "Up" or key == "w":
            moved = self.move_up()
        elif key == "Down" or key == "s":
            moved = self.move_down()
        elif key == "Left" or key == "a":
            moved = self.move_left()
        elif key == "Right" or key == "d":
            moved = self.move_right()
            
        if moved:
            # Update moves counter
            self.moves += 1
            
            # Add new tile
            self.add_new_tile()
            
            # Update turns for time-limited special tiles
            self.update_special_tiles()
            
            # Check for chaos mode
            if self.chaos_mode and self.moves % self.chaos_frequency == 0:
                self.trigger_chaos_event()
            
            # Check missions
            self.check_missions()
            
            # Update display
            self.update_grid_display()
            
            # Check game over
            if self.check_game_over():
                self.game_over = True
                messagebox.showinfo("Game Over", f"Game Over! Your score: {self.score}")
                
    def move_up(self):
        moved = False
        for j in range(self.GRID_SIZE):
            # Process each column
            column = [self.grid[i][j] for i in range(self.GRID_SIZE)]
            frozen_cells = [i for i in range(self.GRID_SIZE) if (i, j) in self.special_tiles and 
                            self.special_tiles[(i, j)]['type'] == 'frozen']
            
            new_column, merged, combo = self.compress_and_merge(column, frozen_cells)
            self.combo_count += combo
            
            if column != new_column:
                moved = True
                # Update grid with new values
                for i in range(self.GRID_SIZE):
                    self.grid[i][j] = new_column[i]
                    
                # Apply special tile effects
                if merged:
                    self.apply_special_tile_effects()
                    
        return moved
        
    def move_down(self):
        moved = False
        for j in range(self.GRID_SIZE):
            # Process each column bottom to top
            column = [self.grid[i][j] for i in range(self.GRID_SIZE)]
            frozen_cells = [i for i in range(self.GRID_SIZE) if (i, j) in self.special_tiles and 
                            self.special_tiles[(i, j)]['type'] == 'frozen']
            
            # Reverse, compress, merge, then reverse back
            column.reverse()
            frozen_cells = [self.GRID_SIZE - 1 - idx for idx in frozen_cells]
            new_column, merged, combo = self.compress_and_merge(column, frozen_cells)
            new_column.reverse()
            self.combo_count += combo
            
            if column[::-1] != new_column:
                moved = True
                # Update grid with new values
                for i in range(self.GRID_SIZE):
                    self.grid[i][j] = new_column[i]
                    
                # Apply special tile effects
                if merged:
                    self.apply_special_tile_effects()
                    
        return moved
        
    def move_left(self):
        moved = False
        for i in range(self.GRID_SIZE):
            # Process each row
            row = self.grid[i].copy()
            frozen_cells = [j for j in range(self.GRID_SIZE) if (i, j) in self.special_tiles and 
                            self.special_tiles[(i, j)]['type'] == 'frozen']
            
            new_row, merged, combo = self.compress_and_merge(row, frozen_cells)
            self.combo_count += combo
            
            if row != new_row:
                moved = True
                # Update grid with new values
                self.grid[i] = new_row
                
                # Apply special tile effects
                if merged:
                    self.apply_special_tile_effects()
                    
        return moved
        
    def move_right(self):
        moved = False
        for i in range(self.GRID_SIZE):
            # Process each row right to left
            row = self.grid[i].copy()
            frozen_cells = [j for j in range(self.GRID_SIZE) if (i, j) in self.special_tiles and 
                            self.special_tiles[(i, j)]['type'] == 'frozen']
            
            # Reverse, compress, merge, then reverse back
            row.reverse()
            frozen_cells = [self.GRID_SIZE - 1 - idx for idx in frozen_cells]
            new_row, merged, combo = self.compress_and_merge(row, frozen_cells)
            new_row.reverse()
            self.combo_count += combo
            
            if row[::-1] != new_row:
                moved = True
                # Update grid with new values
                self.grid[i] = new_row
                
                # Apply special tile effects
                if merged:
                    self.apply_special_tile_effects()
                    
        return moved
        
    def compress_and_merge(self, line, frozen_cells):
        # Remove zeros and pack values together, skipping frozen cells
        new_line = [0] * len(line)
        idx = 0
        
        # First pass: compress
        for i in range(len(line)):
            if i in frozen_cells:
                # Keep frozen cells in place
                new_line[i] = line[i]
            elif line[i] != 0:
                # Find next non-frozen position
                while idx in frozen_cells and idx < len(line):
                    new_line[idx] = line[idx]  # Keep the frozen value
                    idx += 1
                
                if idx < len(line):
                    new_line[idx] = line[i]
                    idx += 1
        
        # Second pass: merge
        merged = False
        combo_count = 0
        for i in range(len(new_line) - 1):
            if i in frozen_cells or i + 1 in frozen_cells:
                continue
                
            if new_line[i] != 0 and new_line[i] == new_line[i + 1]:
                # Merge tiles
                new_line[i] *= 2
                new_line[i + 1] = 0
                self.score += new_line[i]
                merged = True
                combo_count += 1
                
                # Check for 2048 tile
                if new_line[i] == 2048 and not self.game_won:
                    self.game_won = True
                    messagebox.showinfo("Congratulations", "You've reached 2048!")
        
        # Final pass: compress again after merging
        final_line = [0] * len(line)
        idx = 0
        for i in range(len(new_line)):
            if i in frozen_cells:
                final_line[i] = new_line[i]
            elif new_line[i] != 0:
                # Find next non-frozen position
                while idx in frozen_cells and idx < len(final_line):
                    final_line[idx] = new_line[idx]  # Keep the frozen value
                    idx += 1
                
                if idx < len(final_line):
                    final_line[idx] = new_line[i]
                    idx += 1
        
        self.update_score_display()
        return final_line, merged, combo_count
        
    def apply_special_tile_effects(self):
        # Create a copy because we'll modify during iteration
        special_tiles_copy = self.special_tiles.copy()
        
        for (i, j), special_info in special_tiles_copy.items():
            tile_type = special_info['type']
            
            # Skip if the cell is now empty (was moved or merged)
            if self.grid[i][j] == 0:
                if (i, j) in self.special_tiles:
                    del self.special_tiles[(i, j)]
                continue
                
            # Apply effects based on type
            if tile_type == 'bomb':
                # Bomb: clear surrounding tiles
                for ni in range(max(0, i-1), min(self.GRID_SIZE, i+2)):
                    for nj in range(max(0, j-1), min(self.GRID_SIZE, j+2)):
                        if (ni, nj) != (i, j):  # Don't clear the bomb itself
                            # Add score for cleared tiles
                            if self.grid[ni][nj] > 0:
                                self.score += self.grid[ni][nj] // 2
                            self.grid[ni][nj] = 0
                            if (ni, nj) in self.special_tiles:
                                del self.special_tiles[(ni, nj)]
                
                # Remove the bomb tile itself after use
                if (i, j) in self.special_tiles:
                    del self.special_tiles[(i, j)]
                    
            elif tile_type == 'swapper':
                # Swapper: swap with a random adjacent non-zero tile
                adjacent = []
                for ni in range(max(0, i-1), min(self.GRID_SIZE, i+2)):
                    for nj in range(max(0, j-1), min(self.GRID_SIZE, j+2)):
                        if (ni, nj) != (i, j) and self.grid[ni][nj] > 0:
                            adjacent.append((ni, nj))
                
                if adjacent:
                    ni, nj = random.choice(adjacent)
                    # Swap values
                    self.grid[i][j], self.grid[ni][nj] = self.grid[ni][nj], self.grid[i][j]
                    
                    # Move special tile status
                    if (ni, nj) in self.special_tiles:
                        self.special_tiles[(i, j)] = self.special_tiles[(ni, nj)]
                        del self.special_tiles[(ni, nj)]
                    else:
                        # Remove swapper status after use
                        if (i, j) in self.special_tiles:
                            del self.special_tiles[(i, j)]
            
            # Frozen tiles don't have an active effect, they just restrict movement
        
        self.update_score_display()
        
    def update_special_tiles(self):
        # Update turn counters for time-limited special tiles
        to_remove = []
        
        for pos, info in self.special_tiles.items():
            if info['turns'] > 0:
                info['turns'] -= 1
                if info['turns'] <= 0:
                    to_remove.append(pos)
                    
        # Remove expired special tiles
        for pos in to_remove:
            if pos in self.special_tiles:
                del self.special_tiles[pos]
                
    def check_game_over(self):
        # Check if there are any empty cells
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False
        
        # Check if there are any adjacent cells with the same value
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                # Skip if cell is frozen
                if (i, j) in self.special_tiles and self.special_tiles[(i, j)]['type'] == 'frozen':
                    continue
                    
                # Check adjacent cells
                value = self.grid[i][j]
                if (i > 0 and self.grid[i-1][j] == value) or \
                   (i < self.GRID_SIZE-1 and self.grid[i+1][j] == value) or \
                   (j > 0 and self.grid[i][j-1] == value) or \
                   (j < self.GRID_SIZE-1 and self.grid[i][j+1] == value):
                    return False
                    
        # If we get here, no moves are possible
        return True
        
    def save_state(self):
        if len(self.previous_states) >= 5:  # Keep the last 5 states max
            self.previous_states.pop(0)
            
        # Save current state
        state = {
            'grid': copy.deepcopy(self.grid),
            'score': self.score,
            'special_tiles': copy.deepcopy(self.special_tiles),
            'mission': copy.deepcopy(self.current_mission)
        }
        self.previous_states.append(state)
        
    def undo_move(self):
        if not self.previous_states or self.undo_count <= 0:
            return
            
        # Restore previous state
        state = self.previous_states.pop()
        self.grid = state['grid']
        self.score = state['score']
        self.special_tiles = state['special_tiles']
        self.current_mission = state['mission']
        
        # Decrement undo count
        self.undo_count -= 1
        self.undo_btn.config(text=f"Undo ({self.undo_count})")
        
        # Update display
        self.update_score_display()
        self.update_mission_display()
        self.update_grid_display()
        
    def get_hint(self):
        if self.game_over:
            return
            
        # Try each direction and see which gives the best score improvement
        best_direction = None
        best_score_gain = -1
        
        # Save current state
        original_grid = copy.deepcopy(self.grid)
        original_score = self.score
        original_special_tiles = copy.deepcopy(self.special_tiles)
        
        directions = ["Up", "Down", "Left", "Right"]
        for direction in directions:
            # Reset to original state
            self.grid = copy.deepcopy(original_grid)
            self.score = original_score
            self.special_tiles = copy.deepcopy(original_special_tiles)
            
            # Try move
            moved = False
            if direction == "Up":
                moved = self.move_up()
            elif direction == "Down":
                moved = self.move_down()
            elif direction == "Left":
                moved = self.move_left()
            elif direction == "Right":
                moved = self.move_right()
            
            if moved:
                score_gain = self.score - original_score
                if score_gain > best_score_gain:
                    best_score_gain = score_gain
                    best_direction = direction
        
        # Restore original state
        self.grid = original_grid
        self.score = original_score
        self.special_tiles = original_special_tiles
        
        # Show hint
        if best_direction:
            messagebox.showinfo("Hint", f"Try moving {best_direction} for best results!")
        else:
            messagebox.showinfo("Hint", "No good moves available!")
            
    def trigger_chaos_event(self):
        # Pick a random chaos event
        event_type = random.choice([
            "shuffle_one_row",
            "shuffle_one_column",
            "add_extra_tile",
            "add_special_tile"
        ])
        
        if event_type == "shuffle_one_row":
            # Shuffle a random row
            row = random.randint(0, self.GRID_SIZE-1)
            values = [self.grid[row][j] for j in range(self.GRID_SIZE) if self.grid[row][j] != 0]
            random.shuffle(values)
            
            # Place shuffled values back
            idx = 0
            for j in range(self.GRID_SIZE):
                if self.grid[row][j] != 0:
                    self.grid[row][j] = values[idx]
                    idx += 1
            
        elif event_type == "shuffle_one_column":
            # Shuffle a random column
            col = random.randint(0, self.GRID_SIZE-1)
            values = [self.grid[i][col] for i in range(self.GRID_SIZE) if self.grid[i][col] != 0]
            random.shuffle(values)
            
            # Place shuffled values back
            idx = 0
            for i in range(self.GRID_SIZE):
                if self.grid[i][col] != 0:
                    self.grid[i][col] = values[idx]
                    idx += 1
                    
        elif event_type == "add_extra_tile":
            # Add an extra tile
            self.add_new_tile()
            
        elif event_type == "add_special_tile":
            # Find empty spot and add a special tile
            empty_cells = [(i, j) for i in range(self.GRID_SIZE) for j in range(self.GRID_SIZE) if self.grid[i][j] == 0]
            if empty_cells:
                i, j = random.choice(empty_cells)
                self.grid[i][j] = 2
                special_type = random.choice(self.special_types)
                self.special_tiles[(i, j)] = {
                    'type': special_type,
                    'turns': 3 if special_type == 'frozen' else -1
                }
        
        # Show chaos mode notification
        messagebox.showinfo("Chaos Mode", "Chaos event triggered! The board has been altered.")
        
    def check_missions(self):
        # Check mission progress based on type
        if self.current_mission["type"] == "merge":
            # Check if any tile with the target value exists
            for i in range(self.GRID_SIZE):
                for j in range(self.GRID_SIZE):
                    if self.grid[i][j] >= self.current_mission["goal_value"]:
                        self.complete_mission()
                        return
                        
        elif self.current_mission["type"] == "combo":
            # Check if we made enough merges in one move
            if self.combo_count >= self.current_mission["goal_value"]:
                self.complete_mission()
                return
                
        elif self.current_mission["type"] == "score":
            # Check if score meets target
            if self.score >= self.current_mission["goal_value"]:
                self.complete_mission()
                return
                
    def complete_mission(self):
        if self.current_mission["completed"]:
            return
            
        # Mark mission as completed
        self.current_mission["completed"] = True
        
        # Reward based on mission
        if self.current_mission["type"] == "merge":
            # Reward: Extra undo
            self.undo_count = min(self.undo_count + 1, 5)
            self.undo_btn.config(text=f"Undo ({self.undo_count})")
            reward_text = "Reward: +1 Undo!"
            
        elif self.current_mission["type"] == "combo":
            # Reward: Bomb tile
            empty_cells = [(i, j) for i in range(self.GRID_SIZE) for j in range(self.GRID_SIZE) if self.grid[i][j] == 0]
            if empty_cells:
                i, j = random.choice(empty_cells)
                self.grid[i][j] = 2
                self.special_tiles[(i, j)] = {'type': 'bomb', 'turns': -1}
            reward_text = "Reward: Bomb tile added!"
            
        elif self.current_mission["type"] == "score":
            # Reward: Extra points
            bonus = self.current_mission["goal_value"] // 5
            self.score += bonus
            self.update_score_display()
            reward_text = f"Reward: +{bonus} points!"
            
        # Show completion message
        messagebox.showinfo("Mission Complete", f"Mission completed: {self.current_mission['description']}!\n{reward_text}")
        
        # Set new mission
        available_missions = [m for m in self.missions if m != self.current_mission]
        self.current_mission = random.choice(available_missions)
        self.current_mission["completed"] = False
        self.update_mission_display()
        
    def update_mission_display(self):
        mission_text = f"{self.current_mission['description']} - "
        if self.current_mission["type"] == "merge":
            mission_text += f"Progress: Highest tile = {self.get_highest_tile()}/{self.current_mission['goal_value']}"
        elif self.current_mission["type"] == "combo":
            mission_text += f"Progress: {self.combo_count}/{self.current_mission['goal_value']} merges in one move"
        elif self.current_mission["type"] == "score":
            mission_text += f"Progress: {self.score}/{self.current_mission['goal_value']} points"
            
        self.mission_label.config(text=mission_text)
        
    def get_highest_tile(self):
        return max(max(row) for row in self.grid)
        
    def update_score_display(self):
        self.score_label.config(text=str(self.score))
        if self.score > self.high_score:
            self.high_score = self.score
            self.highscore_label.config(text=str(self.high_score))
            
    def update_timer(self):
        if not self.timed_mode or not self.timer_running:
            return
            
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=str(self.time_left))
            self.master.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.game_over = True
            messagebox.showinfo("Time's Up", f"Time's up! Your score: {self.score}")
            
    def toggle_chaos(self):
        self.chaos_mode = self.chaos_var.get()
        
    def toggle_timed(self):
        self.timed_mode = self.timed_var.get()
        if self.timed_mode and not self.timer_running:
            self.timer_running = True
            self.update_timer()
        elif not self.timed_mode:
            self.timer_running = False
    def _apply_theme_recursive(self, widget, theme, panel_bg, score_bg, text_fg):
        """ Recursively apply colors to widgets, but skip theme swatches. """
        # 1) Skip over the swatch buttons entirely
        if hasattr(self, 'theme_buttons') and widget in self.theme_buttons.values():
            return

        cls = widget.__class__.__name__
        # ... rest of your existing logic unchanged .
        # Frames get either panel_bg or board bg:
        if cls == 'Frame':
            bg = score_bg if widget in (self.score_frame, self.highscore_frame, self.timer_frame) else panel_bg
            widget.config(bg=bg)
        # Labels, Buttons, Checkbuttons, OptionMenu, etc:
        elif cls in ('Label', 'Button', 'Checkbutton', 'Radiobutton'):
            widget.config(bg=panel_bg, fg=text_fg)
            if cls == 'Button':
                widget.config(activebackground=theme['empty'], relief='raised', bd=2)
        elif cls == 'OptionMenu':
            widget.config(bg=theme['empty'], fg=text_fg, relief='raised', bd=2)
            # also style its dropdown menu
            widget['menu'].config(bg=theme['empty'], fg=text_fg)
        # Canvas/frame holding the grid:
        if widget == self.canvas_frame:
            widget.config(bg=theme['bg'])
        # Recurse
        for child in widget.winfo_children():
            self._apply_theme_recursive(child, theme, panel_bg, score_bg, text_fg)
            
    def change_theme(self, selection=None):
        # pick the new theme name
        if isinstance(selection, str):
            self.current_theme = selection
        else:
            self.current_theme = self.theme_var.get()
        theme = self.themes[self.current_theme]

        # determine panel vs. score vs. board bg
        if self.current_theme == 'Classic':
            panel_bg = '#faf8ef'
            score_bg = '#bbada0'
            text_fg  = '#776e65'
        else:
            panel_bg = theme['bg']
            score_bg = theme['bg']
            text_fg  = theme['colors'][2][0]

        # window bg
        self.master.config(bg=theme['bg'])

        # recursively restyle every widget
        self._apply_theme_recursive(self.master, theme, panel_bg, score_bg, text_fg)

        # finally redraw the tiles with the new tile‐color map
        self.update_grid_display()

        

if __name__ == "__main__":
    root = tk.Tk()
    app = Game2048(root)
    root.mainloop()