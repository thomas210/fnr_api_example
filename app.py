import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request


app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        mensagem="API de exemplo para Computação em Nuvem",
        disciplina="Computação em Nuvem e Web Services",
        endpoints=["/health", "/saudacao/<nome>", "/info"],
    )


@app.get("/health")
def health():
    return jsonify(
        status="ok",
        instante=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/saudacao/<nome>")
def saudacao(nome):
    idioma = request.args.get("idioma", "pt").lower()
    mensagens = {
        "pt": f"Olá, {nome}!",
        "en": f"Hello, {nome}!",
        "es": f"¡Hola, {nome}!",
    }

    return jsonify(
        mensagem=mensagens.get(idioma, mensagens["pt"]),
        idioma=idioma if idioma in mensagens else "pt",
    )


@app.get("/info")
def info():
    return jsonify(
        ambiente=os.getenv("APP_ENV", "desenvolvimento"),
        provedor=os.getenv("CLOUD_PROVIDER", "local"),
        versao=os.getenv("APP_VERSION", "1.0.0"),
        observacao="Os valores são definidos por variáveis de ambiente.",
    )


@app.errorhandler(404)
def nao_encontrado(_erro):
    return jsonify(erro="Endpoint não encontrado"), 404


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG") == "1")
