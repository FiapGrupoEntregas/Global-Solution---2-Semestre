"""Banco relacional SQLite do TriaSUS: criação, carga e consultas de gestão."""
import sqlite3

import joblib
import pandas as pd

from config import CSV, DB, MODELO, SCHEMA
from fila import AJUSTE_REGIAO
from treinar_modelo import CAT, NUM


def criar_banco(db=DB) -> None:
    df = pd.read_csv(CSV)
    df["prioridade_prevista"] = joblib.load(MODELO).predict(df[NUM + CAT])
    con = sqlite3.connect(db)
    con.executescript(open(SCHEMA).read())
    regs = {n: i + 1 for i, n in enumerate(sorted(AJUSTE_REGIAO))}
    con.executemany("INSERT INTO regiao VALUES (?,?,?)", [(i, n, AJUSTE_REGIAO[n]) for n, i in regs.items()])
    con.executemany(
        "INSERT INTO solicitacao VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        [(r.id, r.idade, r.sexo, regs[r.regiao], r.porte, r.especialidade, r.n_sinais_alerta, r.comorbidades,
          r.dias_espera, r.prioridade_real, r.prioridade_prevista, r.texto_livre) for r in df.itertuples()])
    con.commit()
    con.close()


CONSULTAS = {
    "Espera média por prioridade prevista": """
        SELECT prioridade_prevista AS prioridade, COUNT(*) AS solicitacoes, ROUND(AVG(dias_espera),1) AS espera_media_dias
        FROM solicitacao GROUP BY prioridade_prevista ORDER BY prioridade_prevista DESC""",
    "Alto risco aguardando mais de N dias, por região": """
        SELECT r.nome AS regiao, COUNT(*) AS casos_alto_risco_parados
        FROM solicitacao s JOIN regiao r ON r.id_regiao = s.id_regiao
        WHERE s.prioridade_prevista >= 2 AND s.dias_espera > :dias
        GROUP BY r.nome ORDER BY casos_alto_risco_parados DESC""",
    "Municípios pequenos: espera média por especialidade": """
        SELECT especialidade, COUNT(*) AS solicitacoes, ROUND(AVG(dias_espera),1) AS espera_media_dias
        FROM solicitacao WHERE porte = 'pequeno'
        GROUP BY especialidade ORDER BY espera_media_dias DESC""",
    "Divergência entre prioridade real e prevista (subestimados)": """
        SELECT r.nome AS regiao, COUNT(*) AS subestimados
        FROM solicitacao s JOIN regiao r ON r.id_regiao = s.id_regiao
        WHERE s.prioridade_real >= 2 AND s.prioridade_prevista < 2
        GROUP BY r.nome ORDER BY subestimados DESC""",
}


def consultar(nome: str, dias: int = 90, db=DB) -> pd.DataFrame:
    con = sqlite3.connect(db)
    try:
        return pd.read_sql_query(CONSULTAS[nome], con, params={"dias": dias} if ":dias" in CONSULTAS[nome] else None)
    finally:
        con.close()


if __name__ == "__main__":
    criar_banco()
    for n in CONSULTAS:
        print("\n##", n)
        print(consultar(n).to_string(index=False))
