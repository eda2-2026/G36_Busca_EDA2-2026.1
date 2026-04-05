#!/usr/bin/env python3
"""
Script para verificar se o projeto SwiftPay está pronto para rodar.
Execute: python3 test_project.py
"""

import sys
import os
import json

def check_structure():
    """Verificar estrutura de pastas."""
    print("\n📁 Verificando Estrutura...")
    required = [
        "backend/app.py",
        "backend/search_algorithms.py",
        "frontend/index.html",
        "frontend/css/style.css",
        "frontend/js/main.js",
        "scripts/generate_data.py",
        "requirements.txt",
    ]

    for file in required:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} NÃO ENCONTRADO")
            return False
    return True

def check_data():
    """Verificar dados."""
    print("\n📊 Verificando Dados...")
    if os.path.exists("data/transactions.json"):
        try:
            with open("data/transactions.json", "r") as f:
                data = json.load(f)
            print(f"  ✅ data/transactions.json ({len(data)} transações)")
            return True
        except:
            print("  ❌ arquivo corrompido")
            return False
    else:
        print("  ⚠️  data/transactions.json NÃO ENCONTRADO")
        print("     Execute: python3 scripts/generate_data.py")
        return False

def check_imports():
    """Verificar imports."""
    print("\n📦 Verificando Imports...")
    sys.path.insert(0, "backend")

    try:
        from flask import Flask
        print("  ✅ Flask instalado")
    except:
        print("  ❌ Flask NÃO instalado")
        return False

    try:
        from flask_cors import CORS
        print("  ✅ Flask-CORS instalado")
    except:
        print("  ❌ Flask-CORS NÃO instalado")
        return False

    try:
        from app import app, load_transactions
        print("  ✅ app.py importado com sucesso")
    except Exception as e:
        print(f"  ❌ Erro ao importar app.py: {e}")
        return False

    try:
        from search_algorithms import SearchEngine
        print("  ✅ SearchEngine importado com sucesso")
    except Exception as e:
        print(f"  ❌ Erro ao importar SearchEngine: {e}")
        return False

    return True

def check_algorithms():
    """Verificar funcionamento dos algoritmos."""
    print("\n🔍 Testando Algoritmos...")
    sys.path.insert(0, "backend")

    try:
        with open("data/transactions.json", "r") as f:
            transactions = json.load(f)

        from search_algorithms import SearchEngine
        engine = SearchEngine(transactions)

        # Teste 1: Busca por categoria
        results = engine.search_with_filters(category="Alimentação")
        print(f"  ✅ Busca por categoria: {len(results)} resultados")

        # Teste 2: Busca por valor
        results = engine.search_with_filters(min_amount=100, max_amount=200)
        print(f"  ✅ Busca por valor: {len(results)} resultados")

        # Teste 3: Estatísticas
        stats = engine.get_statistics(transactions)
        print(f"  ✅ Cálculo de estatísticas: OK")

        return True
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False

def main():
    print("="*60)
    print("  🔍 VERIFICAÇÃO DO PROJETO SwiftPay")
    print("="*60)

    checks = [
        ("Estrutura de pastas", check_structure),
        ("Arquivo de dados", check_data),
        ("Dependências", check_imports),
        ("Algoritmos", check_algorithms),
    ]

    results = []
    for name, func in checks:
        try:
            results.append(func())
        except Exception as e:
            print(f"\n❌ Erro em {name}: {e}")
            results.append(False)

    print("\n" + "="*60)
    if all(results):
        print("  ✅ TUDO OK! Projeto pronto para rodar!")
        print("\n  Para iniciar:")
        print("  $ python3 run.py")
        print("\n  Depois acesse:")
        print("  http://localhost:5000")
        print("="*60)
        return 0
    else:
        print("  ❌ Existem problemas. Verifique acima!")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
