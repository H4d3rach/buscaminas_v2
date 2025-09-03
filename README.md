# buscaminas_v2 Minesweeper Multiplayer Server (Socket Based)

This is a basic multiplayer **Minesweeper server application** built using **Python sockets and threading**. It allows multiple clients to connect and play a shared game of Minesweeper over a network.

> This is **version 2**, originally built as a test of socket functionality using Python. It is functional but has **concurrency limitations** that will be addressed in future versions.

---

## Features

- Accepts multiple client connections using **TCP sockets**
- First connected user selects the difficulty and initializes the game board
- Shared game board across all clients
- Basic communication protocol:
  - Clients send coordinates
  - Server responds with result codes
- Basic threading used to handle multiple clients concurrently
- Dynamic board generation based on selected difficulty

---

## Gameplay Flow

1. The first client chooses a difficulty:
   - `Beginner` → 9x9 board with 10 mines
   - `Advanced` → 16x16 board with 40 mines
   - `Test` → 3x3 board with 4 mines (for debugging)

2. The server generates the board and randomly places the mines.

3. Clients take turns sending coordinates in the format `(xx,yy)`, where:
   - If the cell is empty, they can continue playing.
   - If they hit a mine, they lose.
   - If all non-mine cells are discovered, the player wins.

4. The server sends status codes back to the client:
   - `1` → Player has won
   - `2` → Correct move (empty cell)
   - `3` → Coordinates out of range
   - `4` → Mine hit (player loses)
   - `5` → Cell already selected

---

## Known Issues

- Shared global state between all client threads
- No locking mechanism to prevent race conditions
- Only one game session at a time
- No input validation beyond basic checks

---

## Requirements

- Python 3.x

---

## How to Run

python servidor.py <host> <port> <max_connections>
