"""Ponto de entrada para rodar o sistema no seu computador.

    python run.py

Depois abra http://127.0.0.1:5000 no navegador.
Para testar no celular na mesma rede Wi-Fi, use host="0.0.0.0" e acesse
http://SEU-IP:5000 — veja docs/00-guia-do-calouro.md.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
