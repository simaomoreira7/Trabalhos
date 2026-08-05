import pickle
import pandas as pd
from ID3_final import id3

DATASET_PATH = 'popout_dataset.csv'
TREE_CACHE   = 'id3_tree.pkl'

print('A carregar dataset...')
df = pd.read_csv(DATASET_PATH)
X  = df.drop(columns=['move'])
y  = df['move']

print(f'A treinar ID3 com {len(df)} amostras (pode demorar horas)...')
tree = id3(X, y, list(X.columns))

with open(TREE_CACHE, 'wb') as f:
    pickle.dump(tree, f)

print(f'Arvore guardada em {TREE_CACHE} — o jogo ja e instantaneo.')