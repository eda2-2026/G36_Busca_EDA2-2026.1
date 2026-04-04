"""Configurações da aplicação SwiftPay."""

from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TRANSACTIONS_FILE = DATA_DIR / "transactions.json"
FRONTEND_DIR = BASE_DIR / "frontend"


class Config:
    """Configuração base."""

    DEBUG = False
    TESTING = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    CORS_ORIGINS = "*"
    BASE_DIR = str(BASE_DIR)
    DATA_DIR = str(DATA_DIR)
    TRANSACTIONS_FILE = str(TRANSACTIONS_FILE)
    FRONTEND_DIR = str(FRONTEND_DIR)


class DevelopmentConfig(Config):
    """Configuração para desenvolvimento."""

    DEBUG = True


class TestingConfig(Config):
    """Configuração para testes."""

    TESTING = True


class ProductionConfig(Config):
    """Configuração para produção."""

    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
