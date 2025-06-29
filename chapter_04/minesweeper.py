import random

GRID_SIZE = 10
NUM_MINES = 10

def generate_mines(first_move_x, first_move_y, grid_size, num_mines):
    cells = [(i, j) for i in range(grid_size) for j in range(grid_size) if (i, j) != (first_move_x, first_move_y)]
    mine_cells = random.sample(cells, num_mines)
    mine_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    for (i, j) in mine_cells:
        mine_grid[i][j] = 'X'
    return mine_grid

def calculate_numbers(mine_grid, grid_size):
    for i in range(grid_size):
        for j in range(grid_size):
            if mine_grid[i][j] == 'X':
                continue
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    x = i + dx
                    y = j + dy
                    if 0 <= x < grid_size and 0 <= y < grid_size:
                        if mine_grid[x][y] == 'X':
                            count += 1
            mine_grid[i][j] = count

def print_grid(player_grid):
    print("   " + " ".join(str(i) for i in range(GRID_SIZE)))
    for i, row in enumerate(player_grid):
        print(f"{i} |" + " ".join(str(cell) for cell in row))

def main():
    player_grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    game_over = False
    win = False
    first_move = True
    mine_grid = None

    def uncover(x, y):
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            if player_grid[x][y] not in (' ', 'F'):
                continue
            if mine_grid[x][y] == 'X':
                continue

            cell_value = mine_grid[x][y]
            player_grid[x][y] = str(cell_value) if cell_value != 0 else ' '

            if cell_value == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                            if player_grid[nx][ny] in (' ', 'F'):
                                stack.append((nx, ny))

    while not game_over:
        print_grid(player_grid)
        try:
            input_str = input("Enter row, column, action (u/f): ").split()
            if len(input_str) != 3:
                print("Invalid input")
                continue
            x = int(input_str[0])
            y = int(input_str[1])
            action = input_str[2].lower()
            if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE or action not in ('u', 'f'):
                print("Invalid input")
                continue
        except:
            print("Invalid input")
            continue

        if first_move:
            if action != 'u':
                print("First move must be an uncover action (u)")
                continue
            mine_grid = generate_mines(x, y, GRID_SIZE, NUM_MINES)
            calculate_numbers(mine_grid, GRID_SIZE)
            first_move = False

        if action == 'f':
            if player_grid[x][y] == ' ':
                player_grid[x][y] = 'F'
            elif player_grid[x][y] == 'F':
                player_grid[x][y] = ' '
            else:
                print("Cannot flag uncovered cell")
            continue
        elif action == 'u':
            if player_grid[x][y] == 'F':
                print("Cell is flagged, unflag first")
                continue
            if mine_grid[x][y] == 'X':
                print("Game Over! You hit a mine.")
                game_over = True
                for i in range(GRID_SIZE):
                    for j in range(GRID_SIZE):
                        if mine_grid[i][j] == 'X':
                            player_grid[i][j] = 'X'
                print_grid(player_grid)
                break
            else:
                uncover(x, y)
        else:
            print("Invalid action")
            continue

        win = True
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if mine_grid[i][j] == 'X' and player_grid[i][j] != 'F':
                    win = False
                elif mine_grid[i][j] != 'X' and player_grid[i][j] in (' ', 'F'):
                    win = False
            if not win:
                break

        if win:
            print("Congratulations! You won!")
            game_over = True
            print_grid(player_grid)

if __name__ == "__main__":
    main()