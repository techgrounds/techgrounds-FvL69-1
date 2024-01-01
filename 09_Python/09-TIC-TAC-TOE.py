# Tic-Tac-Toe:
'''
Generate a 3x3 board on the command line.
This is a 2-player game, where one player inputs “X” and the other player inputs “O”.
'''
def display_board(b):
    # Print column numbers.
    print("  1 2 3")
    # Print row number.
    for row in range(3):
        print(row+1, end=" ")
        # Print board.
        for column in range(3):
            print( b[row][column], end=" ")
        print()

board = [["-", "-", "-"], ["-", "-", "-"],["-", "-", "-"]]
display_board(board) 


def play_game():
    while True:
        # Get board co-ord.
        try:
            r = int(input("Enter row number: "))
            if r > len(board):
                print("Out of range, try again.")
                continue
            c = int(input("Enter column number: "))
            if c > len(board):
                print("Out of range, try again.")
                continue 
        except ValueError:
            print("Wrong entry, try again.")
            continue
        except TypeError:
            print("Wrong entry, try agian.")
            continue
        i = input("Enter X or O: ").upper()
        if i != "X" and i != "O":
            print("Invalid input, back to start...")
            continue
        # Check if space is available.
        if board[r-1][c-1] != "-":
            print("That position is no longer available! Try again...\n")
            continue
        else:
            board[r-1][c-1] = i
        display_board(board)
        w = checkForWinner()
        if w == True:
            break

def checkForWinner():
    # Horiontal check.
    for row in range(len(board)):
        if board[row] == ["X","X","X"]:
            print("\n X WINS!!! \n")
            return True
        elif board[row] == ["O","O","O"]:
            print("\n O WINS!!! \n")
            return True

    # Vertical check
    for col in range(len(board)):
        checkbox = []
        board[col]
        for row in range(len(board)):
            if board[row][col] != "-":
                checkbox.append(board[row][col])
        # Checking box for match.
        if checkbox == ["X","X","X"]:
            print("\n X WINS!!! \n")
            return True
        elif checkbox == ["O","O","O"]:
            print("\n O WINS!!! \n")
            return True    
    
    # Diagonal check, top left to bottom right.
    checkbox = []
    for n in range(len(board)):
        if board[n][n] != "-":
            checkbox.append(board[n][n])
    # Checking box for match.
    if checkbox == ["X","X","X"]:
        print("\n X WINS!!! \n")
        return True
    elif checkbox == ["O","O","O"]:
        print("\n O WINS!!! \n")
        return True  
    
    # Diagonal check, bottom left to top right.
    checkbox = []
    row = len(board)-1
    for col in range(len(board)):
        if board[row][col] != "-":
            checkbox.append(board[row][col])
        row -= 1
    # Checking box for match.
    if checkbox == ["X","X","X"]:
        print("\n X WINS!!! \n")
        return True
    elif checkbox == ["O","O","O"]:
        print("\n O WINS!!! \n")
        return True  


play_game()   




