#!/usr/bin/env python3
"""Gera dados fictícios para o SwiftPay."""

from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path


DEFAULT_COUNT = 5000
DEFAULT_SEED = 42
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "transactions.json"

CATEGORIES = [
    "Alimentação",
    "Transporte",
    "Saúde",
    "Lazer",
    "Educação",
    "Eletrônicos",
    "Roupas",
    "Moradia",
    "Utilidades",
    "Assinaturas",
]

MERCHANTS = {
    "Alimentação": ["Supermercado X", "Restaurante Y", "Padaria Z", "Mercado ABC", "Lanchonete XYZ"],
    "Transporte": ["Uber", "99Taxi", "Passagem Aérea", "Combustível Shell", "Estacionamento"],
    "Saúde": ["Farmácia Vida", "Clínica Médica", "Dentista Pro", "Hospital ABC", "Laboratório"],
    "Lazer": ["Cinema Cinemark", "Parque Aquático", "Jogo Online", "Streaming Plus", "Bar Noturno"],
    "Educação": ["Cursos Online", "Livros Amazon", "Escola de Idiomas", "Plataforma Edu", "Universidade"],
    "Eletrônicos": ["Amazon", "Kabum", "Mercado Livre", "Apple Store", "Best Buy"],
    "Roupas": ["H&M", "Zara", "Renner", "Lojas Americanas", "Shein"],
    "Moradia": ["Aluguel", "Condomínio", "Água e Luz", "Internet", "Reforma"],
    "Utilidades": ["Limpeza", "Higiene", "Ferragens", "Jardinagem", "Decoração"],
    "Assinaturas": ["Netflix", "Spotify", "Disney+", "Prime Video", "Gym"],
}


def build_parser() -> argparse.ArgumentParser:
    """Configura os argumentos do script."""
    parser = argparse.ArgumentParser(description="Gera dados fictícios para o SwiftPay.")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT, help="Quantidade de transações")
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE, help="Arquivo de saída JSON")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Semente aleatória")
    return parser


def generate_transactions(count: int, seed: int) -> list[dict]:
    """Gera uma lista de transações ordenadas por timestamp."""
    rng = random.Random(seed)
    start_date = datetime.now() - timedelta(days=730)
    statuses = ["Concluída", "Pendente", "Cancelada"]
    transactions: list[dict] = []

    for transaction_id in range(1, count + 1):
        category = rng.choice(CATEGORIES)
        merchant = rng.choice(MERCHANTS[category])
        transaction_date = start_date + timedelta(days=rng.randint(0, 730), seconds=rng.randint(0, 86399))
        amount = round(rng.uniform(5.0, 500.0), 2)

        transactions.append(
            {
                "id": transaction_id,
                "date": transaction_date.strftime("%Y-%m-%d"),
                "timestamp": transaction_date.isoformat(timespec="seconds"),
                "merchant": merchant,
                "category": category,
                "amount": amount,
                "description": f"{merchant} - {category}",
                "status": rng.choice(statuses),
            }
        )

    transactions.sort(key=lambda item: item["timestamp"])
    return transactions


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    print(f"Gerando {args.count} transações fictícias...")
    transactions = generate_transactions(args.count, args.seed)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as file:
        json.dump(transactions, file, ensure_ascii=False, indent=2)

    total_amount = sum(transaction["amount"] for transaction in transactions)
    average_amount = total_amount / len(transactions) if transactions else 0.0

    print(f"✓ {len(transactions)} transações geradas com sucesso!")
    print(f"✓ Arquivo salvo em: {args.output}")
    print("\n📊 Estatísticas:")
    print(f"   Total gasto: R$ {total_amount:,.2f}")
    print(f"   Média por transação: R$ {average_amount:.2f}")
    if transactions:
        print(f"   Período: {transactions[0]['date']} a {transactions[-1]['date']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
