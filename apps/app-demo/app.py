import os
import socket
from flask import Flask, jsonify

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "desconhecido")
APP_VERSION = os.getenv("APP_VERSION", "0.0.0")

# Flag interna pra simular falha (usada no troubleshooting, Fase 11)
_saudavel = True

@app.route("/")
def home():
    return jsonify(
        mensagem="Ola do homelab Kubernetes!",
        pod=socket.gethostname(),   # nome do pod que respondeu
        ambiente=APP_ENV,
        versao=APP_VERSION,
    )

@app.route("/health")
def health():
    # Liveness: o processo esta vivo?
    if _saudavel:
        return jsonify(status="vivo"), 200
    return jsonify(status="doente"), 500

@app.route("/ready")
def ready():
    # Readiness: pronto pra receber trafego?
    return jsonify(status="pronto"), 200

@app.route("/break")
def break_app():
    # Endpoint de sabotagem: deixa o /health falhar (pra simular liveness quebrada)
    global _saudavel
    _saudavel = False
    return jsonify(mensagem="App marcada como doente. /health vai falhar agora."), 200

if __name__ == "__main__":
    print(f"Iniciando app-demo | env={APP_ENV} versao={APP_VERSION}", flush=True)
    app.run(host="0.0.0.0", port=8080)