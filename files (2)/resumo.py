"""Resumo estruturado da solicitação. Nunca inventa campo: o que não está no texto vira 'não informado'."""
import os
import re

SINAIS = ["perda de peso", "sangramento", "dor intensa", "déficit neurológico", "falta de ar"]


def resumo_regras(texto: str) -> dict:
    idade = re.search(r"(\d{1,2}) anos", texto)
    esp = re.search(r"encaminhado para ([\wÀ-ú]+)", texto)
    com = re.search(r"(\d) comorbidade", texto)
    return {
        "idade": idade.group(1) if idade else "não informado",
        "especialidade": esp.group(1) if esp else "não informado",
        "sinais_de_alerta": [s for s in SINAIS if s in texto] or "não informado",
        "comorbidades": com.group(1) if com else "não informado",
    }


def resumo_llm(texto: str) -> dict:  # NÃO TESTADO nesta POC: requer ANTHROPIC_API_KEY
    """Caminho opcional com IA generativa; cai para regras se não houver chave."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        return resumo_regras(texto)
    import json
    import anthropic
    c = anthropic.Anthropic()
    msg = c.messages.create(
        model="claude-sonnet-4-6", max_tokens=400,
        system=("Extraia JSON com idade, especialidade, sinais_de_alerta, comorbidades do texto. "
                "Use exatamente 'não informado' para o que não constar. Responda só JSON."),
        messages=[{"role": "user", "content": texto}])
    try:
        return json.loads(msg.content[0].text)
    except Exception:
        return resumo_regras(texto)
