<img src="../../../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=30% height=30%>

# AI Project Document - Global Solution 2026.2 (CitizenTech) - FIAP

## TriaSUS: regulação inteligente por risco e equidade no SUS

**Nome do grupo:** [PREENCHER: nome do grupo] · **Turma:** 1TIAOB

#### Integrantes
- Jonattas Felipe - RM572692
- Natanael Filho - RM572474
- Pedro Henrique - RM571394
- Andrews Oliveira - RM572311

## Sumário

[1. Introdução](#c1)

[2. Visão Geral do Projeto](#c2)

[3. Desenvolvimento do Projeto](#c3)

[4. Resultados e Avaliações](#c4)

[5. Conclusões e Trabalhos Futuros](#c5)

[6. Referências](#c6)

[Anexos](#c7)

<br>

> **Aviso sobre os dados:** todos os dados deste projeto são **sintéticos**, gerados pela equipe. Nenhum resultado representa eficácia em pacientes reais. O PDF completo da entrega está em `docs/GS2026_TriaSUS_Entrega.pdf`.

# <a name="c1"></a>1. Introdução

## 1.1. Escopo do Projeto

### 1.1.1. Contexto da Inteligência Artificial

A Inteligência Artificial aplicada à saúde pública atua em triagem e priorização de pacientes, previsão de demanda hospitalar, gestão de filas e apoio administrativo. No Brasil, o tema é regulado por normas em evolução: a Resolução CFM nº 2.454/2026 classifica sistemas de IA na medicina por nível de risco e exige supervisão humana [7], e o PL 2.338/2023 (marco legal da IA) seguia em tramitação na Câmara em outubro de 2026 [8]. A abrangência pretendida é nacional, pois a regulação do acesso a especialistas existe em todos os estados, mas esta entrega é uma prova de conceito (POC) sem uso real.

O problema de saúde que motiva o projeto é a espera por atenção especializada no SUS. A espera média por consulta com especialista foi de 57 dias em 2024, acima dos 50 dias de 2020, com casos como 721 dias em genética médica no Mato Grosso [1]. O Sisreg registrou 52 dias de espera média por procedimento em 2024 e 344 dias, em média, para cirurgia de quadril [2]. O Sudeste concentra 55,4% dos especialistas [3]. Esses números vêm de reportagens que citam dados oficiais e devem ser conferidos nas fontes primárias.

### 1.1.2. Descrição da Solução Desenvolvida

O **TriaSUS** é um apoio à decisão para centrais de regulação. Ele (1) sugere a prioridade de risco de cada solicitação em 4 níveis, (2) reordena a fila combinando risco, tempo de espera e um ajuste territorial transparente, (3) armazena os dados em um banco relacional com consultas de gestão e (4) audita o desempenho do modelo por região, porte do município e sexo. A solução operacionaliza os dois critérios da Portaria GM/MS nº 7.266/2025: risco clínico e desigualdades regionais [4]. **A IA apenas sugere; a decisão é do regulador humano.**

# <a name="c2"></a>2. Visão Geral do Projeto

## 2.1. Objetivos do Projeto

- Demonstrar, com uma POC funcional, a priorização de solicitações de regulação por risco e equidade territorial.
- Medir o desempenho do modelo com foco em **recall de alto risco**, e não só em acurácia.
- Expor desigualdades de desempenho entre subgrupos por meio de auditoria.
- Conectar a solução aos ODS 3 (Saúde e bem-estar), 10 (Redução das desigualdades) e 9 (Indústria, inovação e infraestrutura), com indicadores de impacto.

## 2.2. Público-Alvo

Pacientes do SUS que aguardam atenção especializada (em especial os de municípios pequenos e regiões com menos especialistas), médicos generalistas de UBS e UPAs que registram solicitações, reguladores que ordenam a fila e gestores municipais e estaduais que decidem sobre oferta de serviços.

## 2.3. Metodologia

1. **Observação do cenário:** levantamento de dados e normas em fontes públicas (seção 6).
2. **Escolha do recorte:** priorização da fila de regulação, por ter dado existente, critério já definido em portaria e medição clara.
3. **Dados:** geração de base sintética de 5.000 solicitações com semente fixa, com espera média calibrada em 57 dias [1]; viés de registro simulado para municípios pequenos.
4. **Prototipação:** modelo de classificação, escore de fila, banco SQL e aplicação Streamlit.
5. **Validação:** métricas por modelo e por subgrupo, 11 testes automatizados e teste do app.
6. **Impacto:** indicadores e metodologia de avaliação propostos para um piloto real (Anexos).

Limitação metodológica: não houve conversa com usuários reais (pacientes ou reguladores).

# <a name="c3"></a>3. Desenvolvimento do Projeto

## 3.1. Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python, pandas, NumPy | geração e tratamento de dados |
| scikit-learn | Random Forest, MLP, pré-processamento e métricas |
| SQLite e SQL | modelo relacional (`regiao`, `solicitacao`) e 4 consultas de gestão |
| Streamlit e Plotly | aplicação interativa e gráficos |
| pytest | testes automatizados |
| C++, ESP32 e Wokwi | quiosque de triagem offline simulado (`src/esp32`); a lógica foi testada no computador, a simulação no Wokwi **ainda deve ser executada e registrada pelo grupo** |
| IA generativa (opcional) | resumo estruturado de solicitação em `resumo_llm`; **não testada** |

## 3.2. Modelagem e Algoritmos

- **Random Forest** (300 árvores, `class_weight="balanced"`): modelo principal. Foi mantido por ter recall de alto risco ligeiramente maior e ser mais fácil de explicar.
- **Rede neural MLP** (camadas 32 e 16): comparação com o baseline.
- **Variáveis de entrada:** idade, número de sinais de alerta, comorbidades, sexo e especialidade. **Região e porte não entram no modelo**; são usados só na auditoria e no ajuste de fila, para evitar discriminação territorial implícita.
- **Escore de fila** (`src/fila.py`): `peso do risco + 0,3 x dias de espera + ajuste por região e porte`. É uma regra pública e parametrizável, **não** aprendizado de máquina.
- **Resumo da solicitação** (`src/resumo.py`): extração por regras; campos ausentes viram "não informado", sem inventar informação.

## 3.3. Treinamento e Teste

- **Conjunto de dados:** 5.000 solicitações sintéticas (`data/solicitacoes_sinteticas.csv`); separação de 75% para treino e 25% para teste, estratificada pela prioridade.
- **Pré-processamento:** padronização das variáveis numéricas e one-hot das categóricas.
- **Métricas:** acurácia, recall de alto risco (níveis 2 e 3), matriz de confusão e recall por subgrupo.

| Modelo | Acurácia | Recall de alto risco |
|---|---|---|
| Random Forest (em uso) | 0,53 | 0,68 |
| MLP (32, 16) | 0,62 | 0,68 |

**Testes automatizados:** 11 de 11 aprovados (`cd src && python -m pytest -q tests`), cobrindo o escore de fila, o resumo estruturado, a integridade do banco, as consultas SQL e a regra do módulo ESP32 (incluindo C++ compilado com g++ igual ao Python nas 5.000 linhas). O app Streamlit foi executado em teste automatizado, sem exceções nas 5 abas.

# <a name="c4"></a>4. Resultados e Avaliações

## 4.1. Análise dos Resultados

**Desempenho:** o modelo reconhece cerca de 68% dos casos de alto risco; ou seja, cerca de 32% não são reconhecidos. Isso seria inaceitável sem revisão humana. Como a prioridade sintética foi gerada por regra com ruído, a acurácia não prevê o desempenho com dados reais.

![Matriz de confusão](img/fig3_matriz_confusao.png)

**Equidade:** o recall de alto risco é de 0,55 em municípios pequenos, contra 0,76 (grandes) e 0,77 (médios). A diferença decorre do viés simulado: municípios pequenos registram menos sinais de alerta, e o modelo depende deles. A resposta de projeto é tratar a ausência de campos como gatilho de revisão humana, e nunca como baixa prioridade.

![Recall por subgrupo](img/fig2_recall_subgrupos.png)

**Fila:** entre as 500 primeiras posições, a participação de Norte e Nordeste sobe de 47,2% (sem ajuste) para 53,8% (com ajuste), contra 36,1% na base completa; a proporção de alto risco previsto nessas posições fica praticamente igual (96,8% contra 96,4%). O efeito é modesto por construção, e os parâmetros do ajuste devem ser definidos por gestores.

![Ajuste territorial](img/fig4_ajuste_territorial.png)

**Espera por região (dados sintéticos):**

![Espera por região](img/fig1_espera_regiao.png)

**SQL:** na base sintética, a espera média é praticamente a mesma em todas as prioridades (59,3 dias para urgentes e 59,8 para baixa), porque a espera foi simulada sem relação com o risco. Isso é uma construção da simulação, não um achado real.

## 4.2. Feedback dos Usuários

Não houve avaliação com usuários reais (pacientes, médicos ou reguladores) nesta entrega. Isso é uma limitação. Para um piloto, propõe-se validação retrospectiva, modo sombra (o modelo sugere sem influenciar a decisão) e estudo com implantação escalonada por região de saúde.

# <a name="c5"></a>5. Conclusões e Trabalhos Futuros

**Pontos fortes:** fluxo completo (dados, modelo, fila, banco, painel e auditoria) funcionando e testado; critério de avaliação alinhado ao risco clínico (recall); auditoria que revelou uma desigualdade escondida pela acurácia global; transparência sobre o que é sintético.

**Pontos a melhorar:** módulo ESP32 com regra simples (recall de alto risco 0,58) e sem envio de dados; dados sintéticos; acurácia moderada; recall de alto risco de 0,68; ajuste territorial com parâmetros arbitrários; resumo por IA generativa não testado; banco SQLite de usuário único, sem autenticação, sem integração com Sisreg e sem nuvem.

**Plano de ações:**
1. Obter dados reais anonimizados, com acordo institucional e parecer de proteção de dados (LGPD).
2. Rotular uma amostra com reguladores experientes e validar clinicamente.
3. Migrar o banco para um SGBD multiusuário (Oracle ou PostgreSQL) e incluir autenticação e trilha de auditoria.
4. Testar o resumo por IA generativa com avaliação de fidelidade.
5. Calibrar o ajuste territorial com gestores e medir seu efeito num piloto escalonado.

# <a name="c6"></a>6. Referências

1. Valor Saúde. A crise das filas no SUS (dados do Ministério da Saúde via LAI). https://valoresaude.substack.com/p/a-crise-das-filas-no-sus-uma-espera
2. Folha de Pernambuco, a partir de levantamento de O Globo sobre dados do Sisreg. https://www.folhape.com.br/noticias/fila-do-sus-para-cirurgia-no-quadril-feita-por-lula-leva-344-dias-em/398379/
3. Le Monde Diplomatique Brasil. Agora Tem Especialistas. https://diplomatique.org.br/agora-tem-especialistas-sus/
4. Ministério da Saúde. Portaria GM/MS nº 7.266, de 07/11/2025. https://www.ghc.com.br/files/20251107_Portaria_GM_MS_7266.pdf
5. Brasil de Fato (18/09/2026). Filas por consultas e exames no SUS em MG. https://www.brasildefato.com.br/2026/09/18/falta-de-articulacao-do-governo-estadual-expoe-filas-por-consultas-e-exames-no-sus-em-mg/
6. Futuro da Saúde. Ministro é cobrado por filas do SUS na Câmara. https://futurodasaude.com.br/?p=46698
7. Conselho Federal de Medicina. Resolução CFM nº 2.454/2026. https://portal.cfm.org.br/noticias/cfm-normatiza-uso-da-ia-na-medicina
8. Marco legal da IA: situação do PL 2.338/2023 (out/2026). https://www.globalsuitesolutions.com/pt/?p=117764

# <a name="c7"></a>Anexos

## Anexo A. Alinhamento com os ODS e indicadores de impacto

| ODS | Contribuição | Como medir |
|---|---|---|
| 3 - Saúde e bem-estar | prioriza quem tem maior gravidade | mediana de dias na fila por faixa de risco; % de alto risco atendido no prazo-meta |
| 10 - Redução das desigualdades | ajuste territorial e auditoria de subgrupos | razão de espera entre regiões mais e menos assistidas; diferença de recall entre subgrupos |
| 9 - Indústria, inovação e infraestrutura | ferramenta digital para regulação | nº de unidades usando; tempo de registro por solicitação |

## Anexo B. Modelo relacional

Tabelas `regiao` (id_regiao, nome, ajuste_fila) e `solicitacao` (id_solicitacao, idade, sexo, id_regiao, porte, especialidade, n_sinais_alerta, comorbidades, dias_espera, prioridade_real, prioridade_prevista, texto_livre), com chave estrangeira, restrições CHECK e índices. Código completo em `src/schema.sql`.

## Anexo C. Segurança, privacidade e ética

- Nenhum dado pessoal é tratado: a base é sintética.
- Para uso real: dado de saúde é dado pessoal sensível (LGPD, Lei 13.709/2018); seriam necessários pseudonimização, minimização, relatório de impacto, controle de acesso por perfil e trilha de auditoria.
- Supervisão humana obrigatória e direito do paciente à informação sobre o uso de IA [7].

## Anexo D. Como executar

```bash
cd src
pip install -r requirements.txt
python gerar_dados.py
python treinar_modelo.py
python banco.py
python -m pytest -q tests
streamlit run app.py
```

Alternativa sem digitar os comandos: `python iniciar.py` (menu numerado). Na aba "Nova solicitação" do painel, a solicitação pode ser informada escolhendo opções em listas ou por texto livre.

## Anexo E. Documentos complementares

- PDF da entrega: `docs/GS2026_TriaSUS_Entrega.pdf`
- Roteiro do vídeo: `docs/GS2026_Roteiro_Video.md`
- Vídeo demonstrativo (YouTube, não listado): [PREENCHER: link]
