from random import randint as random
from copy import deepcopy as copy

GRID_SIZE = 3


def show_grid(grid):
    print("\n")
    for i in range(1, GRID_SIZE + 1):
        print(f"   {i}", end="")
    print()
    for i in range(GRID_SIZE):
        print(" ", end="")
        for j in range(GRID_SIZE):
            print(" ———", end="")
        print()
        print(i + 1, end=" ")
        for j in range(GRID_SIZE):
            print("|", end=" ")
            print("O" if grid[i][j] == 1 else "X" if grid[i][j] == 2 else " ", end=" ")
        print("|")
    print(" ", end="")
    for j in range(GRID_SIZE):
        print(" ———", end="")
    print("\n")

def row(matrix, i):
    return matrix[i]


def column(matrix, i):
    return [row[i] for row in matrix]


def diagonal(matrix):
    return [row[i] for i, row in enumerate(matrix)]


def complete(grid):
    filled = True
    for row in grid:
        for case in row:
            if case is None:
                filled = False
    return filled


def empty(grid):
    filled = False
    for row in grid:
        for case in row:
            if case is not None:
                filled = True
    return not filled


def who_win(grid):
    for p in range(1, GRID_SIZE):
        for i in range(GRID_SIZE):
            if (
                row(grid, i) == [p] * GRID_SIZE
                or column(grid, i) == [p] * GRID_SIZE
                or diagonal(grid) == [p] * GRID_SIZE
                or diagonal(grid[::-1]) == [p] * GRID_SIZE
            ):
                return p
    return 0


def score(player, grid, depth=0):
    winner = who_win(grid)

    if empty(grid):
        return {"score": 0, "depth": 9}
    elif complete(grid):
        if winner == 1:
            return {"score": 1, "depth": depth}
        elif winner == 2:
            return {"score": -1, "depth": depth}
        else:
            return {"score": 0, "depth": depth}
    elif depth <= 1 and winner == 1:
        return {"score": 1, "depth": depth}
    elif depth == 1 and winner == 2:
        return {"score": -1, "depth": depth}
    elif winner == 1:
        return {"score": 1, "depth": depth}
    elif winner == 2:
        return {"score": -1, "depth": depth}
    else:
        selected_score = None
        selected_depth = None

        for m, r in enumerate(grid):
            for n, case in enumerate(r):
                if case is None:
                    new_grid = copy(grid)

                    new_grid[m][n] = player

                    result = score((2 if player == 1 else 1), new_grid, depth + 1)
                    new_score, new_depth = result["score"], result["depth"]

                    if (
                        selected_score is None
                        or new_score > selected_score
                        or new_score == selected_score == -1
                        and new_depth > selected_depth
                        or new_score == selected_score != -1
                        and new_depth < selected_depth
                    ):
                        selected_score = new_score
                        selected_depth = new_depth
        return {"score": selected_score, "depth": selected_depth}


def advisor(grid, player):
    selected_score = None
    selected_depth = None
    selected_row = None
    selected_column = None

    for row_index, row in enumerate(grid):
        for column_index, case in enumerate(row):
            if case is None:
                new_grid = copy(grid)

                new_grid[row_index][column_index] = player

                result = score((2 if player == 1 else 1), new_grid)
                new_score, new_depth = result["score"], result["depth"]

                if (
                    (selected_score is None
                    or new_score > selected_score
                    or new_score == selected_score == -1)
                    and (new_depth > selected_depth
                    or new_score == selected_score != -1)
                    and (new_depth < selected_depth)
                ):
                    selected_score = new_score
                    selected_depth = new_depth
                    selected_row = row_index
                    selected_column = column_index

    return (selected_row, selected_column)


def main():
    starting_player = random(1, 2)

    grid: list[list[int | None]] = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    if starting_player == 1:
        print("\nC'est l'ordinateur qui commence !\n")
        grid[random(0, GRID_SIZE - 1)][random(0, GRID_SIZE - 1)] = 1
    elif starting_player == 2:
        print("\nC'est vous qui commencez !\n")

    while not complete(grid) or who_win(grid) != 0:
        # print(not complete(grid), who_win(grid) == 0)
        show_grid(grid)

        r = None
        c = None

        while True:
            r = int(input("Sur quelle ligne jouer ? ")) - 1
            c = int(input("Sur quelle colonne jouer ? ")) - 1

            if r not in range(GRID_SIZE) and c not in range(GRID_SIZE):
                print("\nYou cannot play outside of the grid.\n")
            elif grid[r][c] is not None:
                print("\nThis case is already completed.\n")
            else:
                break

        grid[r][c] = 2

        if who_win(grid) != 0:
            break

        row_to_play, column_to_play = advisor(grid, 1)

        if row_to_play is not None and column_to_play is not None:
            grid[row_to_play][column_to_play] = 1

        if who_win(grid) != 0:
            break

    show_grid(grid)

    winner = who_win(grid)

    if winner == 1:
        print("Dommage :(")
    elif winner == 2:
        print("Bien joué !")
    else:
        print("Égalité...")


main()
