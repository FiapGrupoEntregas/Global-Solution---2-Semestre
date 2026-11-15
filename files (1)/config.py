"""Caminhos do projeto: código em src/, modelos em src/modelos/ e bases em data/ (estrutura do template FIAP)."""
from pathlib import Path

SRC = Path(__file__).resolve().parent
DATA = SRC.parent / "data"
CSV = DATA / "solicitacoes_sinteticas.csv"
MODELO = SRC / "modelos" / "modelo.joblib"
METRICAS = DATA / "metricas.json"
DB = DATA / "triasus.db"
SCHEMA = SRC / "schema.sql"
