# Árvore de decisão ID3 do zero
# usa gain ratio em vez de information gain simples (evita enviesamento para atributos de alta cardinalidade)
# discretização MDL para valores contínuos
# pruning por redução de erro para manter a árvore pequena
# sem sklearn em lado nenhum

import math
import copy
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter


# --- divisões (sem sklearn) ---

def stratified_split(X, y, test_size=0.3, seed=42):
    # divide cada classe separadamente para manter as proporções
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
    Xtr = X.loc[tr_idx].reset_index(drop=True)
    Xte = X.loc[te_idx].reset_index(drop=True)
    ytr = y.loc[tr_idx].reset_index(drop=True)
    yte = y.loc[te_idx].reset_index(drop=True)
    return Xtr, Xte, ytr, yte


def kfold_split(X, y, k=5, seed=42):
    # k-fold estratificado — devolve (train_X, train_y, test_X, test_y)
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


# --- entropia e gain ratio ---

def entropy(labels):
    n = len(labels)
    if n == 0:
        return 0.0
    counts = Counter(labels)
    return -sum((c/n)*math.log2(c/n) for c in counts.values() if c > 0)


def info_gain(data, labels, attr):
    base = entropy(labels)
    n = len(labels)
    weighted = sum(
        (len(sub := labels[data[attr] == v]) / n) * entropy(sub)
        for v in data[attr].unique()
    )
    return base - weighted


def split_info(data, attr):
    n = len(data)
    result = 0.0
    for v in data[attr].unique():
        p = (data[attr] == v).sum() / n
        if p > 0:
            result -= p * math.log2(p)
    return result


def gain_ratio(data, labels, attr):
    ig = info_gain(data, labels, attr)
    si = split_info(data, attr)
    return ig / si if si > 0 else 0.0


# --- discretização MDL ---

def _mdl_gain(labels, idx):
    n = len(labels)
    left, right = labels[:idx], labels[idx:]
    return entropy(labels) - (len(left)/n)*entropy(left) - (len(right)/n)*entropy(right)


def _mdl_ok(labels, idx):
    n = len(labels)
    left, right = labels[:idx], labels[idx:]
    k  = len(set(labels))
    k1 = len(set(left))
    k2 = len(set(right))
    delta = math.log2(3**k - 2) - (k*entropy(labels) - k1*entropy(left) - k2*entropy(right))
    return _mdl_gain(labels, idx) >= (math.log2(n-1) + delta) / n


def find_cuts(vals, labels):
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
    out = df.copy()
    cuts = {}
    for col in cols:
        cuts[col] = find_cuts(df[col].values, np.array(labels))
        out[col] = df[col].apply(lambda x: bin_col(x, cuts[col], col))
    return out, cuts


def discretise_new(df, cols, cuts):
    out = df.copy()
    for col in cols:
        out[col] = df[col].apply(lambda x: bin_col(x, cuts[col], col))
    return out


# --- árvore ---

class Node:
    def __init__(self):
        self.attr = None
        self.children = {}
        self.label = None
        self.leaf = False
        self.majority = None

    def predict(self, sample):
        if self.leaf:
            return self.label
        val = sample.get(self.attr)
        if val in self.children:
            return self.children[val].predict(sample)
        return self.majority


def id3(data, labels, attrs):
    node = Node()
    node.majority = Counter(labels).most_common(1)[0][0]

    if len(set(labels)) == 1:
        node.leaf = True
        node.label = labels.iloc[0]
        return node

    if not attrs:
        node.leaf = True
        node.label = node.majority
        return node

    best = max(attrs, key=lambda a: gain_ratio(data, labels, a))
    node.attr = best

    for val in data[best].unique():
        mask = data[best] == val
        sub_data = data[mask].drop(columns=[best])
        sub_labels = labels[mask]

        if len(sub_labels) == 0:
            child = Node()
            child.leaf = True
            child.label = node.majority
            child.majority = node.majority
        else:
            child = id3(sub_data, sub_labels, [a for a in attrs if a != best])

        node.children[val] = child

    return node


# --- pruning ---

def predict_all(tree, data):
    return [tree.predict(row) for _, row in data.iterrows()]


def accuracy(tree, data, labels):
    preds = predict_all(tree, data)
    return sum(p == t for p, t in zip(preds, labels)) / len(labels)


def prune(node, val_data, val_labels):
    if node.leaf:
        return node
    for val in node.children:
        node.children[val] = prune(node.children[val], val_data, val_labels)
    acc_before = accuracy(node, val_data, val_labels)
    leaf = Node()
    leaf.leaf = True
    leaf.label = node.majority
    leaf.majority = node.majority
    if accuracy(leaf, val_data, val_labels) > acc_before:
        return leaf
    return node


# --- utilitários ---

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


# --- visualização ---

def _plot_node(node, ax, x, y, dx, dy, parent_xy=None, edge_label=None):
    color = "#4CAF50" if node.leaf else "#2196F3"
    txt = f"{node.label}" if node.leaf else node.attr
    box = dict(boxstyle="round,pad=0.3", fc=color, ec="white", alpha=0.85)
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
        n = len(kids)
        step = dx*2 / max(n-1, 1)
        for i, (val, child) in enumerate(kids):
            cx = (x - dx + i*step) if n > 1 else x
            _plot_node(child, ax, cx, y-dy, dx/2, dy,
                       parent_xy=(x, y-0.02), edge_label=val)


def show_tree(tree, title="Decision Tree"):
    fig, ax = plt.subplots(figsize=(18, 10))
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend(handles=[
        mpatches.Patch(color='#4CAF50', label='leaf'),
        mpatches.Patch(color='#2196F3', label='split')
    ], loc='upper right', fontsize=9)
    _plot_node(tree, ax, 0.5, 0.92, 0.3, 0.13)
    plt.tight_layout()
    plt.savefig("tree_visual.png", dpi=150, bbox_inches='tight')
    plt.show()


# --- carregar e executar ---

def load_iris_csv(path='iris.csv'):
    df = pd.read_csv(path)
    if 'ID' in df.columns:
        df = df.drop(columns=['ID'])
    df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
    return df


def run_iris(path='iris.csv'):
    df = load_iris_csv(path)
    cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    classes = sorted(df['class'].unique())
    print(f"carregados {len(df)} exemplos, classes: {classes}")

    X, y = df[cols], df['class']

    Xtr, Xtmp, ytr, ytmp = stratified_split(X, y, test_size=0.30, seed=42)
    Xv, Xte, yv, yte = stratified_split(Xtmp, ytmp, test_size=0.50, seed=42)
    print(f"divisão: {len(Xtr)} treino / {len(Xv)} validação / {len(Xte)} teste")

    Xtr_d, cuts = discretise(Xtr, cols, ytr)
    Xv_d  = discretise_new(Xv,  cols, cuts)
    Xte_d = discretise_new(Xte, cols, cuts)
    print("limiares:", {c: [round(t, 3) for t in cuts[c]] for c in cols})

    tree = id3(Xtr_d, ytr, list(Xtr_d.columns))
    print(f"antes do pruning: {count_nodes(tree)} nós, profundidade {tree_depth(tree)}, acc {accuracy(tree, Xte_d, yte):.2%}")

    tree = prune(tree, Xv_d, yv)
    print(f"após pruning:  {count_nodes(tree)} nós, profundidade {tree_depth(tree)}, acc {accuracy(tree, Xte_d, yte):.2%}")

    print_tree(tree)

    preds = predict_all(tree, Xte_d)
    for cls in classes:
        mask = yte == cls
        ok = sum(p == cls for p, m in zip(preds, mask) if m)
        print(f"  {cls}: {ok}/{mask.sum()}")

    show_tree(tree, "ID3 — Iris (gain ratio + MDL + pruning)")
    return tree, cuts


if __name__ == '__main__':
    run_iris('iris.csv')
