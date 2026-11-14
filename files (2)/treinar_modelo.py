"""Treina classificador de prioridade, avalia recall de alto risco e desempenho por subgrupo."""
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config import CSV, METRICAS, MODELO

NUM = ["idade", "n_sinais_alerta", "comorbidades"]
CAT = ["sexo", "especialidade"]  # região/porte NÃO entram como feature: usados só na auditoria e no ajuste de fila
ALVO = "prioridade_real"


def pipe(modelo):
    pre = ColumnTransformer([("n", StandardScaler(), NUM), ("c", OneHotEncoder(handle_unknown="ignore"), CAT)])
    return Pipeline([("pre", pre), ("m", modelo)])


def main():
    df = pd.read_csv(CSV)
    tr, te = train_test_split(df, test_size=0.25, random_state=0, stratify=df[ALVO])
    modelos = {
        "random_forest": pipe(RandomForestClassifier(300, class_weight="balanced", random_state=0)),
        "mlp": pipe(MLPClassifier((32, 16), max_iter=600, random_state=0)),
    }
    res = {}
    for nome, p in modelos.items():
        p.fit(tr[NUM + CAT], tr[ALVO])
        pred = p.predict(te[NUM + CAT])
        alto = te[ALVO] >= 2
        res[nome] = {
            "acuracia": float((pred == te[ALVO]).mean()),
            "recall_alto_risco": float(recall_score(alto, pred >= 2)),
            "matriz_confusao": confusion_matrix(te[ALVO], pred).tolist(),
        }
        print(nome, {k: round(v, 3) for k, v in res[nome].items() if k != "matriz_confusao"})
    melhor = max(res, key=lambda k: res[k]["recall_alto_risco"])
    p = modelos[melhor]
    te = te.assign(prev=p.predict(te[NUM + CAT]))
    sub = {}
    for col in ["regiao", "porte", "sexo"]:
        sub[col] = {g: round(float(recall_score(d[ALVO] >= 2, d.prev >= 2)), 3) for g, d in te.groupby(col)}
    res.update(melhor=melhor, recall_por_subgrupo=sub)
    MODELO.parent.mkdir(exist_ok=True)
    joblib.dump(p, MODELO, compress=("xz", 3))
    json.dump(res, open(METRICAS, "w"), ensure_ascii=False, indent=2)
    print("melhor:", melhor, "\nrecall alto risco por subgrupo:", json.dumps(sub, ensure_ascii=False))


if __name__ == "__main__":
    main()
