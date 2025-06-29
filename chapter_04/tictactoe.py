######
# CODE GENERATED FROM LLM, COOL!
######




def print_board(board):
    for i in range(3):
        print("| " + " | ".join(board[i]) + " |")
        if i < 2:
            print("-------------")

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    while True:
        print_board(board)
        position = input(f"Player {current_player}, enter position (1-9): ").strip()
        if not position.isdigit():
            print("Invalid input. Please enter a number between 1-9.")
            continue
        pos = int(position)
        if pos < 1 or pos > 9:
            print("Invalid position. Enter a number between 1-9.")
            continue
        row = (pos - 1) // 3
        col = (pos - 1) % 3
        if board[row][col] != " ":
            print("Position already taken. Choose another.")
            continue
        board[row][col] = current_player
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} wins!")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()