# Enhanced 2048 🎮

An **interactive**, feature-rich version of the classic 2048 game built with Python and Tkinter.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/) 

---

## 📋 Table of Contents

* [🎥 Demo](#-demo)
* [✨ Features](#-features)
* [🚀 Installation](#-installation)
* [▶️ Usage](#-usage)
* [⌨️ Controls & Shortcuts](#-controls--shortcuts)
* [🎨 Customization](#-customization)
* [🤝 Contributing](#-contributing)
* [📄 License](#-license)

---

## ✨ Features

* **Classic 2048 gameplay** with a modern twist
* **Undo**: Up to 3 undos per game (max 5), track your moves
* **Hint**: Intelligent suggestions for your next move
* **Modes**:

  * **Cha﻿os Mode**: Random board events every 10 moves
  * **Timed Mode**: Race against a 60‑second countdown
* **Special Tiles**:

  * 💣 **Bomb**: Clears surrounding tiles when merged
  * 🌀 **Swapper**: Swaps with a nearby tile
  * 🧊 **Frozen**: Locked in place for 3 turns
* **Missions & Rewards**: Complete random objectives to earn bonuses
* **Themes**: Switch between multiple color schemes on the fly
* **Responsive UI**: Buttons for New Game, Undo, Hint, and toggles for modes

---

## 🚀 Installation

1. **Clone** this repository:

   ```bash
   git clone https://github.com/vickygovekar/enhanced-2048-game.git
   cd enhanced-2048-game
   ```
2. **Install** dependencies (if any):

   ```bash
   pip install -r requirements.txt
   ```
3. **Run** the game:

   ```bash
   python Enhanced-2048.py
   ```

> **Note:** Requires Python 3.6+ and Tkinter (usually included with standard Python installs).

---

## ▶️ Usage

* **Move tiles** with arrow keys or `W`/`A`/`S`/`D`.
* **Cycle themes** by pressing `T` or clicking a swatch button.
* **Activate Chaos & Timed modes** via checkboxes.
* **Use buttons**:

  * **New Game**: Restart.
  * **Undo**: Go back one move.
  * **Hint**: Get the best move recommendation.

---

## ⌨️ Controls & Shortcuts

| Action             | Key / Button           |
| ------------------ | ---------------------- |
| Move Up            | Arrow ↑ or `W`         |
| Move Down          | Arrow ↓ or `S`         |
| Move Left          | Arrow ← or `A`         |
| Move Right         | Arrow → or `D`         |
| Cycle Theme        | `T`                    |
| New Game           | \[New Game] button     |
| Undo (x3 per game) | \[Undo] button         |
| Hint               | \[Hint] button         |
| Toggle Chaos Mode  | \[Chaos Mode] checkbox |
| Toggle Timed Mode  | \[Timed Mode] checkbox |

---

## 🎨 Customization

* **Themes**: Add or tweak color palettes in `self.themes`.
* **Missions**: Edit or extend missions in the `self.missions` list.
* **Special Tiles**: Adjust `special_chance`, types, and effects in the code.
* **Timers & Limits**: Change time limits (`self.time_left`) and undo limits (`self.undo_limit`).

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

Please adhere to the existing code style and include tests/examples when applicable.
