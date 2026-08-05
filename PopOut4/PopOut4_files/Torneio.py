# =============================================================================
# Torneio de Comparação de Configurações MCTS — PopOut4
# =============================================================================
#
# Corre um torneio round-robin entre várias configurações do agente MCTS
# e produz 3 gráficos:
#
#   1. Heatmap de win-rates cruzados (quem bate quem e com que frequência)
#   2. Bar chart com ranking final de cada configuração (win-rate médio)
#   3. Tempo médio de decisão por configuração
#
# Utilização:
#   python benchmark_mcts.py
#
# Ajusta N_GAMES e CONFIGURATIONS abaixo para controlar o orçamento.
# =============================================================================

import math
import time
import random
import itertools
import collections

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from MCTS import MCTS
from PopOut4 import (
    P1, P2, create_board, board_to_tuple,
    check_four, get_moves, drop_disc, pop_disc,
    other, is_full,
)

# =============================================================================
# Configurações a comparar
# Cada entrada é um dicionário com:
#   'name'  : nome curto para os gráficos
#   resto   : kwargs passados diretamente ao construtor MCTS(...)
# =============================================================================

CONFIGURATIONS = [
    {
        'name': 'Default\n(UCT)',
        'c': math.sqrt(2),
        'variant': 'uct',
        'use_heuristic': False,
        'n_simulations': 300,
        'max_children': None,
    },
    {
        'name': 'UCT\n+ Heuristica',
        'c': math.sqrt(2),
        'variant': 'uct',
        'use_heuristic': True,
        'n_simulations': 300,
        'max_children': None,
    },
    {
        'name': 'UCB-V\n+ Smart Rollout',
        'c': 1.0,
        'variant': 'ucbv',
        'use_heuristic': False,
        'n_simulations': 300,
        'max_children': None,
        'smart_rollout': True,
    },
]

# Número de jogos por par (cada par joga N_GAMES, alternando quem começa)
# Recomendado: >= 20 para resultados estatisticamente fiáveis
N_GAMES = 150

# Semente para reprodutibilidade
RANDOM_SEED = 42


# =============================================================================
# Motor de jogo (sem I/O)
# =============================================================================

def play_one_game(agent1, agent2, first_player=P1, max_turns=200):
    """
    Corre uma partida completa entre dois agentes MCTS.

    Parâmetros:
        agent1      : instância MCTS que joga como P1
        agent2      : instância MCTS que joga como P2
        first_player: quem começa (P1 ou P2)
        max_turns   : limite de turnos para evitar loops infinitos

    Retorna:
        str — 'X' (P1 ganhou), 'O' (P2 ganhou), ou 'draw'
    """
    board = create_board()
    turn = first_player
    history = [board_to_tuple(board)]
    agents = {P1: agent1, P2: agent2}

    for _ in range(max_turns):
        opp = other(turn)

        # Verificar fim de jogo antes de pedir movimento
        if check_four(board, P1):
            return P1
        if check_four(board, P2):
            return P2

        move = agents[turn].choose_move(board, turn)
        if move is None:
            return 'draw'

        move_type, col = move
        new_board = (drop_disc(board, col, turn) if move_type == 'drop'
                     else pop_disc(board, col, turn))
        if new_board is None:
            return 'draw'

        # Verificar vitória após mover
        cur_wins = check_four(new_board, turn)
        opp_wins = check_four(new_board, opp)

        if cur_wins or opp_wins:
            if move_type == 'pop' and cur_wins and opp_wins:
                return turn   # regra do pop simultâneo
            return turn if cur_wins else opp

        board = new_board
        history.append(board_to_tuple(board))

        # Empate por repetição (Regra 3)
        if history.count(board_to_tuple(board)) >= 3:
            return 'draw'

        # Empate por tabuleiro cheio (Regra 2)
        if is_full(board):
            return 'draw'

        turn = opp

    return 'draw'


# =============================================================================
# Torneio round-robin
# =============================================================================

def run_tournament(configs, n_games, seed=42):
    """
    Corre um torneio round-robin entre todas as configurações.

    Cada par (i, j) joga n_games partidas no total:
      - metade com i a começar
      - metade com j a começar
    Isto elimina o viés de primeiro mover.

    Parâmetros:
        configs : lista de dicts de configuração (com chave 'name')
        n_games : nº de jogos por par (deve ser par)
        seed    : semente aleatória

    Retorna:
        results : dict (i, j) -> {'wins': int, 'losses': int, 'draws': int}
        times   : dict i -> lista de tempos de decisão (segundos)
    """
    random.seed(seed)
    np.random.seed(seed)

    n = len(configs)
    # results[(i, j)] = quantas vezes i ganhou a j
    results = collections.defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0})
    times = collections.defaultdict(list)   # tempo por decisão, por config

    pairs = list(itertools.combinations(range(n), 2))
    total_matches = len(pairs) * n_games
    done = 0

    print(f"\n{'='*60}")
    print(f"  Torneio MCTS — {n} configurações, {n_games} jogos/par")
    print(f"  Total de partidas: {total_matches}")
    print(f"{'='*60}\n")

    for i, j in pairs:
        cfg_i = {k: v for k, v in configs[i].items() if k != 'name'}
        cfg_j = {k: v for k, v in configs[j].items() if k != 'name'}

        name_i = configs[i]['name'].replace('\n', ' ')
        name_j = configs[j]['name'].replace('\n', ' ')
        print(f"  {name_i}  vs  {name_j}")

        half = n_games // 2

        for game_num in range(n_games):
            # Alternar quem começa para eliminar viés de primeiro mover
            first = P1 if game_num < half else P2

            # Criar agentes com medição de tempo integrada
            agent_i = TimedMCTS(**cfg_i)
            agent_j = TimedMCTS(**cfg_j)

            if first == P1:
                winner = play_one_game(agent_i, agent_j, first_player=P1)
                times[i].extend(agent_i.move_times)
                times[j].extend(agent_j.move_times)
                if winner == P1:
                    results[(i, j)]['wins'] += 1
                    results[(j, i)]['losses'] += 1
                elif winner == P2:
                    results[(i, j)]['losses'] += 1
                    results[(j, i)]['wins'] += 1
                else:
                    results[(i, j)]['draws'] += 1
                    results[(j, i)]['draws'] += 1
            else:
                winner = play_one_game(agent_j, agent_i, first_player=P1)
                times[i].extend(agent_i.move_times)
                times[j].extend(agent_j.move_times)
                if winner == P1:
                    results[(j, i)]['wins'] += 1
                    results[(i, j)]['losses'] += 1
                elif winner == P2:
                    results[(j, i)]['losses'] += 1
                    results[(i, j)]['wins'] += 1
                else:
                    results[(i, j)]['draws'] += 1
                    results[(j, i)]['draws'] += 1

            done += 1

        w = results[(i, j)]['wins']
        l = results[(i, j)]['losses']
        d = results[(i, j)]['draws']
        print(f"    → {name_i}: {w}W / {l}L / {d}D  "
              f"(win-rate {w/n_games:.0%})\n")

    return results, times


class TimedMCTS(MCTS):
    """
    Subclasse de MCTS que regista o tempo gasto em cada choose_move.
    Permite medir o tempo médio de decisão por configuração sem alterar
    a lógica do algoritmo.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_times = []

    def choose_move(self, board, player):
        t0 = time.time()
        move = super().choose_move(board, player)
        self.move_times.append(time.time() - t0)
        return move


# =============================================================================
# Cálculo de métricas agregadas
# =============================================================================

def compute_winrate_matrix(results, n_configs, n_games):
    """
    Constrói a matriz de win-rates: entry[i][j] = taxa de vitória de i contra j.
    A diagonal é NaN (nenhuma config joga contra si própria).

    Parâmetros:
        results   : dict devolvido por run_tournament
        n_configs : número de configurações
        n_games   : jogos por par (para normalizar)

    Retorna:
        np.ndarray de shape (n_configs, n_configs) com valores em [0, 1] ou NaN
    """
    matrix = np.full((n_configs, n_configs), np.nan)
    for i in range(n_configs):
        for j in range(n_configs):
            if i != j:
                w = results[(i, j)]['wins']
                matrix[i][j] = w / n_games
    return matrix


def compute_overall_winrates(matrix):
    """
    Calcula o win-rate médio de cada configuração contra todas as outras.
    Ignora NaN (diagonal) no cálculo da média.

    Parâmetros:
        matrix : np.ndarray de win-rates (diagonal = NaN)

    Retorna:
        np.ndarray de win-rates médios, um por configuração
    """
    return np.nanmean(matrix, axis=1)


# =============================================================================
# Visualização
# =============================================================================

def plot_results(configs, results, times, n_games, save_path='mcts_tournament.png'):
    """
    Produz e guarda uma figura com 3 subplots:

      1. Heatmap de win-rates — quem ganha a quem e com que frequência
      2. Bar chart de ranking — win-rate médio de cada configuração
      3. Bar chart de tempo   — tempo médio de decisão por configuração

    Parâmetros:
        configs   : lista de dicts de configuração (com chave 'name')
        results   : dict devolvido por run_tournament
        times     : dict de tempos de decisão devolvido por run_tournament
        n_games   : jogos por par
        save_path : caminho onde guardar a imagem
    """
    n = len(configs)
    names = [c['name'] for c in configs]

    matrix = compute_winrate_matrix(results, n, n_games)
    overall = compute_overall_winrates(matrix)
    avg_times = [np.mean(times[i]) if times[i] else 0.0 for i in range(n)]

    # Ordenar por win-rate para o ranking
    rank_order = np.argsort(overall)[::-1]

    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle('Torneio MCTS — Comparação de Configurações', fontsize=14, fontweight='bold', y=1.01)

    # ------------------------------------------------------------------
    # Subplot 1: Heatmap de win-rates
    # ------------------------------------------------------------------
    ax = axes[0]
    # Substituir NaN por 0.5 só para visualização (diagonal)
    display_matrix = np.where(np.isnan(matrix), 0.5, matrix)
    im = ax.imshow(display_matrix, cmap='RdYlGn', vmin=0, vmax=1, aspect='auto')

    # Anotações em cada célula
    for i in range(n):
        for j in range(n):
            if i == j:
                ax.text(j, i, '—', ha='center', va='center',
                        fontsize=10, color='gray')
            else:
                val = matrix[i][j]
                color = 'white' if val < 0.25 or val > 0.75 else 'black'
                ax.text(j, i, f'{val:.0%}', ha='center', va='center',
                        fontsize=9, fontweight='bold', color=color)

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(names, fontsize=8)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel('Adversário (coluna)', fontsize=9)
    ax.set_ylabel('Configuração (linha)', fontsize=9)
    ax.set_title('Win-rate de linha contra coluna\n(verde = ganha mais, vermelho = perde mais)',
                 fontsize=9)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label='Win-rate')

    # ------------------------------------------------------------------
    # Subplot 2: Ranking (win-rate médio)
    # ------------------------------------------------------------------
    ax = axes[1]
    ranked_names = [names[i] for i in rank_order]
    ranked_wr = [overall[i] for i in rank_order]

    # Gradiente de cor: 1º lugar dourado, resto azul
    bar_colors = ['#FFD700' if k == 0 else '#4A90D9' for k in range(n)]
    bars = ax.barh(range(n), ranked_wr, color=bar_colors, edgecolor='white',
                   linewidth=0.8, alpha=0.9)

    # Linha de referência: win-rate aleatório = 1/(n-1) ≈ igual chance
    ax.axvline(1 / (n - 1), color='gray', linestyle='--', linewidth=1,
               label=f'Aleatório (1/{n-1})')

    # Anotação do valor em cada barra
    for bar, wr in zip(bars, ranked_wr):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
                f'{wr:.1%}', va='center', fontsize=8, fontweight='bold')

    ax.set_yticks(range(n))
    ax.set_yticklabels(ranked_names, fontsize=8)
    ax.set_xlabel('Win-rate médio contra todos os adversários', fontsize=9)
    ax.set_title('Ranking Final\n(win-rate médio no torneio)', fontsize=9)
    ax.set_xlim(0, 1.1)
    ax.invert_yaxis()   # 1º lugar no topo
    ax.legend(fontsize=8)

    # Medalhas nos 3 primeiros
    medals = ['🥇', '🥈', '🥉']
    for k, medal in enumerate(medals[:min(3, n)]):
        ax.text(-0.02, k, medal, ha='right', va='center',
                fontsize=12, transform=ax.get_yaxis_transform())

    # ------------------------------------------------------------------
    # Subplot 3: Tempo médio de decisão
    # ------------------------------------------------------------------
    ax = axes[2]
    sorted_by_time = np.argsort(avg_times)
    time_names = [names[i] for i in sorted_by_time]
    time_vals = [avg_times[i] for i in sorted_by_time]

    bars = ax.barh(range(n), time_vals, color='#7B68EE', edgecolor='white',
                   linewidth=0.8, alpha=0.9)

    for bar, t in zip(bars, time_vals):
        ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2,
                f'{t:.3f}s', va='center', fontsize=8)

    ax.set_yticks(range(n))
    ax.set_yticklabels(time_names, fontsize=8)
    ax.set_xlabel('Tempo médio por decisão (segundos)', fontsize=9)
    ax.set_title('Eficiência Temporal\n(menor = mais rápido)', fontsize=9)
    ax.invert_yaxis()

    # ------------------------------------------------------------------
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\nGráfico guardado em: {save_path}")
    plt.show()


# =============================================================================
# Relatório textual no terminal
# =============================================================================

def print_report(configs, results, times, n_games):
    """
    Imprime um relatório formatado no terminal com:
      - Ranking final com win-rates
      - Resultados detalhados de cada confronto
      - Tempos médios de decisão
    """
    n = len(configs)
    names = [c['name'].replace('\n', ' ') for c in configs]
    matrix = compute_winrate_matrix(results, n, n_games)
    overall = compute_overall_winrates(matrix)
    rank_order = np.argsort(overall)[::-1]
    avg_times = [np.mean(times[i]) if times[i] else 0.0 for i in range(n)]

    print(f"\n{'='*60}")
    print("  RANKING FINAL")
    print(f"{'='*60}")
    for pos, i in enumerate(rank_order, 1):
        print(f"  {pos}. {names[i]:<30}  win-rate: {overall[i]:.1%}  "
              f"tempo/jogada: {avg_times[i]:.3f}s")

    print(f"\n{'='*60}")
    print("  CONFRONTOS DETALHADOS")
    print(f"{'='*60}")
    for i, j in itertools.combinations(range(n), 2):
        wi = results[(i, j)]['wins']
        wj = results[(j, i)]['wins']
        d  = results[(i, j)]['draws']
        print(f"  {names[i]:<28} {wi:>2}W  vs  {wj:>2}W  {d:>2}D  "
              f"  {names[j]}")


# =============================================================================
# Ponto de entrada
# =============================================================================

if __name__ == '__main__':
    results, times = run_tournament(CONFIGURATIONS, N_GAMES, seed=RANDOM_SEED)
    print_report(CONFIGURATIONS, results, times, N_GAMES)
    plot_results(CONFIGURATIONS, results, times, N_GAMES,
                 save_path='mcts_tournament.png')
