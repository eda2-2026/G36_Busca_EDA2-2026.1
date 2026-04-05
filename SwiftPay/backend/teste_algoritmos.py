#!/usr/bin/env python3
"""
Script de teste para demonstrar:
1. Busca Indexada (Índice Invertido)
2. Busca Binária
3. Busca Combinada (as duas juntas)
"""

import sys
import json
import time

sys.path.insert(0, 'backend')

from search_algorithms import SearchEngine


def print_section(title):
    """Imprime um título de seção."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_resultado(titulo, resultados, tempo=None):
    """Imprime resultado de uma busca."""
    print(f"✅ {titulo}")
    print(f"   Resultados encontrados: {len(resultados)}")
    if tempo:
        print(f"   Tempo de busca: {tempo:.4f}ms")
    if resultados:
        print(f"   Primeiras 3 transações:")
        for i, trans in enumerate(resultados[:3], 1):
            print(f"      {i}. {trans['date']} | {trans['merchant']} | R$ {trans['amount']:.2f}")


def teste_busca_indexada(engine, transactions):
    """
    Testa APENAS a Busca Indexada (Índice Invertido).
    Algoritmo: O(1) em média para buscas por categoria/merchant
    """
    print_section("TESTE 1: BUSCA INDEXADA (Índice Invertido)")
    print("Complexidade: O(1) - acesso direto pela chave")
    print("Tipo: Busca por CATEGORIA ou MERCHANT\n")

    # Teste 1.1: Busca por Categoria
    print("Teste 1.1: Busca por Categoria = 'Alimentação'")
    inicio = time.time()
    resultados = engine.search_with_filters(category="Alimentação")
    tempo = (time.time() - inicio) * 1000
    print_resultado("Busca por Categoria", resultados, tempo)

    # Teste 1.2: Busca por Merchant
    print("\n\nTeste 1.2: Busca por Merchant = 'Supermercado X'")
    inicio = time.time()
    resultados = engine.search_with_filters(merchant="Supermercado X")
    tempo = (time.time() - inicio) * 1000
    print_resultado("Busca por Merchant", resultados, tempo)

    # Teste 1.3: Busca por 2 Categorias (demonstração)
    print("\n\nTeste 1.3: Busca por 2 Categorias diferentes (sequencial)")
    inicio = time.time()
    r1 = engine.search_with_filters(category="Alimentação")
    r2 = engine.search_with_filters(category="Transporte")
    tempo = (time.time() - inicio) * 1000
    print(f"✅ Busca por 2 categorias")
    print(f"   Alimentação: {len(r1)} resultados")
    print(f"   Transporte: {len(r2)} resultados")
    print(f"   Tempo total: {tempo:.4f}ms")


def teste_busca_binaria(engine, transactions):
    """
    Testa APENAS a Busca Binária.
    Algoritmo: O(log n) para buscas por DATA ou VALOR
    """
    print_section("TESTE 2: BUSCA BINÁRIA")
    print("Complexidade: O(log n) - busca em dados ordenados")
    print("Tipo: Busca por DATA ou VALOR (INTERVALO)\n")

    # Teste 2.1: Busca por Intervalo de Data
    print("Teste 2.1: Busca por Intervalo de Data")
    print("   Data inicial: 2025-01-01")
    print("   Data final: 2025-01-31")
    inicio = time.time()
    resultados = engine.search_with_filters(
        start_date="2025-01-01",
        end_date="2025-01-31"
    )
    tempo = (time.time() - inicio) * 1000
    print_resultado("Busca por Data", resultados, tempo)

    # Teste 2.2: Busca por Intervalo de Valor
    print("\n\nTeste 2.2: Busca por Intervalo de Valor")
    print("   Valor mínimo: R$ 100.00")
    print("   Valor máximo: R$ 200.00")
    inicio = time.time()
    resultados = engine.search_with_filters(
        min_amount=100,
        max_amount=200
    )
    tempo = (time.time() - inicio) * 1000
    print_resultado("Busca por Valor", resultados, tempo)

    # Teste 2.3: Busca por Intervalo Maior
    print("\n\nTeste 2.3: Busca por Intervalo Grande de Valor")
    print("   Valor mínimo: R$ 50.00")
    print("   Valor máximo: R$ 300.00")
    inicio = time.time()
    resultados = engine.search_with_filters(
        min_amount=50,
        max_amount=300
    )
    tempo = (time.time() - inicio) * 1000
    print_resultado("Busca por Valor Grande", resultados, tempo)


def teste_busca_combinada(engine, transactions):
    """
    Testa a COMBINAÇÃO de Índice Invertido + Busca Binária.
    Algoritmo: O(1) + O(log n) = super rápido!
    """
    print_section("TESTE 3: BUSCA COMBINADA (Indexada + Binária)")
    print("Complexidade: O(1) + O(log n) = O(log n)")
    print("Combina: CATEGORIA/MERCHANT + DATA/VALOR\n")

    # Teste 3.1: Categoria + Intervalo de Data
    print("Teste 3.1: Alimentação em Janeiro de 2025")
    print("   Categoria: Alimentação")
    print("   Data: 2025-01-01 a 2025-01-31")
    inicio = time.time()
    resultados = engine.search_with_filters(
        category="Alimentação",
        start_date="2025-01-01",
        end_date="2025-01-31"
    )
    tempo = (time.time() - inicio) * 1000
    print_resultado("Busca Combinada 1", resultados, tempo)

    # Teste 3.2: Categoria + Intervalo de Valor
    print("\n\nTeste 3.2: Alimentação entre R$ 50 e R$ 150")
    print("   Categoria: Alimentação")
    print("   Valor: R$ 50.00 a R$ 150.00")
    inicio = time.time()
    resultados = engine.search_with_filters(
        category="Alimentação",
        min_amount=50,
        max_amount=150
    )
    tempo = (time.time() - inicio) * 1000
    print_resultado("Busca Combinada 2", resultados, tempo)

    # Teste 3.3: Todos os filtros juntos!
    print("\n\nTeste 3.3: BUSCA COMPLETA - Todos os filtros!")
    print("   Categoria: Alimentação")
    print("   Merchant: (cualquer um)")
    print("   Data: 2025-06-01 a 2025-06-30")
    print("   Valor: R$ 75.00 a R$ 175.00")
    inicio = time.time()
    resultados = engine.search_with_filters(
        category="Alimentação",
        start_date="2025-06-01",
        end_date="2025-06-30",
        min_amount=75,
        max_amount=175
    )
    tempo = (time.time() - inicio) * 1000
    stats = engine.get_statistics(resultados)
    print_resultado("Busca Combinada Completa", resultados, tempo)
    if resultados:
        print(f"   Total gasto: R$ {stats['total_amount']:,.2f}")
        print(f"   Média: R$ {stats['average_amount']:.2f}")

    # Teste 3.4: Transporte em Período Específico
    print("\n\nTeste 3.4: Transporte no 2º semestre de 2025")
    print("   Categoria: Transporte")
    print("   Data: 2025-07-01 a 2025-12-31")
    print("   Valor: Qualquer um")
    inicio = time.time()
    resultados = engine.search_with_filters(
        category="Transporte",
        start_date="2025-07-01",
        end_date="2025-12-31"
    )
    tempo = (time.time() - inicio) * 1000
    print_resultado("Busca Combinada 4", resultados, tempo)


def main():
    """Função principal."""
    print("\n" + "🚀 TESTES DE ALGORITMOS DE BUSCA - SwiftPay".center(70))
    print("Sistema de Auditoria de Transações Financeiras\n")

    try:
        # Carregar dados
        print("Carregando dados...")
        with open("data/transactions.json", "r", encoding="utf-8") as f:
            transactions = json.load(f)
        print(f"✅ {len(transactions)} transações carregadas\n")

        # Inicializar SearchEngine
        print("Inicializando SearchEngine...")
        engine = SearchEngine(transactions)
        print("✅ SearchEngine pronto\n")

        # Executar testes
        teste_busca_indexada(engine, transactions)
        teste_busca_binaria(engine, transactions)
        teste_busca_combinada(engine, transactions)

        # Resumo final
        print_section("RESUMO DOS ALGORITMOS")
        print("""
1️⃣  BUSCA INDEXADA (Índice Invertido)
    • Complexidade: O(1) em média
    • Uso: Buscas por CATEGORIA ou MERCHANT
    • Vantagem: Rapidíssima, acesso direto
    • Limitação: Apenas para campos categóricos

2️⃣  BUSCA BINÁRIA
    • Complexidade: O(log n)
    • Uso: Intervalos de DATA ou VALOR
    • Vantagem: Muito rápida mesmo em grandes conjuntos
    • Requisito: Dados ordenados

3️⃣  BUSCA COMBINADA
    • Complexidade: O(1) + O(log n) = O(log n)
    • Uso: Múltiplos filtros juntos
    • Vantagem: Combina o melhor dos dois mundos
    • Resultado: Muito rápido e flexível
        """)

        print("=" * 70)
        print("✓ Todos os testes executados com sucesso!")
        print("=" * 70 + "\n")

    except FileNotFoundError:
        print("❌ Erro: Arquivo 'data/transactions.json' não encontrado!")
        print("Execute primeiro: python3 scripts/generate_data.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
