import pandas as pd
from fila import escore, ordenar
from resumo import resumo_regras


def test_urgente_vence_baixa_mesmo_com_menos_espera():
    assert escore(3, 5, "Sul", "grande") > escore(0, 90, "Sul", "grande")


def test_ajuste_territorial_sobe_regiao_remota():
    assert escore(1, 30, "Norte", "pequeno") > escore(1, 30, "Sudeste", "grande")


def test_ordenar_decrescente():
    df = pd.DataFrame({"prioridade_prevista": [0, 3, 1], "dias_espera": [100, 1, 50],
                       "regiao": ["Sul"] * 3, "porte": ["grande"] * 3})
    assert ordenar(df).prioridade_prevista.tolist() == [3, 1, 0]


def test_resumo_nao_inventa():
    r = resumo_regras("Paciente M, 40 anos, encaminhado para Ortopedia.")
    assert r["sinais_de_alerta"] == "não informado" and r["comorbidades"] == "não informado"


def test_resumo_extrai_sinais():
    r = resumo_regras("Paciente F, 70 anos, encaminhado para Neurologia. Relata déficit neurológico. 2 comorbidade(s) crônica(s).")
    assert r["sinais_de_alerta"] == ["déficit neurológico"] and r["comorbidades"] == "2"


# ---------- testes do banco SQL ----------
import sqlite3

import banco


def test_banco_carga_e_integridade(tmp_path):
    db = str(tmp_path / "t.db")
    banco.criar_banco(db)
    con = sqlite3.connect(db)
    assert con.execute("SELECT COUNT(*) FROM solicitacao").fetchone()[0] == 5000
    assert con.execute("SELECT COUNT(*) FROM regiao").fetchone()[0] == 5
    orfas = con.execute("SELECT COUNT(*) FROM solicitacao s LEFT JOIN regiao r USING(id_regiao) WHERE r.id_regiao IS NULL").fetchone()[0]
    assert orfas == 0


def test_consulta_parametrizada_monotonica(tmp_path):
    db = str(tmp_path / "t.db")
    banco.criar_banco(db)
    q = "Alto risco aguardando mais de N dias, por região"
    a = banco.consultar(q, dias=30, db=db).casos_alto_risco_parados.sum()
    b = banco.consultar(q, dias=120, db=db).casos_alto_risco_parados.sum()
    assert a > b > 0
