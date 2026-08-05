# Monte Carlo Tree Search for PopOut4
# Supports two UCB variants:
#   - Standard UCT:  Q + C * sqrt(ln(N) / n)
#   - UCB-V:         Q + sqrt(2 * Var * ln(N) / n) + C * ln(N) / n
#     with an optional heuristic bonus H(s,a) / (n+1) that fades with visits
#
# Configurable parameters:
#   c             : exploration constant (default sqrt(2))
#   variant       : 'uct' or 'ucbv'
#   use_heuristic : add positional bonus (center + threat) to UCB
#   n_simulations : rollout budget per move
#   max_children  : max children expanded per node (None = all)
#   time_limit    : seconds budget (overrides n_simulations if set)

import math
import random
import time
from PopOut4 import (
    ROWS, COLS, EMPTY, P1, P2,
    create_board, print_board, board_to_tuple,
    check_four, get_moves, drop_disc, pop_disc,
    other, is_full, can_drop, can_pop,
)


# ---------------------------------------------------------------------------
# Heuristic bonus H(board, move_type, col, player)
# Combines:
#   - center column preference  (cols closer to center score higher)
#   - immediate win detection   (move wins right now)
#   - opponent block detection  (move blocks opponent's immediate win)
# Returns a value in [0, 1]. Fades with visit count inside UCB so it
# doesn't dominate once a node is well-explored.
# ---------------------------------------------------------------------------

CENTER = COLS // 2
CENTER_WEIGHTS = [1 - abs(c - CENTER) / CENTER for c in range(COLS)]


def heuristic_bonus(board, move_type, col, player):
    score = 0.0

    if move_type == 'drop':
        score += 0.3 * CENTER_WEIGHTS[col]
        new_board = drop_disc(board, col, player)
    else:
        new_board = pop_disc(board, col, player)

    if new_board is None:
        return 0.0

    # immediate win
    if check_four(new_board, player):
        score += 1.0

    # block opponent's immediate win
    opp = other(player)
    if move_type == 'drop':
        opp_board = drop_disc(board, col, opp) if can_drop(board, col) else None
    else:
        opp_board = pop_disc(board, col, opp) if can_pop(board, col, opp) else None

    if opp_board and check_four(opp_board, opp):
        score += 0.7

    return min(score, 1.0)



# ---------------------------------------------------------------------------
# Smart rollout helper
# Priority: immediate win > block opponent win > center > random
# ---------------------------------------------------------------------------

def _best_move(board, moves, player):
    opp = other(player)
    for move_type, col in moves:
        nb = drop_disc(board, col, player) if move_type == "drop" else pop_disc(board, col, player)
        if nb and check_four(nb, player):
            return (move_type, col)
    for move_type, col in moves:
        nb = drop_disc(board, col, opp) if move_type == "drop" else pop_disc(board, col, opp)
        if nb and check_four(nb, opp):
            return (move_type, col)
    drops = [(mt, c) for mt, c in moves if mt == "drop"]
    if drops:
        return min(drops, key=lambda mc: abs(mc[1] - CENTER))
    return random.choice(moves)


# ---------------------------------------------------------------------------
# MCTSNode
# ---------------------------------------------------------------------------

class MCTSNode:
    def __init__(self, board, player, parent=None, move=None):
        """
        board   : current board state (list of lists)
        player  : whose turn it is to move FROM this node
        parent  : parent MCTSNode
        move    : (move_type, col) that led to this node
        """
        self.board = board
        self.player = player
        self.parent = parent
        self.move = move            # ('drop'|'pop', col)

        self.children = []
        self.visits = 0
        self.wins = 0.0             # from perspective of player who MADE the move to here
        self.sq_wins = 0.0          # sum of squared rewards (UCB-V variance estimate)

        self._untried = None        # lazily initialised list of untried moves

    @property
    def untried_moves(self):
        if self._untried is None:
            drops, pops = get_moves(self.board, self.player)
            self._untried = [('drop', c) for c in drops] + [('pop', c) for c in pops]
            random.shuffle(self._untried)
        return self._untried

    def is_terminal(self):
        return (check_four(self.board, P1) or
                check_four(self.board, P2) or
                (is_full(self.board) and not self.untried_moves))

    def is_fully_expanded(self, max_children=None):
        if self.untried_moves:
            return False
        if max_children is not None and len(self.children) >= max_children:
            return True
        return not self.untried_moves

    def apply_move(self, move_type, col):
        if move_type == 'drop':
            return drop_disc(self.board, col, self.player)
        return pop_disc(self.board, col, self.player)

    def ucb_score(self, child, c, variant, use_heuristic):
        """
        UCT:   Q + C * sqrt(ln(N) / n)

        UCB-V: Q + sqrt(2 * Var * ln(N) / n) + C * ln(N) / n
               where Var = E[r^2] - E[r]^2  (sample variance of rollout rewards)
               UCB-V is tighter than UCT when variance is low, wider when
               results are inconsistent — better suited for noisy rollouts.

        Optional heuristic bonus: H(s,a) / (n+1)
               Adds domain knowledge (center preference, win/block detection)
               that is strongest on the first visit and fades asymptotically
               to zero as n grows, so it never dominates the empirical estimate.
        """
        if child.visits == 0:
            return float('inf')

        n = child.visits
        N = self.visits
        q = child.wins / n
        log_N = math.log(N) if N > 0 else 0.0

        if variant == 'uct':
            exploration = c * math.sqrt(log_N / n)

        elif variant == 'ucbv':
            # sample variance of rewards
            variance = max(child.sq_wins / n - q * q, 0.0)
            exploration = math.sqrt(2 * variance * log_N / n) + c * log_N / n

        else:
            raise ValueError(f"Unknown variant '{variant}'. Use 'uct' or 'ucbv'.")

        score = q + exploration

        if use_heuristic and child.move is not None:
            move_type, col = child.move
            h = heuristic_bonus(self.board, move_type, col, self.player)
            score += h / (n + 1)

        return score

    def best_child(self, c, variant, use_heuristic):
        return max(self.children,
                   key=lambda ch: self.ucb_score(ch, c, variant, use_heuristic))

    def most_visited_child(self):
        """Final move selection: pick most visited child (robust, low variance)."""
        return max(self.children, key=lambda ch: ch.visits)


# ---------------------------------------------------------------------------
# MCTS
# ---------------------------------------------------------------------------

class MCTS:
    def __init__(self,
                 c=math.sqrt(2),
                 variant='uct',
                 use_heuristic=False,
                 n_simulations=1000,
                 max_children=None,
                 time_limit=None,
                 smart_rollout=False):
        """
        c             : exploration constant
                        higher  -> more exploration (try new nodes)
                        lower   -> more exploitation (trust best seen)
        variant       : 'uct'   standard UCT (Kocsis & Szepesvari 2006)
                        'ucbv'  UCB-V (Audibert et al. 2009) — variance-aware
        use_heuristic : add fading H/(n+1) positional bonus to UCB score
        n_simulations : MCTS iterations per move (ignored if time_limit set)
        max_children  : cap on children expanded per node (None = all moves)
        time_limit    : seconds budget per move (overrides n_simulations)
        smart_rollout : heavy playout — win > block > center > random
                        also orders expansion by same priority
        """
        self.c = c
        self.variant = variant
        self.use_heuristic = use_heuristic
        self.n_simulations = n_simulations
        self.max_children = max_children
        self.time_limit = time_limit
        self.smart_rollout = smart_rollout

    def choose_move(self, board, player):
        """Run MCTS and return the best (move_type, col)."""
        root = MCTSNode(board, player)

        if self.time_limit:
            deadline = time.time() + self.time_limit
            while time.time() < deadline:
                self._iterate(root)
        else:
            for _ in range(self.n_simulations):
                self._iterate(root)

        if not root.children:
            return None

        best = root.most_visited_child()
        return best.move

    # --- four MCTS phases ---

    def _iterate(self, root):
        node = self._select(root)
        if not node.is_terminal() and node.untried_moves:
            node = self._expand(node)
        result = self._rollout(node)
        self._backpropagate(node, result)

    def _select(self, node):
        """Descend tree following UCB until we reach an unexpanded or terminal node."""
        while (not node.is_terminal() and
               node.is_fully_expanded(self.max_children) and
               node.children):
            node = node.best_child(self.c, self.variant, self.use_heuristic)
        return node

    def _expand(self, node):
        """
        Add one new child for an untried move.
        With smart_rollout, pick highest priority untried move first
        (win > block > center > rest) so best moves get tried first.
        """
        if self.smart_rollout and len(node.untried_moves) > 1:
            best_move = _best_move(node.board, node.untried_moves, node.player)
            node.untried_moves.remove(best_move)
            move_type, col = best_move
        else:
            move_type, col = node.untried_moves.pop()

        new_board = node.apply_move(move_type, col)
        if new_board is None:
            return node
        child = MCTSNode(new_board, other(node.player),
                         parent=node, move=(move_type, col))
        node.children.append(child)
        return child

    def _rollout(self, node):
        """
        Playout to terminal state.
        smart_rollout=False : pure random (vanilla MCTS)
        smart_rollout=True  : heavy playout — priority at each step:
          1. take immediate win
          2. block opponent immediate win
          3. prefer center columns
          4. fall back to random
        Returns 1.0 if the player who moved INTO this node wins,
                0.0 if they lose, 0.5 for draw.
        """
        board = [row[:] for row in node.board]
        current = node.player
        mover = other(node.player)

        while True:
            p1_wins = check_four(board, P1)
            p2_wins = check_four(board, P2)

            if p1_wins or p2_wins:
                if p1_wins and p2_wins:
                    winner = other(current)
                elif p1_wins:
                    winner = P1
                else:
                    winner = P2
                return 1.0 if winner == mover else 0.0

            drops, pops = get_moves(board, current)
            all_moves = [('drop', c) for c in drops] + [('pop', c) for c in pops]

            if not all_moves:
                return 0.5

            if self.smart_rollout:
                move_type, col = _best_move(board, all_moves, current)
            else:
                move_type, col = random.choice(all_moves)

            new_board = (drop_disc(board, col, current) if move_type == 'drop'
                         else pop_disc(board, col, current))
            if new_board is None:
                continue

            board = new_board
            current = other(current)

    def _backpropagate(self, node, result):
        """Walk back to root, flipping result at each level (zero-sum)."""
        while node is not None:
            node.visits += 1
            node.wins += result
            node.sq_wins += result * result
            result = 1.0 - result
            node = node.parent


# ---------------------------------------------------------------------------
# Dataset generation for ID3
# ---------------------------------------------------------------------------

def encode_state(board, player):
    """
    Flat feature dict for ID3:
      cell_r_c  -> 'X', 'O', or '.'   for all 42 cells
      player    -> 'X' or 'O'
    All values are categorical so MDL discretisation is not needed.
    """
    features = {f"cell_{r}_{c}": board[r][c]
                for r in range(ROWS) for c in range(COLS)}
    features['player'] = player
    return features


def encode_move(move_type, col):
    return f"{move_type}_{col}"


def generate_dataset(n_games=200,
                     uct_kwargs=None,
                     ucbv_kwargs=None,
                     verbose=True):
    """
    Generate a dataset by pitting UCT (X) against UCB-V (O) for n_games.
    Every position seen by each agent is recorded as a (state, move) pair,
    so both agents contribute samples — giving more diverse board coverage
    than single-agent self-play.

    UCT  plays as P1 (X) in even games, P2 (O) in odd games.
    UCB-V plays as P2 (O) in even games, P1 (X) in odd games.
    Alternating first mover reduces first-move bias in the dataset.

    Returns list of (feature_dict, label_str).
    """
    if uct_kwargs is None:
        uct_kwargs  = dict(c=math.sqrt(2), variant='uct',
                           use_heuristic=False, n_simulations=200)
    if ucbv_kwargs is None:
        ucbv_kwargs = dict(c=1.0, variant='ucbv',
                           use_heuristic=True,  n_simulations=200)

    agent_uct  = MCTS(**uct_kwargs)
    agent_ucbv = MCTS(**ucbv_kwargs)

    dataset = []
    results  = {P1: 0, P2: 0, 'draw': 0}

    for game_idx in range(n_games):
        # alternate which agent goes first
        if game_idx % 2 == 0:
            agents = {P1: agent_uct, P2: agent_ucbv}
        else:
            agents = {P1: agent_ucbv, P2: agent_uct}

        board  = create_board()
        player = P1
        history = [board_to_tuple(board)]

        while True:
            if check_four(board, P1) or check_four(board, P2):
                break

            drops, pops = get_moves(board, player)
            if not drops and not pops:
                break

            move = agents[player].choose_move(board, player)
            if move is None:
                break

            move_type, col = move
            dataset.append((encode_state(board, player),
                             encode_move(move_type, col)))

            new_board = (drop_disc(board, col, player) if move_type == 'drop'
                         else pop_disc(board, col, player))
            if new_board is None:
                break

            p1w = check_four(new_board, P1)
            p2w = check_four(new_board, P2)
            if p1w or p2w:
                winner = player if (p1w and p2w) else (P1 if p1w else P2)
                results[winner] += 1
                break

            board = new_board
            history.append(board_to_tuple(board))
            player = other(player)

            if history.count(board_to_tuple(board)) >= 3:
                results['draw'] += 1
                break

        if verbose and (game_idx + 1) % 20 == 0:
            print(f"  game {game_idx+1:>4}/{n_games}  —  "
                  f"{len(dataset)} samples  |  "
                  f"X wins {results[P1]}  O wins {results[P2]}  "
                  f"draws {results['draw']}")

    if verbose:
        print(f"\nFinal: {len(dataset)} samples from {n_games} games")
        total = sum(results.values())
        if total:
            print(f"  X wins {results[P1]} ({100*results[P1]/total:.1f}%)  "
                  f"O wins {results[P2]} ({100*results[P2]/total:.1f}%)  "
                  f"draws {results['draw']} ({100*results['draw']/total:.1f}%)")

    return dataset


def dataset_to_csv(dataset, path='popout_dataset.csv'):
    """
    Save dataset to CSV so ID3 can load it with pd.read_csv.
    Columns: cell_0_0 ... cell_5_6, player, move (label).
    """
    import pandas as pd
    if not dataset:
        print("Empty dataset, nothing to save.")
        return

    rows = []
    for features, label in dataset:
        row = dict(features)
        row['move'] = label
        rows.append(row)

    df = pd.DataFrame(rows)
    # put label last
    cols = [c for c in df.columns if c != 'move'] + ['move']
    df = df[cols]
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to '{path}'")
    return df


def dataset_from_csv(path='popout_dataset.csv'):
    """
    Load dataset saved by dataset_to_csv.
    Returns (X DataFrame, y Series) ready for ID3.
    """
    import pandas as pd
    df = pd.read_csv(path)
    X = df.drop(columns=['move'])
    y = df['move']
    print(f"Loaded {len(df)} samples, {y.nunique()} unique moves: {sorted(y.unique())}")
    return X, y