from gturtle import *
import random

# Turtle Setup: Initializes the Turtle graphics window
makeTurtle()
clear()
speed(0)
setPos(-125, 125)
penUp()

# Game board settings (can be adjusted later for larger boards and more mines)
board_size = 5  # Size of the board (number of rows and columns)
cell_size = 50  # Size of each cell in pixels
mark_size = 20  # Size of the mark in each cell (mine or safe)

# Multipliers based on the difficulty level and the number of safe cells revealed
multipliers = {}
# please insert your own multipliers.
def draw_board():
    """Draws the game board based on the board size and cell size."""
    for y in range(board_size):
        for x in range(board_size):
            penUp()
            moveTo(-125 + x * cell_size, 125 - y * cell_size)
            penDown()
            setHeading(0)
            for i in range(4):  # Draws a square (4 sides)
                forward(cell_size)
                right(90)
    penUp()

def mark_cell(row, col, is_mine):
    """Marks the selected cell as a mine (red) or safe (green)."""
    penUp()
    moveTo(-125 + col * cell_size + (cell_size - mark_size) / 2,
           125 - row * cell_size - (cell_size - mark_size) / 2 + mark_size / 2)
    penDown()
    if is_mine:
        setPenColor("red")  # Color for mines
    else:
        setPenColor("green")  # Color for safe cells
    fill(4)  # Fills the cell with color
    penUp()

def setup_game(balance, difficulty):
    """Prepares the game by generating mines based on the selected difficulty."""
    global mine_positions
    if difficulty == 1:
        mine_count = 5  # Easy difficulty: 5 mines
    elif difficulty == 2:
        mine_count = 7  # Medium difficulty: 7 mines
    else:
        mine_count = 10  # Hard difficulty: 10 mines

    # Randomly select positions for the mines on the board
    mine_positions = random.sample(range(board_size * board_size), mine_count)
    return balance, mine_count

def check_cell(row, col, balance, mine_count, safe_count):
    """Checks the selected cell and updates the balance based on whether it's a mine or not."""
    cell_index = row * board_size + col  # Converts 2D coordinates to a 1D index for simplicity
    if cell_index in revealed_positions:
        print("This cell has already been checked.")
        return balance, safe_count

    revealed_positions.append(cell_index)  # Adds the cell index to the list of revealed cells
    if cell_index in mine_positions:
        print(f"You hit a mine! You lose {balance}$.")
        balance = 0  # If the player hits a mine, their balance becomes zero
    else:
        # Use a multiplier based on the number of mines and safe cells revealed
        multiplier = multipliers[mine_count][safe_count] if safe_count < 10 else multipliers[mine_count][-1]
        balance = int(balance * multiplier)  # Update balance with multiplier
        safe_count += 1  # Increment the count of safe cells
        print(f"Safe cell! Multiplier: {multiplier}x. New balance: {balance}$")
    return balance, safe_count

def main():
    global revealed_positions
    revealed_positions = []  # List to store revealed cell indices

    # Ask the player for the starting balance
    start_balance_input = input("How much would you like as your starting balance? (or type 'new' for a new start with 100$): ")

    if start_balance_input.lower() == 'new':
        balance = 100  # Default balance
    else:
        try:
            balance = int(start_balance_input)  # Try to convert input to an integer
            if balance <= 0:
                print("Invalid amount. The game starts with 100$.")
                balance = 100
        except ValueError:
            print("Invalid input. Starting balance will be set to 100$.")
            balance = 100

    # Ask the player to choose the difficulty level
    difficulty_input = input("Choose the difficulty level (1 = Easy, 2 = Medium, 3 = Hard): ")
    try:
        difficulty = int(difficulty_input)
        if difficulty not in [1, 2, 3]:
            print("Invalid difficulty level. Difficulty 1 (Easy) will be selected.")
            difficulty = 1
    except ValueError:
        print("Invalid input. Difficulty 1 (Easy) will be selected.")
        difficulty = 1

    while True:
        print(f"Current balance: {balance}$")

        if balance <= 0:
            print("You have no money left. Game over.")
            break
        
        investment_input = input("How much would you like to invest? (or type 'cashout' to cash out): ")

        if investment_input.lower() == 'cashout':
            print(f"You cashed out {balance}$. Remember this amount for the next round!")
            break

        try:
            investment = int(investment_input)
            if investment <= 0 or investment > balance:
                print("Invalid amount. Please enter a valid amount.")
                continue

            draw_board()  # Draw the game board
            balance, mine_count = setup_game(balance, difficulty)  # Set up the game based on the difficulty level
            safe_count = 0  # Count of safe cells revealed
            revealed_positions.clear()  # Clear the revealed positions list

            while balance > 0:
                try:
                    # Ask for row and column to check
                    row = int(input("Row (1-5): ")) - 1
                    col = int(input("Column (1-5): ")) - 1
                    if row < 0 or row >= board_size or col < 0 or col >= board_size:
                        print("Invalid input. Please try again.")
                        continue
                    
                    # Check the cell for mines or safety
                    balance, safe_count = check_cell(row, col, balance, mine_count, safe_count)

                    if balance == 0:
                        print("You have no money left. Game over.")
                        break

                except ValueError:
                    print("Invalid input. Please enter numbers between 1 and 5.")
                    continue

            if balance > 0:
                continue

        except ValueError:
            print("Invalid input. Please enter an amount.")

# Start the game
main()
