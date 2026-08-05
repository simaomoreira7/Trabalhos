# World Heritage App

Aplicação web em Flask para consultar o Património Mundial da UNESCO, com pesquisa avançada, filtragem por país, região e categoria, e queries SQL personalizadas sobre os dados.

## Requisitos

- Python 3.10+
- Flask

Em sistemas Debian/Ubuntu recentes, o `pip` bloqueia instalações diretas no sistema (erro `externally-managed-environment`). Usa um ambiente virtual:

**Linux/macOS (bash):**
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install flask
```

> No Windows, o `pip install` costuma funcionar diretamente sem `externally-managed-environment` (é uma proteção específica de distros Linux), mas continua a ser boa prática usar o `venv` para não misturar dependências com outros projetos.

## Como correr

Com o `venv` ativado (bash ou PowerShell, comando igual nos dois):

```bash
python main.py
```

A aplicação liga-se automaticamente à base de dados `unesco.db` (incluída no repositório) e fica disponível em:

```
http://localhost:9000
```

> Nota: existe também um `server.py` com a mesma lógica de arranque numa porta diferente (9005) — usa qualquer um dos dois, `main.py` é a versão principal.

## Estrutura do projeto

```
WorldHeritageApp/
├── main.py          # ponto de entrada, arranca o servidor Flask
├── app.py           # rotas e lógica da aplicação
├── db.py            # ligação e queries à base de dados SQLite
├── unesco.db         # base de dados com os sítios do Património Mundial
├── static/           # CSS
└── templates/         # páginas HTML (pesquisa, listas, detalhe de sítio, etc.)
```

## Funcionalidades

- Listagem de sítios, países, regiões, categorias e critérios de classificação
- Pesquisa avançada com filtros combinados
- Página de sítios "em perigo"
- Execução de queries SQL personalizadas sobre o dataset
