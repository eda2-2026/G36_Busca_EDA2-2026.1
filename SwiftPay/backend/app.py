"""Aplicação Flask do SwiftPay."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from config import Config
from search_algorithms import SearchEngine


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
DATA_FILE = BASE_DIR / "data" / "transactions.json"


app = Flask(__name__, static_folder=str(FRONTEND_DIR))
app.config.from_object(Config)
app.config["TRANSACTIONS_FILE"] = str(DATA_FILE)
CORS(app)

transactions: List[Dict] = []
search_engine: Optional[SearchEngine] = None


def load_transactions() -> List[Dict]:
    """Carrega as transações e inicializa o motor de busca."""
    global transactions, search_engine

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {DATA_FILE}")

    with DATA_FILE.open("r", encoding="utf-8") as file:
        loaded_transactions = json.load(file)

    if not isinstance(loaded_transactions, list):
        raise ValueError("O arquivo de transações deve conter uma lista JSON.")

    transactions = loaded_transactions
    search_engine = SearchEngine(transactions)

    app.logger.info("%s transações carregadas com sucesso", len(transactions))
    return transactions


def get_search_engine() -> SearchEngine:
    """Garante que o motor de busca está pronto para uso."""
    global search_engine

    if search_engine is None:
        load_transactions()

    assert search_engine is not None
    return search_engine


@app.route("/")
def index():
    """Página principal do dashboard."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/css/<path:filename>")
def serve_css(filename: str):
    """Entrega os arquivos CSS do frontend."""
    return send_from_directory(FRONTEND_DIR / "css", filename)


@app.route("/js/<path:filename>")
def serve_js(filename: str):
    """Entrega os arquivos JavaScript do frontend."""
    return send_from_directory(FRONTEND_DIR / "js", filename)


@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    """Lista transações com paginação."""
    page = max(request.args.get("page", 1, type=int) or 1, 1)
    per_page = max(request.args.get("per_page", 50, type=int) or 50, 1)

    start = (page - 1) * per_page
    end = start + per_page

    return jsonify(
        {
            "total": len(transactions),
            "page": page,
            "per_page": per_page,
            "pages": (len(transactions) + per_page - 1) // per_page,
            "data": transactions[start:end],
        }
    )


@app.route("/api/search", methods=["GET"])
def search():
    """Executa buscas combinando filtros opcionais."""
    try:
        engine = get_search_engine()

        category = request.args.get("category") or None
        merchant = request.args.get("merchant") or None
        start_date = request.args.get("start_date") or None
        end_date = request.args.get("end_date") or None
        min_amount = request.args.get("min_amount", type=float)
        max_amount = request.args.get("max_amount", type=float)

        results = engine.search_with_filters(
            category=category,
            merchant=merchant,
            start_date=start_date,
            end_date=end_date,
            min_amount=min_amount,
            max_amount=max_amount,
        )

        return jsonify(
            {
                "success": True,
                "count": len(results),
                "statistics": engine.get_statistics(results),
                "data": results,
                "filters": {
                    "category": category,
                    "merchant": merchant,
                    "start_date": start_date,
                    "end_date": end_date,
                    "min_amount": min_amount,
                    "max_amount": max_amount,
                },
            }
        )

    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 400


@app.route("/api/categories", methods=["GET"])
def get_categories():
    """Lista todas as categorias disponíveis."""
    engine = get_search_engine()
    categories = engine.inverted_index.get_all_categories()
    return jsonify({"categories": categories, "count": len(categories)})


@app.route("/api/merchants", methods=["GET"])
def get_merchants():
    """Lista todos os merchants disponíveis."""
    engine = get_search_engine()
    merchants = engine.inverted_index.get_all_merchants()
    return jsonify({"merchants": merchants, "count": len(merchants)})


@app.route("/api/statistics", methods=["GET"])
def get_statistics():
    """Retorna estatísticas de todas as transações carregadas."""
    engine = get_search_engine()
    return jsonify(engine.get_statistics(transactions))


@app.route("/api/health", methods=["GET"])
def health_check():
    """Verifica se a API está disponível e se os dados foram carregados."""
    return jsonify(
        {
            "status": "ok",
            "transactions_loaded": len(transactions),
            "data_file": str(DATA_FILE),
        }
    )


if __name__ == "__main__":
    load_transactions()

    print("\n🚀 SwiftPay iniciado em http://localhost:5000")
    print("📊 Acesse http://localhost:5000 para usar o dashboard\n")

    app.run(debug=True, host="0.0.0.0", port=5000)

