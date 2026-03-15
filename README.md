# Classic Checkers (Tkinter)

A local computer checkers game built with Python and Tkinter

You can play in:
- 1 Player: Human (`light`) vs a builtn in agent (`dark`)
- 2 Player: Local pass and play (`light` vs `dark`)

## Requirements

- Python 3.9+ (3.10+ recommended)
- Tkinter available in Python installation

- A note that most standard Python installs include Tkinter. On some Linux setups you may need to install it separately

## Run the game

From the repository root:

```bash
python3 src/main.py
```

When the app opens:
1. Click **Play**
2. Choose **1 Player (vs Agent)** or **2 Player (Human vs Human)**
3. Start moving pieces by clicking on the board


## How to play

This implementation follows standard checkers with enforced captures

### 1) Board orientation and sides

- The game is played on an 8×8 board
- Pieces move on dark squares only
- `light` pieces start at the bottom rows and move upward as men
- `dark` pieces start at the top rows and move downward as men
- Light always moves first

### 2) Basic turn flow

On your turn:
1. Click one of your pieces to select it
2. Click a highlighted destination square to move
3. Turn ends automatically unless you must continue a capture chain

### 3) Move rules for men

A man (or piece) can:
- Move diagonally forward by 1 square (non-capturing move), or
- Jump diagonally forward by 2 squares or more to capture an opponent piece

A jump is legal only if:
- The adjacent diagonal square contains an opponent piece, and
- The landing square just beyond is empty

### 4) Forced captures

This game enforces mandatory captures:
- If any of your pieces can capture, you **must** make a capture
- Non-capturing moves are rejected when a capture is available

UI help for this rule:
- Pieces that can jump are outlined in **red**
- Valid destinations for the selected piece are shown as **green markers**

### 5) Multijumps

After you capture:
- If that same piece can capture again immediately, you must continue jumping with it
- Your turn ends only when no further capture is available from that piece

### 6) Kings

A man is crowned when it reaches the far edge:
- `light_man` reaching top row becomes `light_king`
- `dark_man` reaching bottom row becomes `dark_king`

Kings can move and capture diagonally in both directions

### 7) Winning the game

A player wins when the opponent has no legal moves on their turn

This can happen if the opponent:
- Has no pieces left, or
- Still has pieces but none can move or capture

When the game ends, the UI shows the winner and a Home button to return to the start screen


## 1 - Player (vs agent)

In 1 Player mode:
- You control **light**
- The agent controls **dark**
- The status text will indicate when the agent is thinking

The agent uses a minimax and alpha beta style search with a board evaluation heuristic

## On screen controls

- **Green border** on a piece: currently selected piece
- **Red border** on a piece: that piece has a required jump
- **Green dots/ovals** on squares: legal destinations for selected piece
- **Score line**: current mode and remaining piece counts for both sides
- **Home button**: return to start/menu

## Troubleshooting Reminders

### Window does not open
- Make sure that Tkinter is installed and available to your Python interpreter

### Clicks do nothing
- In 1 Player mode, you cannot move during the agent's turn (`dark`)
- If a jump is available, you must play a jump first

### Game feels stuck after a capture
- You likely have a forced follow up jump with the same piece so continue the chain