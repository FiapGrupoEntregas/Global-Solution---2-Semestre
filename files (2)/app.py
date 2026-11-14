"""TriaSUS - POC (dados sintéticos). Execute: streamlit run app.py"""
import json

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

from fila import AJUSTE_REGIAO, ROTULOS, escore, ordenar
from banco import CONSULTAS, consultar, criar_banco
from config import CSV, DB, METRICAS, MODELO
from resumo import SINAIS, resumo_llm
from treinar_modelo import CAT, NUM

st.set_page_config(page_title="TriaSUS (POC)", layout="wide")
st.title("TriaSUS: regulação por risco e equidade")
st.warning("POC com dados SINTÉTICOS. Não validada clinicamente. A IA apenas sugere; a decisão é do regulador humano.")


@st.cache_data
def carregar():
    return pd.read_csv(CSV)


@st.cache_resource
def modelo():
    return joblib.load(MODELO)


df = carregar()
m = modelo()
df["prioridade_prevista"] = m.predict(df[NUM + CAT])

aba1, aba2, aba3, aba4, aba5 = st.tabs(["Fila priorizada", "Painel do gestor", "Auditoria de equidade", "Nova solicitação", "Consultas SQL"])

with aba1:
    ajuste = st.toggle("Aplicar ajuste territorial", value=True)
    esp = st.multiselect("Especialidade", sorted(df.especialidade.unique()))
    f = ordenar(df, usar_ajuste=ajuste)
    if esp:
        f = f[f.especialidade.isin(esp)]
    f["prioridade"] = f.prioridade_prevista.map(ROTULOS)
    st.dataframe(f[["posicao", "id", "prioridade", "dias_espera", "regiao", "porte", "especialidade", "escore_fila"]].head(200),
                 width='stretch', hide_index=True)

with aba2:
    c1, c2, c3 = st.columns(3)
    c1.metric("Solicitações", f"{len(df):,}")
    c2.metric("Espera média (dias)", f"{df.dias_espera.mean():.0f}")
    c3.metric("Alto risco (previsto)", f"{(df.prioridade_prevista >= 2).mean():.0%}")
    por_reg = df.groupby("regiao", as_index=False).dias_espera.median()
    st.plotly_chart(px.bar(por_reg, x="regiao", y="dias_espera", title="Mediana de dias de espera por região (sintético)"),
                    width='stretch')
    alto = df[df.prioridade_prevista >= 2].groupby("regiao", as_index=False).dias_espera.median()
    st.plotly_chart(px.bar(alto, x="regiao", y="dias_espera", title="Mediana de espera, apenas alto risco"),
                    width='stretch')

with aba3:
    met = json.load(open(METRICAS))
    st.write(f"Modelo em uso: **{met['melhor']}** | recall de alto risco: **{met[met['melhor']]['recall_alto_risco']:.2f}**")
    for col, nome in [("regiao", "Região"), ("porte", "Porte do município"), ("sexo", "Sexo")]:
        d = pd.DataFrame(met["recall_por_subgrupo"][col].items(), columns=[nome, "recall alto risco"])
        st.plotly_chart(px.bar(d, x=nome, y="recall alto risco", range_y=[0, 1], title=f"Recall por {nome.lower()}"),
                        width='stretch')
    st.info("Municípios pequenos têm recall menor porque registram menos sinais de alerta. "
            "Ausência de dado deve acionar revisão humana, não baixa prioridade.")

with aba4:
    modo = st.radio("Como informar a solicitação?", ["Escolher opções", "Texto livre"], horizontal=True)
    n_sinais = com = idade = 0
    sexo, esp_n, regiao, porte, dias = "F", "Cardiologia", "Nordeste", "pequeno", 30
    pronto = False
    if modo == "Escolher opções":
        c1, c2, c3 = st.columns(3)
        idade = c1.slider("Idade", 0, 95, 60)
        sexo = c1.selectbox("Sexo", ["F", "M"])
        esp_n = c2.selectbox("Especialidade", sorted(df.especialidade.unique()))
        sinais = c2.multiselect("Sinais de alerta", SINAIS)
        com = c3.selectbox("Comorbidades crônicas", [0, 1, 2, 3])
        regiao = c3.selectbox("Região", list(AJUSTE_REGIAO))
        porte = c1.selectbox("Porte do município", ["pequeno", "medio", "grande"])
        dias = c2.slider("Dias já esperados", 0, 365, 30)
        n_sinais = len(sinais)
        pronto = st.button("Sugerir prioridade")
    else:
        txt = st.text_area("Texto livre da solicitação", "Paciente F, 63 anos, encaminhado para Cardiologia. Relata dor intensa, falta de ar. 2 comorbidade(s) crônica(s).")
        regiao = st.selectbox("Região", list(AJUSTE_REGIAO))
        porte = st.selectbox("Porte do município", ["pequeno", "medio", "grande"])
        dias = st.slider("Dias já esperados", 0, 365, 30)
        if st.button("Resumir e sugerir prioridade"):
            r = resumo_llm(txt)
            st.json(r)
            n_sinais = len(r["sinais_de_alerta"]) if isinstance(r["sinais_de_alerta"], list) else 0
            com = int(r["comorbidades"]) if str(r["comorbidades"]).isdigit() else 0
            idade = int(r["idade"]) if str(r["idade"]).isdigit() else 50
            esp_n = r["especialidade"] if r["especialidade"] != "não informado" else "Cardiologia"
            sexo = "F" if "F," in txt else "M"
            pronto = True
    if pronto:
        x = pd.DataFrame([{"idade": idade, "n_sinais_alerta": n_sinais, "comorbidades": com, "sexo": sexo, "especialidade": esp_n}])
        p = int(m.predict(x[NUM + CAT])[0])
        sc = escore(p, dias, regiao, porte)
        pos = int((ordenar(df)["escore_fila"] > sc).sum()) + 1
        st.success(f"Sugestão: {ROTULOS[p]} | escore de fila {sc} | entraria na posição {pos} de {len(df) + 1} (o regulador decide)")

with aba5:
    import os
    if not DB.exists():
        criar_banco()
    nome = st.selectbox("Consulta", list(CONSULTAS))
    dias = st.slider("Dias de espera (N)", 30, 180, 90) if ":dias" in CONSULTAS[nome] else 90
    st.code(CONSULTAS[nome].strip(), language="sql")
    st.dataframe(consultar(nome, dias), hide_index=True, width="stretch")
