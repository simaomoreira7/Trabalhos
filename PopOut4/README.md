# PopOut4 — Agentes de IA (MCTS + ID3)

Projeto de Inteligência Artificial: agentes de jogo para o PopOut4 (variante do Connect-4) usando Monte Carlo Tree Search (MCTS) e um classificador ID3 (árvore de decisão) treinado sobre um dataset gerado pelo próprio agente MCTS.

## Requisitos

```bash
pip install pandas numpy matplotlib
```

Em sistemas Debian/Ubuntu recentes, o `pip` bloqueia instalações diretas no sistema (erro `externally-managed-environment`). Usa um ambiente virtual:

**Linux/macOS (bash):**
```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy matplotlib
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install pandas numpy matplotlib
```

> No Windows, o `pip install` costuma funcionar diretamente sem `externally-managed-environment` (é uma proteção específica de distros Linux), mas continua a ser boa prática usar o `venv` para não misturar dependências com outros projetos.

## Como jogar

O jogo corre a partir do `PLAY.py`, com três modos (comandos iguais em bash e PowerShell, desde que o `venv` esteja ativado):

```bash
python PLAY.py human_human   # Humano vs Humano
python PLAY.py human_mcts    # Humano vs MCTS
python PLAY.py mcts_id3      # MCTS vs ID3 (20 jogos automáticos)
python PLAY.py               # menu interativo, para escolher o modo
```

> Para os modos que usam o ID3 (`mcts_id3`), é preciso ter o ficheiro `id3_tree.pkl` na pasta — já vem incluído no projeto. Se precisares de o gerar de novo (ver secção abaixo), corre `python ID3_Treino.py` antes de jogar.

## Estrutura do projeto

```
ficheiros/
├── PLAY.py                    # interface de jogo, todos os modos
├── PopOut4.py                  # regras e lógica do jogo (tabuleiro, jogadas, vitória)
├── MCTS.py                     # implementação do agente MCTS (UCT e UCB-V)
├── ID3_final.py                # implementação do algoritmo ID3
├── ID3_Treino.py                # treina o ID3 a partir do dataset e guarda id3_tree.pkl
├── ID3_Iris.py                  # validação do ID3 num dataset de referência (Iris)
├── Generate_Dataset.py          # gera popout_dataset.csv a partir de partidas MCTS
├── Torneio.py                   # torneio round-robin entre configurações de MCTS
├── PopOut4_AI_Notebook.ipynb     # notebook com toda a análise e experimentação
├── popout_dataset.csv           # dataset gerado para treino do ID3
├── id3_tree.pkl                 # árvore de decisão já treinada (pronta a usar)
└── *.png                        # gráficos gerados (matriz de confusão, torneio, árvore)
```

## Passo a passo para reproduzir tudo do zero

1. **Gerar o dataset** (opcional — já vem um pronto em `popout_dataset.csv`):
   ```bash
   python Generate_Dataset.py
   ```
   Corre partidas de MCTS (UCB-V + Smart Rollout) contra um agente aleatório durante várias horas, guardando progresso a cada 50 jogos.

2. **Treinar o ID3** a partir do dataset:
   ```bash
   python ID3_Treino.py
   ```
   Gera `id3_tree.pkl`, para o jogo não precisar de treinar em tempo real.

3. **Comparar configurações de MCTS** (exploração, heurística, rollout, etc.):
   ```bash
   python Torneio.py
   ```
   Produz um heatmap de win-rates, um ranking por configuração e o tempo médio de decisão de cada uma.

4. **Jogar / testar os agentes**:
   ```bash
   python PLAY.py mcts_id3
   ```

## Análise completa

Todo o processo — geração de dados, treino, validação do ID3 e experimentação com parâmetros do MCTS — está documentado passo a passo em `PopOut4_AI_Notebook.ipynb`.
