# variante PopOut do Connect 4
# regras: coloca uma peça normalmente, ou retira a tua peça da base (tudo cai para baixo)
# se um pop der 4 em linha a ambos os jogadores, quem fez o pop ganha
# 3 estados de tabuleiro repetidos = pode pedir empate, o mesmo se o tabuleiro estiver completamente cheio

import copy

ROWS = 6
COLS = 7
EMPTY = '.'
P1 = 'X'
P2 = 'O'


def create_board():
    return [[EMPTY] * COLS for _ in range(ROWS)]


def print_board(board):
    print()
    labels = '  ' + '  '.join(str(c + 1) for c in range(COLS))
    print(labels)
    for row in board:
        print('  ' + '  '.join(cell for cell in row))
    print(labels)
    print()


def board_to_tuple(board):
    return tuple(tuple(row) for row in board)


def is_full(board):
    return all(board[0][c] != EMPTY for c in range(COLS))


def can_drop(board, col):
    return 0 <= col < COLS and board[0][col] == EMPTY


def can_pop(board, col, player):
    return 0 <= col < COLS and board[ROWS - 1][col] == player


def drop_disc(board, col, player):
    if not can_drop(board, col):
        return None
    b = [row[:] for row in board]
    for row in range(ROWS - 1, -1, -1):
        if b[row][col] == EMPTY:
            b[row][col] = player
            return b
    return None


def pop_disc(board, col, player):
    if not can_pop(board, col, player):
        return None
    b = [row[:] for row in board]
    for row in range(ROWS - 1, 0, -1):
        b[row][col] = b[row - 1][col]
    b[0][col] = EMPTY
    return b


def check_four(board, player):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r + i][c - i] == player for i in range(4)):
                return True
    return False


def get_moves(board, player):
    drops = [c for c in range(COLS) if can_drop(board, c)]
    pops = [c for c in range(COLS) if can_pop(board, c, player)]
    return drops, pops


def other(player):
    return P2 if player == P1 else P1


def show_moves(board, player):
    drops, pops = get_moves(board, player)
    print(f"drop: {[c + 1 for c in drops]}  |  pop: {[c + 1 for c in pops]}")
    if is_full(board):
        print("tabuleiro cheio - podes escrever 'draw'")
    print()


def get_move(board, player, history):
    state = board_to_tuple(board)
    repeated = history.count(state) >= 2

    while True:
        prompt = "jogada (ex: 'drop 3' ou 'pop 2')"
        if is_full(board) or repeated:
            prompt += " ou 'draw'"
        if repeated:
            prompt += "  [tabuleiro repetido 3x]"
        prompt += ": "

        raw = input(prompt).strip().lower()

        if raw == 'draw':
            if is_full(board) or repeated:
                return 'draw', None
            print("ainda não podes pedir empate")
            continue

        parts = raw.split()
        if len(parts) != 2:
            print("tenta algo como: drop 4")
            continue

        move_type, col_str = parts
        if move_type not in ('drop', 'pop'):
            print("tem de ser drop ou pop")
            continue

        try:
            col = int(col_str) - 1
        except ValueError:
            print("a coluna deve ser um número")
            continue

        if move_type == 'drop':
            if not can_drop(board, col):
                print("essa coluna está cheia")
                continue
            return 'drop', col
        else:
            if not can_pop(board, col, player):
                print("não tens uma peça na base dessa coluna")
                continue
            return 'pop', col


def play_game():
    board = create_board()
    turn = P1
    history = [board_to_tuple(board)]

    print("\n--- POPOUT ---")
    print(f"X começa. drop para colocar, pop para remover a tua peça da base.")
    print("faz 4 em linha para ganhar.\n")

    while True:
        print_board(board)
        opp = other(turn)
        print(f"{turn}'s turn")
        show_moves(board, turn)

        move_type, col = get_move(board, turn, history)

        if move_type == 'draw':
            print_board(board)
            print("empate!")
            break

        if move_type == 'drop':
            new_board = drop_disc(board, col, turn)
            popped = False
        else:
            new_board = pop_disc(board, col, turn)
            popped = True

        if new_board is None:
            print("algo correu mal, tenta outra vez")
            continue

        cur_wins = check_four(new_board, turn)
        opp_wins = check_four(new_board, opp)

        if cur_wins or opp_wins:
            print_board(new_board)
            if popped and cur_wins and opp_wins:
                print(f"ambos fizeram 4 em linha mas {turn} fez o pop — {turn} ganha!")
            elif cur_wins:
                print(f"{turn} ganha!")
            else:
                print(f"{opp} ganha!")
            break

        board = new_board
        history.append(board_to_tuple(board))
        turn = opp


if __name__ == '__main__':
    while True:
        play_game()
        again = input("\njogar outra vez? (s/n): ").strip().lower()
        if again not in ('s', 'sim'):
            break
