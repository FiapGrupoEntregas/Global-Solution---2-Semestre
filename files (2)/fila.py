"""Escore de fila: risco + tempo de espera + ajuste territorial (regra pública, não ML)."""
import pandas as pd

PESO_RISCO = {0: 0, 1: 30, 2: 70, 3: 120}
AJUSTE_REGIAO = {"Norte": 10, "Nordeste": 6, "Centro-Oeste": 3, "Sul": 0, "Sudeste": 0}
AJUSTE_PORTE = {"pequeno": 5, "medio": 2, "grande": 0}
ROTULOS = {0: "Baixa (azul)", 1: "Média (verde/amarelo)", 2: "Alta (laranja)", 3: "Urgente (vermelho)"}


def escore(prioridade: int, dias_espera: int, regiao: str, porte: str, usar_ajuste: bool = True) -> float:
    s = PESO_RISCO[int(prioridade)] + 0.3 * dias_espera
    if usar_ajuste:
        s += AJUSTE_REGIAO.get(regiao, 0) + AJUSTE_PORTE.get(porte, 0)
    return round(s, 2)


def ordenar(df: pd.DataFrame, col_prio: str = "prioridade_prevista", usar_ajuste: bool = True) -> pd.DataFrame:
    out = df.copy()
    out["escore_fila"] = [escore(p, d, r, po, usar_ajuste)
                          for p, d, r, po in zip(out[col_prio], out.dias_espera, out.regiao, out.porte)]
    out = out.sort_values("escore_fila", ascending=False).reset_index(drop=True)
    out["posicao"] = out.index + 1
    return out
