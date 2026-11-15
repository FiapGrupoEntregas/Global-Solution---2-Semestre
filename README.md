# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/">
  <img src="../../assets/logo-fiap.png" 
       alt="FIAP - Faculdade de Informática e Administração Paulista" 
       width="40%">
</a>
</p>

<br>

# TriaSUS: regulação inteligente por risco e equidade no SUS (Global Solution 2026.2 - CitizenTech)

## Sala
· Turma: 1TIAOB

## 👨‍🎓 Integrantes: 
- <a href="[PREENCHER: link LinkedIn ou GitHub]">Jonattas Felipe</a> - RM572692
- <a href="[PREENCHER: link LinkedIn ou GitHub]">Natanael Filho</a> - RM572474
- <a href="[PREENCHER: link LinkedIn ou GitHub]">Pedro Henrique</a> - RM571394
- <a href="[PREENCHER: link LinkedIn ou GitHub]">Andrews Oliveira</a> - RM572311

## 👩‍🏫 Professores:

### Tutor(a)
- <a href="[PREENCHER: link LinkedIn da tutora]">Sabrina</a>
  
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>

## 📜 Descrição

O **TriaSUS** é uma prova de conceito (POC) de apoio à decisão para centrais de regulação do SUS. Ele sugere a prioridade de risco de cada solicitação de consulta especializada, reordena a fila combinando risco, tempo de espera e um ajuste territorial transparente, e audita o desempenho do modelo por região, porte do município e sexo. **A IA apenas sugere; a decisão é do regulador humano.**

**Problema e público:** a espera média por especialista no SUS foi de 57 dias em 2024, com casos acima de 700 dias, e o Sudeste concentra 55,4% dos especialistas (dados do Ministério da Saúde divulgados pela imprensa; ver referências em `docs/`). A Portaria GM/MS 7.266/2025 manda priorizar por risco e por desigualdade regional, e o TriaSUS operacionaliza esses dois critérios. Beneficiam-se pacientes do SUS, médicos de UBS, reguladores e gestores.

**⚠️ Dados 100% sintéticos.** A base de 5.000 solicitações é gerada por `src/gerar_dados.py` (semente fixa). Só a espera média (~57 dias) é ancorada em dado público; sinais, rótulos e viés foram simulados. Sem validação clínica; **não usar com pacientes reais.**

**Abordagens aplicadas:** classificação supervisionada (Random Forest) e rede neural (MLP), banco relacional SQL (SQLite) com 4 consultas de gestão, visualização interativa (Streamlit/Plotly), auditoria de equidade por subgrupo e testes automatizados (pytest). O resumo por IA generativa existe como caminho opcional (`resumo_llm`) e **não foi testado**.

**Resultados medidos (dados sintéticos):** Random Forest com acurácia 0,53 e recall de alto risco 0,68; MLP com 0,62 e 0,68. Recall de alto risco por porte do município: grande 0,76, médio 0,77 e **pequeno 0,55**. 7 de 7 testes aprovados.

**ODS:** 3 (Saúde e bem-estar), 10 (Redução das desigualdades) e 9 (Indústria, inovação e infraestrutura).

**Limitações:** dados sintéticos; acurácia moderada (cerca de 32% dos casos de alto risco não reconhecidos); SQLite local de usuário único; sem autenticação e sem integração com Sisreg. Conteúdos do curso não utilizados: AWS, R e C++/ESP32 no Wokwi. Linguagens usadas: Python e SQL.

## 📁 Estrutura de pastas 

Abaixo encontra-se a descrição da organização da raiz do projeto e a finalidade de cada diretório e arquivo:

* **`data/`** Armazena as bases do projeto: a base sintética de solicitações (`solicitacoes_sinteticas.csv`), o banco SQLite (`triasus.db`) e as métricas do modelo (`metricas.json`). Todos são regenerados pelos scripts.

* **`docs/`** Centraliza a documentação: o PDF da entrega (`GS2026_TriaSUS_Entrega.pdf`), o AI Project Document (`ai_project_document_fiap.md`), o roteiro do vídeo e as imagens usadas (`img/`).

* **`notebooks/`** Não utilizada nesta entrega (todo o desenvolvimento está em scripts Python).

* **`src/`** Todo o código-fonte: `gerar_dados.py`, `treinar_modelo.py`, `fila.py`, `resumo.py`, `banco.py`, `schema.sql`, `app.py` (painel Streamlit), `iniciar.py` (menu de execução), `config.py`, `tests/`, `requirements.txt` e o modelo treinado em `modelos/`.

* **`README.md`** Este arquivo.

## 📎 Links e Observações

### 🔗 Links do Projeto

* **[Vídeo de entrega no YouTube (não listado)]([PREENCHER: link])** - demonstração da solução em até 5 minutos.

### 🧠 Decisões Técnicas

> Random Forest como modelo principal por ter recall de alto risco ligeiramente maior e ser mais explicável; MLP mantida para comparação. Região e porte **não** entram como variáveis do modelo (só na auditoria e no ajuste de fila), para evitar discriminação territorial implícita. O ajuste territorial é uma regra pública e parametrizável (`src/fila.py`), não aprendizado de máquina. SQLite foi escolhido por não exigir servidor na POC; em produção seria Oracle ou PostgreSQL. O critério de avaliação priorizado é o recall de alto risco, pois classificar um caso grave como leve é o erro mais custoso.

### 📢 Observações Gerais

* **Participação na Competição:** [ ] Sim, aceitamos participar / [ ] Não vamos participar. **[PREENCHER: marcar uma opção; se for Sim, o vídeo começa com o nome do grupo e a frase "QUERO CONCORRER"]**
* *Outras observações gerais:* o PDF em `docs/` traz a documentação completa, os resultados e o código em texto.

## 🔧 Como executar o código

Pré-requisitos: Python 3.10 ou superior (testado em Linux com Python 3).

```bash
cd 1TIAO/GLOBAL-SOLUTION-2/src
pip install -r requirements.txt
python gerar_dados.py        # gera data/solicitacoes_sinteticas.csv
python treinar_modelo.py     # treina, avalia e salva o modelo e data/metricas.json
python banco.py              # cria data/triasus.db e imprime as consultas SQL
python -m pytest -q tests    # 7 testes
streamlit run app.py         # abre o painel
```

**Sem digitar comandos:** rode `python iniciar.py` dentro de `src` e escolha o número da etapa em um menu. No painel, a aba "Nova solicitação" permite escolher as opções em listas, sem escrever texto.

Os arquivos de `data/` e `src/modelos/` já estão incluídos, então `streamlit run app.py` funciona direto; rodar os scripts na ordem reproduz tudo.

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/fiap-tutoria/FIAP-PORTFOLIO-AI">TEMPLATE - FIAP PORTFÓLIO AI</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
