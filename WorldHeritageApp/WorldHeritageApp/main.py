# main.py
import logging
from app import APP
import db

if __name__ == "__main__":
    # Configuração do logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",  # Corrigido: %Y (ano completo) em vez de %^
    )
    
    # Conectar ao banco de dados
    db.connect()
    
    try:
        # Executar a aplicação Flask
        APP.run(host="0.0.0.0", port=9000, debug=True)
    finally:
        # Fechar conexão com o banco de dados
        db.close()