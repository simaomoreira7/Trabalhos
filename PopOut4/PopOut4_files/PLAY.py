# play.py — PopOut4 com todos os modos de jogo
#
# Modos via linha de comandos:
#   python play.py human_human  — Humano vs Humano
#   python play.py human_mcts   — Humano vs MCTS
#   python play.py mcts_id3     — MCTS vs ID3 (20 jogos automáticos)
#   python play.py              — menu interativo

import sys
import time
import random
import pandas as pd

from MCTS import MCTS, encode_state

from PopOut4 import (
    ROWS, COLS, P1, P2,
    create_board, print_board, board_to_tuple,
    check_four, get_moves, drop_disc, pop_disc,
    other, is_full, get_move, show_moves, can_drop, can_pop
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

MCTS_KWARGS = dict(
    c             = 1.41,
    variant       = 'ucbv',
    use_heuristic = False,
    smart_rollout = True,
    n_simulations = 300,
)

DATASET_PATH = 'popout_dataset.csv'

# ---------------------------------------------------------------------------
# Treinar ID3
# ---------------------------------------------------------------------------

TREE_CACHE = 'id3_tree.pkl'

def load_and_train_id3(path=DATASET_PATH):
    import pickle, os
    if not os.path.exists(TREE_CACHE):
        print(f"Erro: '{TREE_CACHE}' nao encontrado.")
        print("Corre 'python ID3_Treino.py' uma vez para gerar o ficheiro.")
        sys.exit(1)
    with open(TREE_CACHE, 'rb') as f:
        tree = pickle.load(f)
    print("Arvore ID3 carregada.")
    return tree
# ---------------------------------------------------------------------------
# ID3 como agente
# ---------------------------------------------------------------------------

def id3_move(tree, board, player):
    """Converte estado do tabuleiro em features e usa a árvore para jogar."""
    features  = encode_state(board, player)
    sample    = pd.Series(features)
    predicted = tree.predict(sample)

    if predicted is None:
        drops, pops = get_moves(board, player)
        all_moves = [('drop', c) for c in drops] + [('pop', c) for c in pops]
        return random.choice(all_moves) if all_moves else None

    parts     = predicted.split('_')
    move_type = parts[0]
    col       = int(parts[1])

    if move_type == 'drop' and can_drop(board, col):
        return move_type, col
    if move_type == 'pop' and can_pop(board, col, player):
        return move_type, col

    # fallback: jogada aleatória válida
    drops, pops = get_moves(board, player)
    all_moves = [('drop', c) for c in drops] + [('pop', c) for c in pops]
    return random.choice(all_moves) if all_moves else None

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _check_winner(board, turn, move_type):
    opp = other(turn)
    cur_wins = check_four(board, turn)
    opp_wins = check_four(board, opp)
    if cur_wins or opp_wins:
        if move_type == 'pop' and cur_wins and opp_wins:
            return turn
        return turn if cur_wins else opp
    return None

def _print_result(winner):
    print("\n" + "="*35)
    if winner == 'draw':
        print("  EMPATE!")
    else:
        print(f"  {winner} VENCEU!")
    print("="*35 + "\n")

# ---------------------------------------------------------------------------
# Modo 0: Humano vs Humano  
# ---------------------------------------------------------------------------

def play_human_vs_human():
    """Dois jogadores humanos jogam no mesmo terminal."""
    board   = create_board()
    turn    = P1
    history = [board_to_tuple(board)]

    print("\n--- PopOut: Humano vs Humano ---")
    print("X começa. 'drop N' para colocar, 'pop N' para retirar da base.\n")

    while True:
        print_board(board)
        opp = other(turn)
        print(f"Vez de {turn}")
        show_moves(board, turn)

        move_type, col = get_move(board, turn, history)

        if move_type == 'draw':
            _print_result('draw')
            break

        new_board = (drop_disc(board, col, turn) if move_type == 'drop'
                     else pop_disc(board, col, turn))

        if new_board is None:
            print("Jogada inválida, tenta outra vez.")
            continue

        winner = _check_winner(new_board, turn, move_type)
        if winner:
            print_board(new_board)
            _print_result(winner)
            break

        board = new_board
        history.append(board_to_tuple(board))

        if history.count(board_to_tuple(board)) >= 3:
            print_board(board)
            print("Estado repetido 3 vezes.")
            _print_result('draw')
            break

        if is_full(board):
            print_board(board)
            _print_result('draw')
            break

        turn = opp

# ---------------------------------------------------------------------------
# Modo 1: Humano vs MCTS
# ---------------------------------------------------------------------------

def play_human_vs_mcts(human_player=P1):
    agent   = MCTS(**MCTS_KWARGS)
    board   = create_board()
    turn    = P1
    history = [board_to_tuple(board)]

    print(f"\n--- PopOut: Humano ('{human_player}') vs MCTS ---\n")

    while True:
        print_board(board)
        opp = other(turn)

        if turn == human_player:
            print(f"A tua vez ({turn})")
            show_moves(board, turn)
            move_type, col = get_move(board, turn, history)
            if move_type == 'draw':
                _print_result('draw')
                break
            new_board = (drop_disc(board, col, turn) if move_type == 'drop'
                         else pop_disc(board, col, turn))
        else:
            print(f"MCTS a pensar ({turn})...")
            t0 = time.perf_counter()
            move = agent.choose_move(board, turn)
            dt = time.perf_counter() - t0
            if move is None:
                _print_result('draw')
                break
            move_type, col = move
            print(f"MCTS joga: {move_type} coluna {col + 1}  ({dt:.2f}s)\n")
            new_board = (drop_disc(board, col, turn) if move_type == 'drop'
                         else pop_disc(board, col, turn))

        if new_board is None:
            print("Jogada inválida, tenta outra vez.")
            continue

        winner = _check_winner(new_board, turn, move_type)
        if winner:
            print_board(new_board)
            _print_result(winner)
            break

        board = new_board
        history.append(board_to_tuple(board))

        if history.count(board_to_tuple(board)) >= 3:
            print_board(board)
            _print_result('draw')
            break
        if is_full(board):
            print_board(board)
            _print_result('draw')
            break

        turn = opp

# ---------------------------------------------------------------------------
# Modo 2: MCTS vs ID3 (N jogos automáticos)
# ---------------------------------------------------------------------------

def play_mcts_vs_id3(tree, n_games=100):
    mcts    = MCTS(**MCTS_KWARGS)
    results = {'MCTS': 0, 'ID3': 0, 'draw': 0}

    print(f"\n--- MCTS vs ID3 ({n_games} jogos) ---\n")

    for game in range(n_games):
        mcts_player = P1 if game % 2 == 0 else P2
        id3_player  = other(mcts_player)

        board   = create_board()
        turn    = P1
        history = [board_to_tuple(board)]
        winner  = None

        while True:
            if check_four(board, P1) or check_four(board, P2):
                break

            drops, pops = get_moves(board, turn)
            if not drops and not pops:
                break

            move = (mcts.choose_move(board, turn) if turn == mcts_player
                    else id3_move(tree, board, turn))

            if move is None:
                break

            move_type, col = move
            new_board = (drop_disc(board, col, turn) if move_type == 'drop'
                         else pop_disc(board, col, turn))
            if new_board is None:
                break

            w = _check_winner(new_board, turn, move_type)
            if w:
                winner = w
                break

            board = new_board
            history.append(board_to_tuple(board))
            if history.count(board_to_tuple(board)) >= 3:
                break
            if is_full(board):
                break

            turn = other(turn)

        if winner == mcts_player:
            results['MCTS'] += 1
            label = 'MCTS'
        elif winner == id3_player:
            results['ID3'] += 1
            label = 'ID3'
        else:
            results['draw'] += 1
            label = 'draw'

        first = 'MCTS' if mcts_player == P1 else 'ID3'
        print(f"  Jogo {game+1:>3}  (começa: {first:<4})  →  {label}")

    total = sum(results.values())
    print(f"\n{'='*40}")
    print(f"  RESULTADOS FINAIS ({n_games} jogos)")
    print(f"{'='*40}")
    print(f"  MCTS : {results['MCTS']:>3}  ({100*results['MCTS']/total:.1f}%)")
    print(f"  ID3  : {results['ID3']:>3}  ({100*results['ID3']/total:.1f}%)")
    print(f"  Draws: {results['draw']:>3}  ({100*results['draw']/total:.1f}%)")
    return results

# ---------------------------------------------------------------------------
# Menu interativo
# ---------------------------------------------------------------------------

def menu():
    print("\n" + "="*40)
    print("  PopOut4 — Escolhe o modo de jogo")
    print("="*40)
    print("  1. Humano vs Humano")
    print("  2. Humano vs MCTS")
    print("  3. MCTS vs ID3  (automático)")
    print("  0. Sair")
    print("="*40)

    choice = input("Opção: ").strip()

    if choice == '1':
        play_human_vs_human()
    elif choice == '2':
        side = input("Jogas como X ou O? [X]: ").strip().upper()
        play_human_vs_mcts(human_player=side if side in ('X', 'O') else P1)
    elif choice == '3':
        n = input("Número de jogos? [20]: ").strip()
        tree = load_and_train_id3(DATASET_PATH)
        play_mcts_vs_id3(tree, n_games=int(n) if n.isdigit() else 100)
    elif choice == '0':
        print("Até logo!")
        sys.exit(0)
    else:
        print("Opção inválida.")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else None

    if mode == 'human_human':
        play_human_vs_human()
    elif mode == 'human_mcts':
        play_human_vs_mcts()
    elif mode == 'mcts_id3':
        tree = load_and_train_id3(DATASET_PATH)
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        play_mcts_vs_id3(tree, n_games=n)
    else:
        while True:
            menu()
            again = input("\nJogar outra vez? (s/n): ").strip().lower()
            if again not in ('s', 'sim'):
                break