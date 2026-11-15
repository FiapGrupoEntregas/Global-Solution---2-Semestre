# Roteiro do vídeo (até 5 min) – TriaSUS

> Cronometre antes de gravar: leia em voz normal; o total abaixo soma ~4m30s. Publique no YouTube como **"Não listado"** e cole o link no final do PDF.

**[0:00–0:15] Abertura (um integrante, olhando para a câmera)**
"Somos o grupo **[NOME DO GRUPO]**, turma **[TURMA]**: Jonattas, Natanael, Pedro e Andrews. **QUERO CONCORRER.**" *(dizer a frase só se forem concorrer ao pódio)*

**[0:15–0:55] Problema (Integrante 1)**
- Fila do SUS para especialista: espera média de 57 dias em 2024 (dados do Ministério da Saúde via LAI, noticiados pela imprensa); casos de mais de 700 dias.
- Sudeste concentra 55,4% dos especialistas.
- A Portaria 7.266/2025 manda priorizar por risco e por desigualdade regional. Nosso projeto operacionaliza isso.

**[0:55–1:25] Solução e público (Integrante 2)**
- TriaSUS: apoio à decisão do regulador. Sugere prioridade, reordena a fila e audita equidade.
- Público: pacientes de UBS, reguladores, gestores.
- Frase-chave: "A IA sugere; quem decide é o profissional" (Resolução CFM 2.454/2026).

**[1:25–2:00] Dados e integração entre disciplinas (Integrante 3)**
- Base **sintética** de 5.000 solicitações, espera média calibrada em 57 dias. Dizer claramente que não são dados reais.
- Disciplinas usadas: Python/pandas (dados), Streamlit/Plotly (visualização interativa), Random Forest e MLP (aprendizado supervisionado e redes neurais), ética e segurança (auditoria, sem região no modelo, pseudonimização para uso real).
- Dizer o que **não** foi feito: NoSQL, nuvem (AWS) e R. Citar o módulo ESP32/C++ no Wokwi **somente se o grupo executar a simulação**. SQL: banco SQLite com consultas (mostrar na aba "Consultas SQL").

**[2:00–3:45] Demonstração prática (Integrante 4, tela do app)**
1. Rodar `streamlit run app.py`.
2. Aba **Fila priorizada**: mostrar a lista; ligar/desligar "Aplicar ajuste territorial" e comentar que Norte+Nordeste vão de 47,2% para 53,8% das 500 primeiras posições.
3. Aba **Painel do gestor**: espera mediana por região.
4. Aba **Auditoria de equidade**: recall de alto risco 0,55 em municípios pequenos vs 0,76–0,77 nos demais. Explicar o motivo (menos sinais registrados).
5. Aba **Consultas SQL**: escolher "Alto risco aguardando mais de N dias", mexer no slider e mostrar o SQL e o resultado.
6. Aba **Nova solicitação**: no modo "Escolher opções", marcar sinais de alerta nas listas e clicar em "Sugerir prioridade"; mostrar também o modo "Texto livre" (colar o texto de exemplo e clicar em "Resumir e sugerir prioridade"). Se quiserem, mostrar antes o menu `python iniciar.py`.

**[3:45–4:15] Testes e limitações (Integrante 1 ou 2)**
- 11 testes automatizados aprovados (`pytest`).
- Random Forest: acurácia 0,53, recall de alto risco 0,68: ainda deixa passar cerca de 32% dos casos graves.
- Dados sintéticos, sem validação clínica, resumo por IA generativa não testado.

**[4:15–4:35] ODS e impacto (Integrante 3)**
- ODS 3, 10 e 9.
- Medir: mediana de dias por faixa de risco, razão de espera entre regiões, diferença de recall entre subgrupos.

**[4:35–4:50] Encerramento (todos)**
"Obrigado. Repositório e PDF com todo o código e os resultados."

## Checklist antes de gravar
- [ ] Todos os números do roteiro batem com o PDF.
- [ ] O app roda sem erro na máquina de quem vai gravar.
- [ ] Vídeo com no máximo 5 minutos.
- [ ] Publicado como "Não listado" e link colado no PDF.
