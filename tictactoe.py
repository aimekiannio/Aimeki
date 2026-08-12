board = [" ", " ", " ",
         " ", " ", " ",
         " ", " ", " "]

def print_board():
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("--+---+--")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("--+---+--")
    print(board[6] + " | " + board[7] + " | " + board[8])


def move(player):
    pos = int(input(f"Player {player}, choose position (0-8): "))

    if pos < 0 or pos > 8:
        print("Invalid position")
        move(player)
        return

    if board[pos] == " ":
        board[pos] = player
    else:
        print("Already taken. Try again.")
        move(player)


def check_win(p):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]

    for a, b, c in wins:
        if board[a] == board[b] == board[c] == p:
            return True
    return False


turn = "X"

for i in range(9):
    print_board()
    move(turn)

    if check_win(turn):
        print_board()
        print(turn, "wins!")
        break

    turn = "O" if turn == "X" else "X"
else:
    print("Draw")
