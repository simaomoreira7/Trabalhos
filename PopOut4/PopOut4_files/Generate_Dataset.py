# Geração de dataset para treino do ID3 do PopOut4
# Executa UCB-V+Smart Rollout contra aleatório durante 8 horas
# Guarda progresso a cada 50 jogos para não perder dados em caso de falha
#
# Utilização: python generate_dataset.py
# Saída: popout_dataset.csv

import time
import random
import pandas as pd

from MCTS import (
    MCTS, encode_state, encode_move
)
from PopOut4 import (
    ROWS, COLS, P1, P2,
    create_board, board_to_tuple,
    check_four, get_moves,
    drop_disc, pop_disc, other, is_full
)

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

HOURS          = 8 # duração da execução
BUDGET_SECS    = HOURS * 3600
N_SIMULATIONS  = 300       # simulações por jogada (300 = melhor equilíbrio qualidade/velocidade)
SAVE_EVERY     = 50        # guardar no CSV a cada N jogos
OUTPUT_PATH    = 'popout_dataset.csv'

# agente principal — variante mais forte do benchmark
# Nota: rollout inteligente está sempre ativo em MCTS._rollout(), sem parâmetro necessário
MCTS_KWARGS = dict(
    c             = 1.41,
    variant       = 'ucbv',
    use_heuristic = False,
    smart_rollout = True,
    n_simulations = N_SIMULATIONS,
)

# ---------------------------------------------------------------------------
# Agente aleatório
# ---------------------------------------------------------------------------

def random_move(board, player):
    drops, pops = get_moves(board, player)
    all_moves = [('drop', c) for c in drops] + [('pop', c) for c in pops]
    return random.choice(all_moves) if all_moves else None


# ---------------------------------------------------------------------------
# Jogo único — MCTS de um lado, oponente do outro
# Apenas as jogadas do MCTS são registadas como amostras de treino.
# oponente: 'random' | 'mcts'
# ---------------------------------------------------------------------------

def play_one_game(agent, mcts_player, opponent, opponent_agent=None):
    board   = create_board()
    turn    = P1
    history = [board_to_tuple(board)]
    samples = []
    winner  = None

    while True:
        p1w = check_four(board, P1)
        p2w = check_four(board, P2)
        if p1w or p2w:
            if p1w and p2w:
                winner = other(turn)  # quem fez o pop ganha
            elif p1w:
                winner = P1
            else:
                winner = P2
            break

        drops, pops = get_moves(board, turn)
        if not drops and not pops:
            break

        if turn == mcts_player:
            move = agent.choose_move(board, turn)
            if move is None:
                break
            samples.append((encode_state(board, turn), encode_move(*move)))
        else:
            if opponent == 'random':
                move = random_move(board, turn)
            else:
                move = opponent_agent.choose_move(board, turn)
            if move is None:
                break

        move_type, col = move
        new_board = (drop_disc(board, col, turn) if move_type == 'drop'
                     else pop_disc(board, col, turn))
        if new_board is None:
            break

        board = new_board
        history.append(board_to_tuple(board))
        turn = other(turn)

        if history.count(board_to_tuple(board)) >= 3:
            break

    if winner is None:
        outcome = 'D'
    elif winner == mcts_player:
        outcome = 'W'
    else:
        outcome = 'L'

    return samples, outcome


# ---------------------------------------------------------------------------
# Ciclo principal de geração
# ---------------------------------------------------------------------------

def generate(hours=HOURS, n_simulations=N_SIMULATIONS, budget_secs=None):
    if budget_secs is None:
        budget_secs = hours * 3600

    kwargs = dict(MCTS_KWARGS)
    kwargs['n_simulations'] = n_simulations

    agent          = MCTS(**kwargs)
    opponent_agent = MCTS(**kwargs)

    all_samples = []
    game_idx    = 0
    start       = time.time()

    results = {'W': 0, 'L': 0, 'D': 0}
    game_log = []  # (game_idx, description, outcome)

    print(f"Starting dataset generation — budget: {hours}h")
    print(f"MCTS config: {kwargs}")
    print(f"Output: {OUTPUT_PATH}\n")

    while time.time() - start < budget_secs:
        elapsed = time.time() - start
        remaining = budget_secs - elapsed

        # escalonamento de tipos de jogo (ciclo repetido de 4):
        #   0: MCTS(X) vs Aleatório(O)
        #   1: Aleatório(X) vs MCTS(O)
        #   2: MCTS(X) vs MCTS(O)   — ambos registados
        #   3: MCTS(O) vs Aleatório(X) (igual a 1, mantém equilíbrio)
        mode = game_idx % 4

        if mode == 0:
            samples, outcome = play_one_game(agent, P1, 'random')
            desc = "MCTS(X) vs Random(O)"
        elif mode == 1:
            samples, outcome = play_one_game(agent, P2, 'random')
            desc = "Random(X) vs MCTS(O)"
        elif mode == 2:
            s1, o1 = play_one_game(agent,          P1, 'mcts', opponent_agent)
            s2, o2 = play_one_game(opponent_agent, P2, 'mcts', agent)
            samples = s1 + s2
            outcome = o1
            desc = "MCTS(X) vs MCTS(O)"
        else:
            samples, outcome = play_one_game(agent, P2, 'random')
            desc = "Random(X) vs MCTS(O)"

        results[outcome] += 1
        game_log.append((game_idx + 1, desc, outcome))
        all_samples.extend(samples)
        game_idx += 1

        # guardar periodicamente
        if game_idx % SAVE_EVERY == 0:
            _save(all_samples)

        # guardar periodicamente
        if game_idx % SAVE_EVERY == 0:
            _save(all_samples)
            elapsed_min = elapsed / 60
            remaining_min = remaining / 60
            rate = game_idx / (elapsed / 3600)
            print(f"  game {game_idx:>5}  |  {len(all_samples):>7} samples  |  "
                  f"{elapsed_min:.0f}min elapsed  {remaining_min:.0f}min left  |  "
                  f"{rate:.0f} games/h")

    # guardar final
    _save(all_samples)
    total_time = time.time() - start
    print(f"\nDone: {game_idx} games, {len(all_samples)} samples "
          f"in {total_time/3600:.2f}h")
    print(f"Saved to {OUTPUT_PATH}")

    _print_stats(all_samples, results, game_log)
    return all_samples


def _save(samples):
    if not samples:
        return
    rows = [dict(feat, move=label) for feat, label in samples]
    df   = pd.DataFrame(rows)
    cols = [c for c in df.columns if c != 'move'] + ['move']
    df[cols].to_csv(OUTPUT_PATH, index=False)


def _print_stats(samples, results, game_log):
    total = sum(results.values())
    wr = results['W'] / total if total else 0

    print(f"\n{'='*55}")
    print(f"  RESULTADOS FINAIS (perspetiva MCTS)")
    print(f"{'='*55}")
    print(f"  W: {results['W']:>4}  L: {results['L']:>4}  D: {results['D']:>4}  "
          f"Total: {total}  Win-rate: {wr:.1%}")

    if not samples:
        return
    from collections import Counter
    labels = [label for _, label in samples]
    counts = Counter(labels)
    print(f"\n{'='*55}")
    print(f"  DISTRIBUIÇÃO DE LABELS ({len(counts)} movimentos únicos)")
    print(f"{'='*55}")
    for move, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        bar = '█' * (cnt * 40 // max(counts.values()))
        print(f"  {move:<12} {cnt:>6}  {bar}")


# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    hours        = float(sys.argv[1]) if len(sys.argv) > 1 else HOURS
    n_simulations = int(sys.argv[2])  if len(sys.argv) > 2 else N_SIMULATIONS
    generate(hours=hours, n_simulations=n_simulations)