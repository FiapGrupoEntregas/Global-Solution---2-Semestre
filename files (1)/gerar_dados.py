"""Gera base SINTÉTICA de solicitações de regulação (NÃO são dados reais de pacientes).

Parâmetros de espera ancorados em números públicos (média nacional ~57 dias, ref. S1 do documento).
O restante (sinais, rótulos, viés) é simulado para fins de demonstração.
"""
import numpy as np
import pandas as pd

from config import CSV, DATA

RNG = np.random.default_rng(42)
REGIOES = {"Norte": 1.45, "Nordeste": 1.25, "Centro-Oeste": 1.0, "Sudeste": 0.8, "Sul": 0.85}
ESPECIALIDADES = ["Cardiologia", "Oftalmologia", "Ortopedia", "Neurologia", "Oncologia", "Dermatologia"]
SINAIS = ["perda de peso", "sangramento", "dor intensa", "déficit neurológico", "falta de ar"]


def gerar(n: int = 5000) -> pd.DataFrame:
    regiao = RNG.choice(list(REGIOES), n, p=[.08, .27, .08, .42, .15])
    porte = RNG.choice(["pequeno", "medio", "grande"], n, p=[.35, .35, .30])
    idade = np.clip(RNG.normal(52, 20, n), 0, 95).astype(int)
    sexo = RNG.choice(["F", "M"], n)
    esp = RNG.choice(ESPECIALIDADES, n)
    n_sinais = RNG.choice([0, 1, 2, 3], n, p=[.5, .28, .15, .07])
    comorb = RNG.choice([0, 1, 2, 3], n, p=[.35, .35, .2, .1])

    # prioridade "verdadeira" (0 baixa, 1 média, 2 alta, 3 urgente)
    risco = 0.9 * n_sinais + 0.5 * comorb + 0.02 * (idade - 50) + (esp == "Oncologia") * 1.2 + RNG.normal(0, .6, n)
    prio = np.digitize(risco, [0.8, 1.9, 3.0])

    # espera: maior em regiões remotas e cidades pequenas; média global calibrada ~57 dias
    base = np.array([REGIOES[r] for r in regiao]) * np.where(porte == "pequeno", 1.3, 1.0)
    espera = RNG.lognormal(3.6, 0.8, n) * base
    espera = espera * 57 / espera.mean()

    # qualidade do registro: municípios pequenos descrevem menos sinais (viés realista a ser auditado)
    omite = (porte == "pequeno") & (RNG.random(n) < 0.35)
    sinais_reg = np.where(omite, 0, n_sinais)

    textos = []
    for i in range(n):
        ss = list(RNG.choice(SINAIS, n_sinais[i], replace=False)) if n_sinais[i] and not omite[i] else []
        t = f"Paciente {sexo[i]}, {idade[i]} anos, encaminhado para {esp[i]}."
        if ss:
            t += " Relata " + ", ".join(ss) + "."
        if comorb[i]:
            t += f" {comorb[i]} comorbidade(s) crônica(s)."
        textos.append(t)

    return pd.DataFrame({
        "id": range(1, n + 1), "idade": idade, "sexo": sexo, "regiao": regiao, "porte": porte,
        "especialidade": esp, "n_sinais_alerta": sinais_reg, "comorbidades": comorb,
        "dias_espera": espera.round().astype(int), "texto_livre": textos, "prioridade_real": prio,
    })


if __name__ == "__main__":
    df = gerar()
    DATA.mkdir(exist_ok=True)
    df.to_csv(CSV, index=False)
    print(df.shape, "| espera média:", round(df.dias_espera.mean(), 1), "dias")
    print(df.prioridade_real.value_counts().sort_index().to_dict())
