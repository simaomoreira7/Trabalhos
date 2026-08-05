# ID3 decision tree from scratch
# uses gain ratio instead of plain info gain (avoids bias toward high-cardinality attrs)
# MDL discretisation for continuous values
# reduced error pruning to keep the tree small
# k-fold cross-validation for robust evaluation
# confusion matrix for PopOut analysis
# no sklearn used anywhere

import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter


# =============================================================================
# Splits
# =============================================================================

def stratified_split(X, y, test_size=0.3, seed=42):
    """
    Divide dataset em treino/teste mantendo a proporção de cada classe.
    Garante que nenhuma classe fica desproporcionalmente representada.
    """
    random.seed(seed)
    classes = y.unique()
    tr_idx, te_idx = [], []
    for cls in classes:
        idx = list(y[y == cls].index)
        random.shuffle(idx)
        cut = int(len(idx) * (1 - test_size))
        tr_idx += idx[:cut]
        te_idx += idx[cut:]
    random.shuffle(tr_idx); random.shuffle(te_idx)
    return (X.loc[tr_idx].reset_index(drop=True),
            X.loc[te_idx].reset_index(drop=True),
            y.loc[tr_idx].reset_index(drop=True),
            y.loc[te_idx].reset_index(drop=True))


def kfold_split(X, y, k=5, seed=42):
    """
    Gerador de k folds estratificados.
    Cada iteração devolve (X_train, X_test, y_train, y_test).
    Todos os exemplos são usados para teste exatamente uma vez.
    """
    random.seed(seed)
    classes = y.unique()
    folds = [[] for _ in range(k)]
    for cls in classes:
        idx = list(y[y == cls].index)
        random.shuffle(idx)
        for i, j in enumerate(idx):
            folds[i % k].append(j)
    for f in range(k):
        te_idx = folds[f]
        tr_idx = [j for i, fold in enumerate(folds) if i != f for j in fold]
        yield (X.loc[tr_idx].reset_index(drop=True),
               y.loc[tr_idx].reset_index(drop=True),
               X.loc[te_idx].reset_index(drop=True),
               y.loc[te_idx].reset_index(drop=True))


# =============================================================================
# Entropia e Gain Ratio
# =============================================================================

def entropy(labels):
    """Entropia de Shannon: H = -Σ p(c) * log2(p(c))"""
    n = len(labels)
    if n == 0:
        return 0.0
    counts = Counter(labels)
    return -sum((c/n)*math.log2(c/n) for c in counts.values() if c > 0)


def info_gain(data, labels, attr):
    """Information Gain: redução de entropia ao dividir por `attr`."""
    base = entropy(labels)
    n = len(labels)
    weighted = sum(
        (len(sub := labels[data[attr] == v]) / n) * entropy(sub)
        for v in data[attr].unique()
    )
    return base - weighted


def split_info(data, attr):
    """Split Info: entropia da divisão (penaliza atributos com muitos valores)."""
    n = len(data)
    result = 0.0
    for v in data[attr].unique():
        p = (data[attr] == v).sum() / n
        if p > 0:
            result -= p * math.log2(p)
    return result


def gain_ratio(data, labels, attr):
    """Gain Ratio = Info Gain / Split Info. Evita viés para atributos com muitos valores."""
    ig = info_gain(data, labels, attr)
    si = split_info(data, attr)
    return ig / si if si > 0 else 0.0


# =============================================================================
# Discretização MDL (para atributos contínuos como o Iris)
# =============================================================================

def _mdl_gain(labels, idx):
    n = len(labels)
    left, right = labels[:idx], labels[idx:]
    return entropy(labels) - (len(left)/n)*entropy(left) - (len(right)/n)*entropy(right)


def _mdl_ok(labels, idx):
    """Critério MDL de Fayyad & Irani: só aceita corte se a melhoria justificar a complexidade."""
    n = len(labels)
    left, right = labels[:idx], labels[idx:]
    k  = len(set(labels))
    k1 = len(set(left))
    k2 = len(set(right))
    delta = math.log2(3**k - 2) - (k*entropy(labels) - k1*entropy(left) - k2*entropy(right))
    return _mdl_gain(labels, idx) >= (math.log2(n-1) + delta) / n


def find_cuts(vals, labels):
    """Encontra os melhores pontos de corte para discretizar um atributo contínuo."""
    idx = np.argsort(vals)
    sv, sl = vals[idx], labels[idx]

    def recurse(a, b):
        if b - a < 2:
            return []
        best_g, best_i = -1, None
        for i in range(a+1, b):
            if sl[i] != sl[i-1]:
                g = _mdl_gain(sl[a:b], i-a)
                if g > best_g:
                    best_g, best_i = g, i
        if best_i is None or not _mdl_ok(sl[a:b], best_i-a):
            return []
        cut = (sv[best_i-1] + sv[best_i]) / 2
        return recurse(a, best_i) + [cut] + recurse(best_i, b)

    return sorted(recurse(0, len(sv)))


def bin_col(x, cuts, col):
    for t in cuts:
        if x <= t:
            return f"{col}<={t:.2f}"
    return f"{col}>{cuts[-1]:.2f}" if cuts else f"{col}=any"


def discretise(df, cols, labels):
    """Discretiza colunas contínuas usando MDL. Devolve df discretizado e os cortes."""
    out = df.copy()
    cuts = {}
    for col in cols:
        cuts[col] = find_cuts(df[col].values, np.array(labels))
        out[col] = df[col].apply(lambda x: bin_col(x, cuts[col], col))
    return out, cuts


def discretise_new(df, cols, cuts):
    """Aplica cortes já calculados a um novo dataset (validação/teste)."""
    out = df.copy()
    for col in cols:
        out[col] = df[col].apply(lambda x: bin_col(x, cuts[col], col))
    return out


# =============================================================================
# Árvore de Decisão ID3
# =============================================================================

class Node:
    """
    Nó da árvore de decisão.
    - Nós internos: têm `attr` (atributo de divisão) e `children` (dict valor→filho)
    - Folhas: têm `leaf=True` e `label` (classe prevista)
    - `majority`: classe mais frequente no treino — usado como fallback para
      valores não vistos durante o treino
    """
    def __init__(self):
        self.attr     = None
        self.children = {}
        self.label    = None
        self.leaf     = False
        self.majority = None

    def predict(self, sample):
        if self.leaf:
            return self.label
        val = sample.get(self.attr)
        if val in self.children:
            return self.children[val].predict(sample)
        return self.majority   # fallback para valores desconhecidos


def id3(data, labels, attrs):
    """
    Constrói recursivamente uma árvore de decisão ID3.

    Critérios de paragem:
      1. Todos os exemplos têm a mesma classe → folha
      2. Não há mais atributos para dividir → folha com classe maioritária
      3. Subconjunto vazio → folha com classe maioritária do pai

    Em cada nó escolhe o atributo com maior Gain Ratio.
    """
    node = Node()
    node.majority = Counter(labels).most_common(1)[0][0]

    # Critério 1: conjunto puro
    if len(set(labels)) == 1:
        node.leaf  = True
        node.label = labels.iloc[0]
        return node

    # Critério 2: sem atributos
    if not attrs:
        node.leaf  = True
        node.label = node.majority
        return node

    # Escolher o melhor atributo por Gain Ratio
    best      = max(attrs, key=lambda a: gain_ratio(data, labels, a))
    node.attr = best

    for val in data[best].unique():
        mask       = data[best] == val
        sub_data   = data[mask].drop(columns=[best])
        sub_labels = labels[mask]

        if len(sub_labels) == 0:
            # Critério 3: subconjunto vazio
            child          = Node()
            child.leaf     = True
            child.label    = node.majority
            child.majority = node.majority
        else:
            child = id3(sub_data, sub_labels, [a for a in attrs if a != best])

        node.children[val] = child

    return node


# =============================================================================
# Poda (Reduced Error Pruning)
# =============================================================================

def predict_all(tree, data):
    """Aplica a árvore a todos os exemplos de um dataset."""
    return [tree.predict(row) for _, row in data.iterrows()]


def accuracy(tree, data, labels):
    """Acurácia da árvore num dataset."""
    preds = predict_all(tree, data)
    return sum(p == t for p, t in zip(preds, labels)) / len(labels)


def prune(node, val_data, val_labels):
    """
    Reduced Error Pruning: percorre a árvore de baixo para cima.
    Substitui cada nó interno por uma folha se isso não piorar a acurácia
    no conjunto de validação. Resultado: árvore mais pequena, menos overfitting.
    """
    if node.leaf:
        return node
    for val in node.children:
        node.children[val] = prune(node.children[val], val_data, val_labels)
    acc_before = accuracy(node, val_data, val_labels)
    leaf = Node()
    leaf.leaf     = True
    leaf.label    = node.majority
    leaf.majority = node.majority
    if accuracy(leaf, val_data, val_labels) >= acc_before:
        return leaf
    return node


# =============================================================================
# Helpers de análise
# =============================================================================

def count_nodes(node):
    if node.leaf:
        return 1
    return 1 + sum(count_nodes(c) for c in node.children.values())


def tree_depth(node):
    if node.leaf:
        return 0
    return 1 + max(tree_depth(c) for c in node.children.values())


def print_tree(node, indent=0, branch=None):
    pad = "    " * indent
    if branch is not None:
        print(f"{pad}[{branch}]")
        pad += "  "
    if node.leaf:
        print(f"{pad}-> {node.label}")
    else:
        print(f"{pad}{node.attr}")
        for val, child in node.children.items():
            print_tree(child, indent+1, val)


def confusion_matrix_plot(preds, labels, classes, title="Confusion Matrix", save_path=None):
    """
    Plota a matriz de confusão.

    Parâmetros:
        preds     : lista de previsões
        labels    : lista de labels verdadeiros
        classes   : lista de classes (ordem das linhas/colunas)
        title     : título do gráfico
        save_path : se definido, guarda a imagem neste caminho
    """
    n = len(classes)
    idx = {c: i for i, c in enumerate(classes)}
    matrix = np.zeros((n, n), dtype=int)

    for p, t in zip(preds, labels):
        if p in idx and t in idx:
            matrix[idx[t]][idx[p]] += 1

    fig, ax = plt.subplots(figsize=(max(8, n*0.8), max(6, n*0.7)))
    im = ax.imshow(matrix, cmap='Blues')

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(classes, rotation=45, ha='right', fontsize=8)
    ax.set_yticklabels(classes, fontsize=8)
    ax.set_xlabel('Previsão', fontsize=10)
    ax.set_ylabel('Real', fontsize=10)
    ax.set_title(title, fontsize=12, fontweight='bold')

    # Anotações em cada célula
    thresh = matrix.max() / 2
    for i in range(n):
        for j in range(n):
            if matrix[i][j] > 0:
                ax.text(j, i, str(matrix[i][j]),
                        ha='center', va='center', fontsize=7,
                        color='white' if matrix[i][j] > thresh else 'black')

    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  Matriz de confusão guardada em: {save_path}")

    plt.show()


# =============================================================================
# Visualização da árvore
# =============================================================================

def _plot_node(node, ax, x, y, dx, dy, parent_xy=None, edge_label=None):
    color = "#4CAF50" if node.leaf else "#2196F3"
    txt   = f"{node.label}" if node.leaf else node.attr
    box   = dict(boxstyle="round,pad=0.3", fc=color, ec="white", alpha=0.85)
    ax.text(x, y, txt, ha='center', va='center', fontsize=7,
            color='white', fontweight='bold', bbox=box, transform=ax.transAxes)
    if parent_xy:
        ax.annotate("", xy=(x, y+0.03), xytext=parent_xy,
                    xycoords='axes fraction', textcoords='axes fraction',
                    arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.2))
        mx = (x + parent_xy[0]) / 2
        my = (y + parent_xy[1]) / 2 + 0.01
        ax.text(mx, my, str(edge_label), ha='center', va='bottom',
                fontsize=5.5, color="#333", transform=ax.transAxes)
    if not node.leaf:
        kids = list(node.children.items())
        n    = len(kids)
        step = dx*2 / max(n-1, 1)
        for i, (val, child) in enumerate(kids):
            cx = (x - dx + i*step) if n > 1 else x
            _plot_node(child, ax, cx, y-dy, dx/2, dy,
                       parent_xy=(x, y-0.02), edge_label=val)


def show_tree(tree, title="Decision Tree", save_path="tree_visual.png"):
    fig, ax = plt.subplots(figsize=(18, 10))
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend(handles=[
        mpatches.Patch(color='#4CAF50', label='leaf'),
        mpatches.Patch(color='#2196F3', label='split')
    ], loc='upper right', fontsize=9)
    _plot_node(tree, ax, 0.5, 0.92, 0.3, 0.13)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"  Árvore guardada em: {save_path}")


# =============================================================================
# Pipeline Iris
# =============================================================================

def load_iris_csv(path='iris.csv'):
    df = pd.read_csv(path)
    if 'ID' in df.columns:
        df = df.drop(columns=['ID'])
    df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
    return df


def run_iris(path='iris.csv'):
    """Pipeline completo ID3 no dataset Iris com MDL, poda e k-fold."""
    df      = load_iris_csv(path)
    cols    = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    classes = sorted(df['class'].unique())
    print(f"Iris: {len(df)} amostras, classes: {classes}")

    X, y = df[cols], df['class']

    # Divisão 70/15/15
    Xtr, Xtmp, ytr, ytmp = stratified_split(X, y, test_size=0.30, seed=42)
    Xv,  Xte,  yv,  yte  = stratified_split(Xtmp, ytmp, test_size=0.50, seed=42)
    print(f"Split: {len(Xtr)} treino / {len(Xv)} val / {len(Xte)} teste")

    # Discretização MDL
    Xtr_d, cuts = discretise(Xtr, cols, ytr)
    Xv_d        = discretise_new(Xv,  cols, cuts)
    Xte_d       = discretise_new(Xte, cols, cuts)
    print("Cortes MDL:", {c: [round(t, 3) for t in cuts[c]] for c in cols})

    # Treinar e podar
    tree = id3(Xtr_d, ytr, list(Xtr_d.columns))
    print(f"\nAntes da poda : {count_nodes(tree)} nós, profundidade {tree_depth(tree)}, "
          f"acc {accuracy(tree, Xte_d, yte):.2%}")
    tree = prune(tree, Xv_d, yv)
    print(f"Depois da poda: {count_nodes(tree)} nós, profundidade {tree_depth(tree)}, "
          f"acc {accuracy(tree, Xte_d, yte):.2%}")

    # Por classe
    preds = predict_all(tree, Xte_d)
    print("\nAcurácia por classe:")
    for cls in classes:
        mask = yte == cls
        ok   = sum(p == cls for p, m in zip(preds, mask) if m)
        print(f"  {cls}: {ok}/{mask.sum()}")

    # k-fold
    print("\nValidação cruzada k-fold (k=5):")
    fold_accs = []
    for fold_i, (Xf_tr, yf_tr, Xf_te, yf_te) in enumerate(kfold_split(X, y, k=5)):
        Xf_tr_d, c = discretise(Xf_tr, cols, yf_tr)
        Xf_te_d    = discretise_new(Xf_te, cols, c)
        t = id3(Xf_tr_d, yf_tr, list(Xf_tr_d.columns))
        acc_fold = accuracy(t, Xf_te_d, yf_te)
        fold_accs.append(acc_fold)
        print(f"  Fold {fold_i+1}: {acc_fold:.2%}")
    print(f"  Média: {np.mean(fold_accs):.2%}  ±{np.std(fold_accs):.2%}")

    show_tree(tree, "ID3 — Iris (gain ratio + MDL + pruning)")
    print_tree(tree)
    return tree, cuts


# =============================================================================
# Pipeline PopOut — movimento exato
# =============================================================================

def run_popout(path='popout_dataset.csv'):
    """
    ID3 no dataset PopOut para prever o movimento exato (drop_N ou pop_N).
    Não precisa de discretização — as features de célula já são categóricas.
    Inclui k-fold e matriz de confusão.
    """
    df = pd.read_csv(path)
    print(f"PopOut dataset: {len(df)} amostras")

    feature_cols = [c for c in df.columns if c != 'move']
    X = df[feature_cols]
    y = df['move']

    moves = sorted(y.unique())
    print(f"Movimentos únicos ({len(moves)}): {moves}")
    print(f"\nDistribuição:\n{y.value_counts().to_string()}\n")

    # Divisão 70/15/15
    Xtr, Xtmp, ytr, ytmp = stratified_split(X, y, test_size=0.30, seed=42)
    Xv,  Xte,  yv,  yte  = stratified_split(Xtmp, ytmp, test_size=0.50, seed=42)
    print(f"Split: {len(Xtr)} treino / {len(Xv)} val / {len(Xte)} teste")

    # Treinar
    print("\nA treinar árvore ID3...")
    t0   = __import__('time').perf_counter()
    tree = id3(Xtr, ytr, list(Xtr.columns))
    dt   = __import__('time').perf_counter() - t0
    print(f"  Treino concluído em {dt:.1f}s")

    acc_before = accuracy(tree, Xte, yte)
    print(f"\nAntes da poda : {count_nodes(tree)} nós, "
          f"profundidade {tree_depth(tree)}, acc {acc_before:.2%}")

    tree = prune(tree, Xv, yv)
    acc_after = accuracy(tree, Xte, yte)
    print(f"Depois da poda: {count_nodes(tree)} nós, "
          f"profundidade {tree_depth(tree)}, acc {acc_after:.2%}")

    # Acurácia por movimento
    preds = predict_all(tree, Xte)
    print(f"\nAcurácia por movimento:")
    for move in moves:
        mask    = [t == move for t in yte]
        if not any(mask):
            continue
        correct = sum(p == move for p, m in zip(preds, mask) if m)
        total   = sum(mask)
        print(f"  {move:<12} {correct:>4}/{total:<4}  ({100*correct/total:.0f}%)")

    # Acurácia do tipo (drop vs pop)
    correct_type = sum(p.split('_')[0] == t.split('_')[0]
                       for p, t in zip(preds, yte))
    print(f"\nAcurácia do tipo (drop vs pop): "
          f"{correct_type}/{len(yte)} ({100*correct_type/len(yte):.1f}%)")
    print(f"Atributo raiz: {tree.attr}")

    # Matriz de confusão
    confusion_matrix_plot(
        preds, list(yte), moves,
        title="Matriz de Confusão — ID3 PopOut (movimento exato)",
        save_path="confusion_matrix_popout.png"
    )

    # K-fold (k=5) para avaliação robusta
    print("\nValidação cruzada k-fold (k=5):")
    fold_accs  = []
    fold_types = []
    for fold_i, (Xf_tr, yf_tr, Xf_te, yf_te) in enumerate(kfold_split(X, y, k=5)):
        t = id3(Xf_tr, yf_tr, list(Xf_tr.columns))
        # poda simples sem validação separada em k-fold (usa 10% do treino)
        Xf_tr2, yf_tr2, Xf_v, yf_v = (
            Xf_tr.iloc[:int(len(Xf_tr)*0.9)].reset_index(drop=True),
            yf_tr.iloc[:int(len(yf_tr)*0.9)].reset_index(drop=True),
            Xf_tr.iloc[int(len(Xf_tr)*0.9):].reset_index(drop=True),
            yf_tr.iloc[int(len(yf_tr)*0.9):].reset_index(drop=True),
        )
        t = id3(Xf_tr2, yf_tr2, list(Xf_tr2.columns))
        t = prune(t, Xf_v, yf_v)

        fp         = predict_all(t, Xf_te)
        acc_fold   = sum(p == tv for p, tv in zip(fp, yf_te)) / len(yf_te)
        type_fold  = sum(p.split('_')[0] == tv.split('_')[0]
                         for p, tv in zip(fp, yf_te)) / len(yf_te)
        fold_accs.append(acc_fold)
        fold_types.append(type_fold)
        print(f"  Fold {fold_i+1}: acc={acc_fold:.2%}  tipo={type_fold:.2%}")

    print(f"\n  Média acc  : {np.mean(fold_accs):.2%}  ±{np.std(fold_accs):.2%}")
    print(f"  Média tipo : {np.mean(fold_types):.2%}  ±{np.std(fold_types):.2%}")

    return tree


# =============================================================================
# Entry point
# =============================================================================

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'popout':
        path = sys.argv[2] if len(sys.argv) > 2 else 'popout_dataset.csv'
        run_popout(path)
    else:
        run_iris('iris.csv')
