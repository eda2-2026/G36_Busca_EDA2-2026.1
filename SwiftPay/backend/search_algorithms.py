"""
Motor de busca do SwiftPay.

Combina índice invertido para campos categóricos e busca binária para campos
ordenados, como data e valor.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Set


def _parse_timestamp_bound(date_text: str, end_of_day: bool = False) -> str:
    """Converte uma data YYYY-MM-DD para o formato ISO usado nas transações."""
    parsed = datetime.strptime(date_text, "%Y-%m-%d")
    suffix = "T23:59:59" if end_of_day else "T00:00:00"
    return parsed.strftime("%Y-%m-%d") + suffix


class InvertedIndex:
    """Índice invertido para busca por categoria e merchant."""

    def __init__(self) -> None:
        self.category_index: Dict[str, Set[int]] = defaultdict(set)
        self.merchant_index: Dict[str, Set[int]] = defaultdict(set)

    def build(self, transactions: List[Dict]) -> None:
        """Monta os índices a partir da lista de transações."""
        self.category_index.clear()
        self.merchant_index.clear()

        for transaction in transactions:
            transaction_id = transaction["id"]
            self.category_index[transaction["category"]].add(transaction_id)
            self.merchant_index[transaction["merchant"]].add(transaction_id)

    def search_by_category(self, category: str) -> Set[int]:
        """Retorna os IDs associados a uma categoria."""
        return set(self.category_index.get(category, set()))

    def search_by_merchant(self, merchant: str) -> Set[int]:
        """Retorna os IDs associados a um merchant."""
        return set(self.merchant_index.get(merchant, set()))

    def get_all_categories(self) -> List[str]:
        """Lista todas as categorias indexadas."""
        return sorted(self.category_index.keys())

    def get_all_merchants(self) -> List[str]:
        """Lista todos os merchants indexados."""
        return sorted(self.merchant_index.keys())


class BinarySearcher:
    """Busca binária para data e valor."""

    def __init__(self, transactions: List[Dict]) -> None:
        self.transactions = transactions
        self.timestamps = [transaction["timestamp"] for transaction in transactions]
        self.amount_pairs = sorted((float(t["amount"]), t["id"]) for t in transactions)
        self.amount_values = [amount for amount, _ in self.amount_pairs]

    def search_by_date_range(self, start_date: Optional[str], end_date: Optional[str]) -> List[int]:
        """Retorna IDs dentro de um intervalo de datas, aceitando limites abertos."""
        left = 0
        right = len(self.transactions)

        if start_date:
            left = bisect_left(self.timestamps, _parse_timestamp_bound(start_date))

        if end_date:
            right = bisect_right(self.timestamps, _parse_timestamp_bound(end_date, end_of_day=True))

        return [self.transactions[index]["id"] for index in range(left, right)]

    def search_by_amount_range(self, min_amount: Optional[float], max_amount: Optional[float]) -> List[int]:
        """Retorna IDs dentro de um intervalo de valores, aceitando limites abertos."""
        lower = float("-inf") if min_amount is None else float(min_amount)
        upper = float("inf") if max_amount is None else float(max_amount)

        if lower > upper:
            return []

        left = bisect_left(self.amount_values, lower)
        right = bisect_right(self.amount_values, upper)
        return [transaction_id for _, transaction_id in self.amount_pairs[left:right]]

    def search_by_exact_date(self, date: str) -> List[int]:
        """Busca todas as transações de uma data específica."""
        return self.search_by_date_range(date, date)


class SearchEngine:
    """Combina índice invertido e busca binária em uma interface única."""

    def __init__(self, transactions: List[Dict]) -> None:
        self.transactions = transactions
        self.id_to_transaction = {transaction["id"]: transaction for transaction in transactions}

        self.inverted_index = InvertedIndex()
        self.inverted_index.build(transactions)

        self.binary_searcher = BinarySearcher(transactions)

    def search_with_filters(
        self,
        category: Optional[str] = None,
        merchant: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
    ) -> List[Dict]:
        """Busca transações combinando qualquer conjunto de filtros."""
        result_ids = set(self.id_to_transaction.keys())

        if category:
            result_ids &= self.inverted_index.search_by_category(category)

        if merchant:
            result_ids &= self.inverted_index.search_by_merchant(merchant)

        if start_date or end_date:
            result_ids &= set(self.binary_searcher.search_by_date_range(start_date, end_date))

        if min_amount is not None or max_amount is not None:
            result_ids &= set(self.binary_searcher.search_by_amount_range(min_amount, max_amount))

        return [transaction for transaction in self.transactions if transaction["id"] in result_ids]

    def get_statistics(self, transactions: List[Dict]) -> Dict:
        """Calcula estatísticas básicas sobre uma lista de transações."""
        if not transactions:
            return {
                "total_transactions": 0,
                "total_amount": 0.0,
                "average_amount": 0.0,
                "min_amount": 0.0,
                "max_amount": 0.0,
            }

        amounts = [float(transaction["amount"]) for transaction in transactions]
        total_amount = sum(amounts)

        return {
            "total_transactions": len(transactions),
            "total_amount": total_amount,
            "average_amount": total_amount / len(amounts),
            "min_amount": min(amounts),
            "max_amount": max(amounts),
        }
