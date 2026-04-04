# SwiftPay

Sistema web para auditoria e análise de transações financeiras com filtros por categoria, merchant, data e valor.

## Estrutura

- backend/ — API Flask e motor de busca
- frontend/ — dashboard web
- data/ — arquivo JSON com as transações
- scripts/ — utilitários para gerar dados

## Estrutura atual

- backend/app.py
- backend/config.py
- backend/search_algorithms.py
- frontend/index.html
- frontend/css/style.css
- frontend/js/main.js
- data/transactions.json

## Como executar

1. Entrar na pasta do projeto

```bash
cd SwiftPay
```

2. Gerar os dados, se necessário

```bash
python3 scripts/generate_data.py
```

3. Iniciar a aplicação

```bash
python3 backend/app.py
```

Depois, acessar:

- Dashboard: http://localhost:5000
- Health check: http://localhost:5000/api/health

## Endpoints

- GET /api/transactions
- GET /api/search
- GET /api/categories
- GET /api/merchants
- GET /api/statistics
- GET /api/health

## Filtros de busca

O endpoint /api/search aceita:

- category
- merchant
- start_date
- end_date
- min_amount
- max_amount

Exemplo:

```bash
curl "http://localhost:5000/api/search?category=Alimentação&min_amount=10&max_amount=100"
```

## Algoritmos

- Índice invertido para categoria e merchant
- Busca binária para intervalos de data e valor

## Testes

```bash
python3 teste_algoritmos.py
python3 test_project.py
```

## Observação

Os dados são fictícios e gerados automaticamente para fins de estudo.
