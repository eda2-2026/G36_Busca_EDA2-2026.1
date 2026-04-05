#!/usr/bin/env python3
"""
Script principal para executar o SwiftPay.
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import app, load_transactions

if __name__ == "__main__":
    # Carregar dados
    try:
        load_transactions()
    except FileNotFoundError:
        print("❌ Erro: Arquivo de transações não encontrado!")
        print("Execute primeiro: python scripts/generate_data.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao carregar transações: {e}")
        sys.exit(1)

    # Iniciar servidor
    print("\n🚀 SwiftPay iniciado com sucesso!")
    print("📍 Acesse http://localhost:5000")
    print("🔧 Pressione CTRL+C para parar\n")

    app.run(debug=True, host="0.0.0.0", port=5000)
