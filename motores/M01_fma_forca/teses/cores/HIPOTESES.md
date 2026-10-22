# HIPOTESES — registro de hipóteses do motor econofísico (F = m·a·k) e das cores

> **Documento vivo.** O painel entre `<!-- AUTO:h_painel:INICIO -->
_Gerado em 2026-10-06 · pastas: 2024_26, 2026, CandlesHistoricos2026 · janela=20 · limiares 1.5σ/2.5σ_
_Veredito calculado pelo script a partir dos dados (regra de significância: \|t\| ≥ 3). Resumo: CONFIRMADA: 19 · INCONCLUSIVA: 5 · PARCIAL: 3 · NÃO SUPORTADA: 2 · REFUTADA: 1 · PENDENTE: 1. Replicação em WDO: 30 de 31 vereditos idênticos._

| id | grupo | hipótese | regra de decisão | evidência (WIN) | veredito | veredito WDO |
|:---|:---|:---|:---|:---|:---|:---|
| H01 | Modelo | k é cosmético: com limiares adaptativos o estado independe de k (F×k ⇒ mesmo z) | 0 divergências entre k=1 e k=100 | 5min: 0 de 55436; 15min: 0 de 23246 | **CONFIRMADA** | CONFIRMADA |
| H02 | Modelo | m e a são componentes distintos (não redundantes) | \|ρ de postos\| entre \|m\| e a < 0.30 | 5min: ρ = +0.12; 15min: ρ = +0.10 | **CONFIRMADA** | CONFIRMADA |
| H03 | Modelo | O esforço (a) produz deslocamento: corpo/ATR cresce com a (lei de impacto) | β > 0.25 e R² ≥ 0.80 (log-log, 20 faixas) | 5min: β = 0.68, R² = 0.94; 15min: β = 0.72, R² = 0.93 | **CONFIRMADA** | CONFIRMADA |
| H04 | Modelo | O cruzamento m×a prevê atividade futura melhor que m ou a isolados | expansão do range seguinte de F > a e > \|m\| (frequência igual) | 5min: F 1.18× · a 1.18× · \|m\| 1.07×; 15min: F 1.09× · a 1.10× · \|m\| 1.05× | **PARCIAL** | PARCIAL |
| H05 | Modelo | A cor do candle extremo carrega direção (retorno h1 alinhado ≠ 0) | \|t\| ≥ 3 com o mesmo sinal nos dois TFs | 5min: μ h1 = -4.2 pts (t = -2.3); 15min: μ h1 = +1.9 pts (t = +0.4) | **INCONCLUSIVA** | INCONCLUSIVA |
| H06 | Pareto→Bollinger | A regra 80/20 vale para \|F\|: os 20% maiores candles concentram ≥ 80% da energia Σ\|F\| | top 20% ≥ 80% (estrito) · 65–80% (aproximado) · < 65% refuta | 5min: 56%; 10min: 56%; 15min: 57%; 20min: 58%; 30min: 52%; 60min: 55% | **REFUTADA** | REFUTADA |
| H07 | Pareto→Bollinger | O limiar fixo 70 equivale ao percentil ~80 de \|F\| em todos os TFs (âncora Pareto) | P(\|F\|≥70) entre 16% e 24% em todos os TFs | 5min: 20.7%; 10min: 21.3%; 15min: 21.3%; 20min: 21.8%; 30min: 21.2%; 60min: 22.5% | **CONFIRMADA** | CONFIRMADA |
| H08 | Pareto→Bollinger | A cauda de \|F\| segue lei de potência (Pareto) e não exponencial | R² log-log > R² semilog na cauda P80–P99.5 | 5min: 0.999 vs 0.934; 10min: 0.978 vs 0.990; 15min: 0.965 vs 0.999; 20min: 0.956 vs 1.000; 30min: 0.964 vs 1.000; 60min: 0.976 vs 0.987 | **PARCIAL** | PARCIAL |
| H09 | Pareto→Bollinger | Com 70/85 fixos a hierarquia ignição < saturação se inverte (≥85 é mais comum que 70–85) | P(≥85) > P(70–85) em todos os TFs, na definição nova e na dos robôs | 5min: 14.9% vs 5.8% (robôs 14.3% vs 6.1%); 10min: 16.0% vs 5.4% (robôs 15.3% vs 5.5%); 15min: 16.6% vs 4.7% (robôs 15.9% vs 4.8%); 20min: 17.0% vs 4.8% (robôs 16.4% vs 4.8%); 30min: 15.2% vs 6.0% (robôs 14.9% vs 6.2%); 60min: 16.9% vs 5.6% (robôs 16.6% vs 5.7%) | **CONFIRMADA** | CONFIRMADA |
| H10 | Pareto→Bollinger | Com Bollinger a hierarquia é preservada (brilhante é mais raro que escuro) | brilhante < escuro em todos os TFs | 5min: 2.7% vs 9.3%; 10min: 3.5% vs 10.6%; 15min: 4.5% vs 9.7%; 20min: 5.5% vs 8.5%; 30min: 2.2% vs 10.8%; 60min: 2.5% vs 11.4% | **CONFIRMADA** | CONFIRMADA |
| H11 | Pareto→Bollinger | Bollinger desacopla a quantidade diária de cores do regime de volatilidade do dia (o limiar fixo não) | ρ(fixo, amplitude do dia) ≥ 0.15 e \|ρ(Bollinger, amplitude)\| < 0.10 nos dois TFs | 5min: ρ fixo +0.20 vs Bollinger +0.02; 15min: ρ fixo +0.34 vs Bollinger +0.04 | **CONFIRMADA** | NÃO SUPORTADA |
| H12 | Pareto→Bollinger | Bollinger distribui a cor ao longo do dia de forma mais uniforme que o limiar fixo | CV entre horas (9h–17h) menor que o do fixo nos dois TFs | 5min: CV fixo 0.68 vs Bollinger 0.53; 15min: CV fixo 1.01 vs Bollinger 1.14 | **INCONCLUSIVA** | INCONCLUSIVA |
| H13 | Pareto→Bollinger | Remover a sazonalidade do volume (a sazonal) elimina a concentração de cor na abertura | CV com a sazonal < 0.8 × CV canônico nos dois TFs | 5min: CV 0.53 → 0.08; 15min: CV 1.14 → 0.13 | **CONFIRMADA** | CONFIRMADA |
| H14 | Pareto→Bollinger | A cauda de F é mais pesada que a normal: 2.5σ ocorre bem mais que o previsto por um Bollinger gaussiano | medido ÷ normal ≥ 1.5 em 2.5σ | 5min: 2.2× (α de Hill = 2.11); 15min: 3.6× (α de Hill = 2.91) | **CONFIRMADA** | CONFIRMADA |
| H15 | Pareto→Bollinger | O candle atual dentro da janela de μ/σ mascara extremos (auto-inclusão) | colorido sobe ≥ 1 p.p. ao excluir o candle atual | 5min: 12.0% → 14.2%; 15min: 14.1% → 16.0% | **CONFIRMADA** | CONFIRMADA |
| H16 | Pareto→Bollinger | Em frequência igual, Bollinger e Pareto fixo preveem a atividade seguinte com a mesma qualidade (a migração é estrutural, não preditiva) | \|Δ expansão do range seguinte\| ≤ 0.03× nos dois TFs | 5min: Bollinger 1.18× vs Pareto equiparado 1.18×; 15min: Bollinger 1.10× vs Pareto equiparado 1.09× | **CONFIRMADA** | CONFIRMADA |
| H17 | Sinais | Cor persiste: candle colorido é seguido de candle colorido acima do esperado para a hora | lift ajustado por hora ≥ 1.30 (nos dois TFs = confirmada; em um = parcial) | 5min: lift = 1.59; 15min: lift = 1.11 | **PARCIAL** | PARCIAL |
| H18 | Sinais | Escuro = continuação (o preço segue na direção da cor — "manter posição") | μ h1 alinhado > 0 com t ≥ 3 nos dois TFs | 5min: μ h1 = -3.9 (t = -2.2); 15min: μ h1 = -2.7 (t = -0.4) | **INCONCLUSIVA** | INCONCLUSIVA |
| H19 | Sinais | Brilhante = exaustão (reversão à média após o clímax) | μ h1 e μ h3 alinhados < 0 com t ≤ −3 nos dois TFs | 5min: h1 -5.1 (t = -1.0); h3 -1.7 (t = -0.2); 15min: h1 +12.0 (t = +1.3); h3 +17.9 (t = +1.1) | **NÃO SUPORTADA** | NÃO SUPORTADA |
| H20 | Sinais | Brilhante antecipa expansão de volatilidade (alerta de atividade, não de direção) | range seguinte ≥ 1.10× a média da hora com t ≥ 3 nos dois TFs | 5min: 1.44× (t = +19.1); 15min: 1.15× (t = +8.3) | **CONFIRMADA** | CONFIRMADA |
| H21 | Sinais | Neutro = sem vantagem direcional (abstenção) | \|t\| < 3 em μ h1 nos dois TFs | 5min: μ h1 = -1.1 (t = -1.8); 15min: μ h1 = -0.3 (t = -0.2) | **CONFIRMADA** | CONFIRMADA |
| H22 | Operação | A cor é rara o bastante para saltar aos olhos (saliência visual) | nos TFs de foco: colorido ≤ 15% e brilhante ≤ 5% | 5min: 12.0% / 2.7%; 15min: 14.1% / 4.5% | **CONFIRMADA** | CONFIRMADA |
| H23 | Operação | A abertura (9h) concentra as cores acima do seu peso em candles | fração das cores em 9h ÷ fração dos candles em 9h ≥ 1.5 | 5min: 2.0×; 15min: 3.5× | **CONFIRMADA** | CONFIRMADA |
| H24 | Operação | A quantidade diária de cores não indica dia de tendência nem de alta volatilidade (orçamento de cor ~constante) | \|ρ\| < 0.15 entre coloridos/dia e (amplitude do dia; \|C−O\|/amplitude) nos dois TFs | 5min: ρ amplitude +0.02; ρ direcional +0.03; CV diário 0.20; 15min: ρ amplitude +0.04; ρ direcional -0.00; CV diário 0.32 | **CONFIRMADA** | CONFIRMADA |
| H25 | Próxima teoria | Clusters de cor similar formam áreas (faixas de preço) com comportamento próprio (suporte/resistência, retorno às bordas) | teste de retorno/rejeição nas bordas do cluster — ainda não executado | 5min: 19% dos clusters têm ≥ 2 candles; amplitude mediana 2.8 ATR; 15min: 24% dos clusters têm ≥ 2 candles; amplitude mediana 3.7 ATR | **PENDENTE** | PENDENTE |
| H26 | Janela física | Em uma janela fixa de 100 minutos, frequência e persistência de estados são comparáveis entre 5 min e 15 min | diferença de cor ≤ 5 p.p. e diferença de persistência ≤ 0.15; sem inferir direção, risco ou operação | 5min: 15.18% de candles coloridos; persistência 0.35; Δ cor 1.23 p.p.; Δ persistência 0.37; 15min: 16.41% de candles coloridos; persistência 0.72; Δ cor 1.23 p.p.; Δ persistência 0.37 | **INCONCLUSIVA** | INCONCLUSIVA |
| H30 | Distribuição de cores | Dias muito direcionais têm uma distribuição de cores diferente dos demais | |Δ hora da 1ª cor| > 0 ou |Δ brilho| > 0 com |t| ≥ 3, sem inferir direção | 5min: 1ª cor 9.03 h vs 9.03 h; brilho 2.7% vs 2.7%; t = -0.02, +0.07; 15min: 1ª cor 9.05 h vs 9.09 h; brilho 4.5% vs 4.5%; t = -1.57, -0.03 | **NÃO SUPORTADA** | NÃO SUPORTADA |
| H29 | Absorção | A absorção (a ≥ 2 e |m| < 0.3) tem atividade e persistência próprias | range/ATR ≥ 1.50× e |t_exp| ≥ 3; não inferir direção, entrada ou SL | 2020–2026: ver linha acima; split temporal 2024-06/2025-06: treino e holdout passam em 5min/15min; Welch ainda sem ajuste por pregão (ver anexo) | **CONFIRMADA** | CONFIRMADA |
| H31 | Áreas por cluster | O preço retorna às bordas dos clusters em até N candles mais que janelas aleatórias do mesmo horário e largura | P(retorno) > controle e |t| ≥ 3; rejeição e rompimento ficam para estudo posterior | 5min: 87.1% vs 95.0% (t = -8.28; n = 1206); 15min: 91.2% vs 94.6% (t = -3.32; n = 713) | **INCONCLUSIVA** | INCONCLUSIVA |
| H40 | Transições | A duração das transições de família é descrita por mediana e percentis, sem inferir causalidade ou direção | mediana ≤ 3 em ambos os TFs e P90 ≤ 25, com gaps de timestamp separados da contagem de neutros | 5min: mediana 3.00; P90 21.00; gaps 0.9%; 15min: mediana 1.00; P90 23.00; gaps 2.6% | **CONFIRMADA** | CONFIRMADA |
| H39 | Alarmes multi-TF | Alarms coincidentes em dois ou mais timeframes têm maior próximo range/retorno do que alarmes isolados | range/ATR e retorno médios maiores, com |t| ≥ 3; não usar contagem como prova de direção | 5min: 1.89 vs 1.29; retorno 39.49 vs -9.04; t = +14.53, +6.89; 15min: 1.89 vs 1.29; retorno 39.49 vs -9.04; t = +14.53, +6.89 | **CONFIRMADA** | CONFIRMADA |
<!-- AUTO:h_painel:FIM -->` é regravado por
> [validacao_econofisica.py](validacao_econofisica.py); fichas, backlog e decisões são manuais.
> Contexto e tabelas completas: [VALIDACAO_ECONOFISICA.md](VALIDACAO_ECONOFISICA.md). Última revisão manual: **2026-10-06**.

> **Leitura visual consolidada do motor:** [LEITURA_VISUAL_MOTOR.md](LEITURA_VISUAL_MOTOR.md) reúne a legenda dos estados, as combinações de cores e o status da hipótese de entrada no primeiro candle colorido.

## 1. Como usar

- Cada hipótese tem **id estável** (H01…), enunciado e **regra de decisão declarada antes do teste**; o veredito é calculado pelo script (função `hipoteses()`), nunca à mão.
- **Vereditos:** `CONFIRMADA` (regra satisfeita em todos os TFs/ativos testados) · `PARCIAL` (satisfeita em parte) · `INCONCLUSIVA` (2 ≤ \|t\| < 3 ou evidência mista) ·
  `NÃO SUPORTADA` (sem evidência) · `REFUTADA` (evidência clara do contrário) · `PENDENTE` (teste ainda não existe).
- **Regra de significância** para hipóteses direcionais: \|t\| ≥ 3 (há dezenas de testes; \|t\| ≈ 2 aparece por acaso). Para as demais, o limiar está escrito na própria regra.
- **Ciclo:** nova hipótese → implementar teste em `hipoteses()` → rodar o script → registrar a decisão na §4. Ao mudar uma regra, **crie um novo id**; não reescreva o histórico.
- **Robustez cross-ativo:** a coluna "veredito WDO" repete o teste no WDO (mesmas pastas, mesmos TFs).
- **Suficiência dos dados:** antes de um veredito, a amostra precisa ter quantidade suficiente, cobertura temporal representativa, qualidade dos timestamps/variáveis, definição clara do evento, controle comparável e um conjunto de observações fora da amostra para validação. Se algum desses itens falhar, registrar **PENDENTE** ou **INCONCLUSIVO POR DADOS**, não atribuir veredito.
- **Não usar dados de teste para criar a hipótese:** o conjunto de validação externo deve ser separado da seleção usada para definir a regra, os parâmetros e o veredito inicial.

## 2. Painel (veredito automático)

<!-- AUTO:h_painel:INICIO -->
_Gerado em 2026-10-06 · pastas: 2024_26, 2026, CandlesHistoricos2026 · janela=20 · limiares 1.5σ/2.5σ_
_Veredito calculado pelo script a partir dos dados (regra de significância: \|t\| ≥ 3). Resumo: CONFIRMADA: 19 · INCONCLUSIVA: 5 · PARCIAL: 3 · NÃO SUPORTADA: 2 · REFUTADA: 1 · PENDENTE: 1. Replicação em WDO: 30 de 31 vereditos idênticos._

| id | grupo | hipótese | regra de decisão | evidência (WIN) | veredito | veredito WDO |
|:---|:---|:---|:---|:---|:---|:---|
| H01 | Modelo | k é cosmético: com limiares adaptativos o estado independe de k (F×k ⇒ mesmo z) | 0 divergências entre k=1 e k=100 | 5min: 0 de 55436; 15min: 0 de 23246 | **CONFIRMADA** | CONFIRMADA |
| H02 | Modelo | m e a são componentes distintos (não redundantes) | \|ρ de postos\| entre \|m\| e a < 0.30 | 5min: ρ = +0.12; 15min: ρ = +0.10 | **CONFIRMADA** | CONFIRMADA |
| H03 | Modelo | O esforço (a) produz deslocamento: corpo/ATR cresce com a (lei de impacto) | β > 0.25 e R² ≥ 0.80 (log-log, 20 faixas) | 5min: β = 0.68, R² = 0.94; 15min: β = 0.72, R² = 0.93 | **CONFIRMADA** | CONFIRMADA |
| H04 | Modelo | O cruzamento m×a prevê atividade futura melhor que m ou a isolados | expansão do range seguinte de F > a e > \|m\| (frequência igual) | 5min: F 1.18× · a 1.18× · \|m\| 1.07×; 15min: F 1.09× · a 1.10× · \|m\| 1.05× | **PARCIAL** | PARCIAL |
| H05 | Modelo | A cor do candle extremo carrega direção (retorno h1 alinhado ≠ 0) | \|t\| ≥ 3 com o mesmo sinal nos dois TFs | 5min: μ h1 = -4.2 pts (t = -2.3); 15min: μ h1 = +1.9 pts (t = +0.4) | **INCONCLUSIVA** | INCONCLUSIVA |
| H06 | Pareto→Bollinger | A regra 80/20 vale para \|F\|: os 20% maiores candles concentram ≥ 80% da energia Σ\|F\| | top 20% ≥ 80% (estrito) · 65–80% (aproximado) · < 65% refuta | 5min: 56%; 10min: 56%; 15min: 57%; 20min: 58%; 30min: 52%; 60min: 55% | **REFUTADA** | REFUTADA |
| H07 | Pareto→Bollinger | O limiar fixo 70 equivale ao percentil ~80 de \|F\| em todos os TFs (âncora Pareto) | P(\|F\|≥70) entre 16% e 24% em todos os TFs | 5min: 20.7%; 10min: 21.3%; 15min: 21.3%; 20min: 21.8%; 30min: 21.2%; 60min: 22.5% | **CONFIRMADA** | CONFIRMADA |
| H08 | Pareto→Bollinger | A cauda de \|F\| segue lei de potência (Pareto) e não exponencial | R² log-log > R² semilog na cauda P80–P99.5 | 5min: 0.999 vs 0.934; 10min: 0.978 vs 0.990; 15min: 0.965 vs 0.999; 20min: 0.956 vs 1.000; 30min: 0.964 vs 1.000; 60min: 0.976 vs 0.987 | **PARCIAL** | PARCIAL |
| H09 | Pareto→Bollinger | Com 70/85 fixos a hierarquia ignição < saturação se inverte (≥85 é mais comum que 70–85) | P(≥85) > P(70–85) em todos os TFs, na definição nova e na dos robôs | 5min: 14.9% vs 5.8% (robôs 14.3% vs 6.1%); 10min: 16.0% vs 5.4% (robôs 15.3% vs 5.5%); 15min: 16.6% vs 4.7% (robôs 15.9% vs 4.8%); 20min: 17.0% vs 4.8% (robôs 16.4% vs 4.8%); 30min: 15.2% vs 6.0% (robôs 14.9% vs 6.2%); 60min: 16.9% vs 5.6% (robôs 16.6% vs 5.7%) | **CONFIRMADA** | CONFIRMADA |
| H10 | Pareto→Bollinger | Com Bollinger a hierarquia é preservada (brilhante é mais raro que escuro) | brilhante < escuro em todos os TFs | 5min: 2.7% vs 9.3%; 10min: 3.5% vs 10.6%; 15min: 4.5% vs 9.7%; 20min: 5.5% vs 8.5%; 30min: 2.2% vs 10.8%; 60min: 2.5% vs 11.4% | **CONFIRMADA** | CONFIRMADA |
| H11 | Pareto→Bollinger | Bollinger desacopla a quantidade diária de cores do regime de volatilidade do dia (o limiar fixo não) | ρ(fixo, amplitude do dia) ≥ 0.15 e \|ρ(Bollinger, amplitude)\| < 0.10 nos dois TFs | 5min: ρ fixo +0.20 vs Bollinger +0.02; 15min: ρ fixo +0.34 vs Bollinger +0.04 | **CONFIRMADA** | NÃO SUPORTADA |
| H12 | Pareto→Bollinger | Bollinger distribui a cor ao longo do dia de forma mais uniforme que o limiar fixo | CV entre horas (9h–17h) menor que o do fixo nos dois TFs | 5min: CV fixo 0.68 vs Bollinger 0.53; 15min: CV fixo 1.01 vs Bollinger 1.14 | **INCONCLUSIVA** | INCONCLUSIVA |
| H13 | Pareto→Bollinger | Remover a sazonalidade do volume (a sazonal) elimina a concentração de cor na abertura | CV com a sazonal < 0.8 × CV canônico nos dois TFs | 5min: CV 0.53 → 0.08; 15min: CV 1.14 → 0.13 | **CONFIRMADA** | CONFIRMADA |
| H14 | Pareto→Bollinger | A cauda de F é mais pesada que a normal: 2.5σ ocorre bem mais que o previsto por um Bollinger gaussiano | medido ÷ normal ≥ 1.5 em 2.5σ | 5min: 2.2× (α de Hill = 2.11); 15min: 3.6× (α de Hill = 2.91) | **CONFIRMADA** | CONFIRMADA |
| H15 | Pareto→Bollinger | O candle atual dentro da janela de μ/σ mascara extremos (auto-inclusão) | colorido sobe ≥ 1 p.p. ao excluir o candle atual | 5min: 12.0% → 14.2%; 15min: 14.1% → 16.0% | **CONFIRMADA** | CONFIRMADA |
| H16 | Pareto→Bollinger | Em frequência igual, Bollinger e Pareto fixo preveem a atividade seguinte com a mesma qualidade (a migração é estrutural, não preditiva) | \|Δ expansão do range seguinte\| ≤ 0.03× nos dois TFs | 5min: Bollinger 1.18× vs Pareto equiparado 1.18×; 15min: Bollinger 1.10× vs Pareto equiparado 1.09× | **CONFIRMADA** | CONFIRMADA |
| H17 | Sinais | Cor persiste: candle colorido é seguido de candle colorido acima do esperado para a hora | lift ajustado por hora ≥ 1.30 (nos dois TFs = confirmada; em um = parcial) | 5min: lift = 1.59; 15min: lift = 1.11 | **PARCIAL** | PARCIAL |
| H18 | Sinais | Escuro = continuação (o preço segue na direção da cor — "manter posição") | μ h1 alinhado > 0 com t ≥ 3 nos dois TFs | 5min: μ h1 = -3.9 (t = -2.2); 15min: μ h1 = -2.7 (t = -0.4) | **INCONCLUSIVA** | INCONCLUSIVA |
| H19 | Sinais | Brilhante = exaustão (reversão à média após o clímax) | μ h1 e μ h3 alinhados < 0 com t ≤ −3 nos dois TFs | 5min: h1 -5.1 (t = -1.0); h3 -1.7 (t = -0.2); 15min: h1 +12.0 (t = +1.3); h3 +17.9 (t = +1.1) | **NÃO SUPORTADA** | NÃO SUPORTADA |
| H20 | Sinais | Brilhante antecipa expansão de volatilidade (alerta de atividade, não de direção) | range seguinte ≥ 1.10× a média da hora com t ≥ 3 nos dois TFs | 5min: 1.44× (t = +19.1); 15min: 1.15× (t = +8.3) | **CONFIRMADA** | CONFIRMADA |
| H21 | Sinais | Neutro = sem vantagem direcional (abstenção) | \|t\| < 3 em μ h1 nos dois TFs | 5min: μ h1 = -1.1 (t = -1.8); 15min: μ h1 = -0.3 (t = -0.2) | **CONFIRMADA** | CONFIRMADA |
| H22 | Operação | A cor é rara o bastante para saltar aos olhos (saliência visual) | nos TFs de foco: colorido ≤ 15% e brilhante ≤ 5% | 5min: 12.0% / 2.7%; 15min: 14.1% / 4.5% | **CONFIRMADA** | CONFIRMADA |
| H23 | Operação | A abertura (9h) concentra as cores acima do seu peso em candles | fração das cores em 9h ÷ fração dos candles em 9h ≥ 1.5 | 5min: 2.0×; 15min: 3.5× | **CONFIRMADA** | CONFIRMADA |
| H24 | Operação | A quantidade diária de cores não indica dia de tendência nem de alta volatilidade (orçamento de cor ~constante) | \|ρ\| < 0.15 entre coloridos/dia e (amplitude do dia; \|C−O\|/amplitude) nos dois TFs | 5min: ρ amplitude +0.02; ρ direcional +0.03; CV diário 0.20; 15min: ρ amplitude +0.04; ρ direcional -0.00; CV diário 0.32 | **CONFIRMADA** | CONFIRMADA |
| H25 | Próxima teoria | Clusters de cor similar formam áreas (faixas de preço) com comportamento próprio (suporte/resistência, retorno às bordas) | teste de retorno/rejeição nas bordas do cluster — ainda não executado | 5min: 19% dos clusters têm ≥ 2 candles; amplitude mediana 2.8 ATR; 15min: 24% dos clusters têm ≥ 2 candles; amplitude mediana 3.7 ATR | **PENDENTE** | PENDENTE |
| H26 | Janela física | Em uma janela fixa de 100 minutos, frequência e persistência de estados são comparáveis entre 5 min e 15 min | diferença de cor ≤ 5 p.p. e diferença de persistência ≤ 0.15; sem inferir direção, risco ou operação | 5min: 15.18% de candles coloridos; persistência 0.35; Δ cor 1.23 p.p.; Δ persistência 0.37; 15min: 16.41% de candles coloridos; persistência 0.72; Δ cor 1.23 p.p.; Δ persistência 0.37 | **INCONCLUSIVA** | INCONCLUSIVA |
| H30 | Distribuição de cores | Dias muito direcionais têm uma distribuição de cores diferente dos demais | |Δ hora da 1ª cor| > 0 ou |Δ brilho| > 0 com |t| ≥ 3, sem inferir direção | 5min: 1ª cor 9.03 h vs 9.03 h; brilho 2.7% vs 2.7%; t = -0.02, +0.07; 15min: 1ª cor 9.05 h vs 9.09 h; brilho 4.5% vs 4.5%; t = -1.57, -0.03 | **NÃO SUPORTADA** | NÃO SUPORTADA |
| H29 | Absorção | A absorção (a ≥ 2 e |m| < 0.3) tem atividade e persistência próprias | range/ATR ≥ 1.50× e |t_exp| ≥ 3; não inferir direção, entrada ou SL | 5min: range 1.60× vs 1.03×; persistência 1.56; t = +20.14; 15min: range 1.71× vs 1.03×; persistência 1.67; t = +25.68 | **CONFIRMADA** | CONFIRMADA |
| H31 | Áreas por cluster | O preço retorna às bordas dos clusters em até N candles mais que janelas aleatórias do mesmo horário e largura | P(retorno) > controle e |t| ≥ 3; rejeição e rompimento ficam para estudo posterior | 5min: 87.1% vs 95.0% (t = -8.28; n = 1206); 15min: 91.2% vs 94.6% (t = -3.32; n = 713) | **INCONCLUSIVA** | INCONCLUSIVA |
| H40 | Transições | A duração das transições de família é descrita por mediana e percentis, sem inferir causalidade ou direção | mediana ≤ 3 em ambos os TFs e P90 ≤ 25, com gaps de timestamp separados da contagem de neutros | 5min: mediana 3.00; P90 21.00; gaps 0.9%; 15min: mediana 1.00; P90 23.00; gaps 2.6% | **CONFIRMADA** | CONFIRMADA |
| H39 | Alarmes multi-TF | Alarms coincidentes em dois ou mais timeframes têm maior próximo range/retorno do que alarmes isolados | range/ATR e retorno médios maiores, com |t| ≥ 3; não usar contagem como prova de direção | 5min: 1.89 vs 1.29; retorno 39.49 vs -9.04; t = +14.53, +6.89; 15min: 1.89 vs 1.29; retorno 39.49 vs -9.04; t = +14.53, +6.89 | **CONFIRMADA** | CONFIRMADA |
<!-- AUTO:h_painel:FIM -->

## 3. Fichas (origem, implicação, próximo passo)

| id | origem / racional | o que o veredito implica | próximo passo |
|:---|:---|:---|:---|
| H01 | fórmula F = m·a·100 do documento-base | com z-score a escala não importa; a única dependência real de k é o **clamp ±100** dos robôs | não limitar F ao usar limiares adaptativos |
| H02 | premissa "candle e volume são dimensões distintas" | manter os dois componentes; m não é redundante com a | — |
| H03 | analogia volume ↔ aceleração; lei de impacto de mercado | a é medida plausível de esforço (β ≈ 0.7, entre raiz quadrada e linear) | medir β por horário (abertura × almoço) |
| H04 | premissa "o produto isola falso rompimento (absorção)" | o filtro de absorção funciona (grade a × \|m\|), mas o produto não prevê atividade melhor que a | avaliar preditor combinado a × amplitude para alertas de risco |
| H05 | fundamentação das cores (anexo) | a cor não é gatilho direcional | testar direção condicionada ao contexto (tendência do TF maior) |
| H06 | "Pareto" como heurística inicial | o 80/20 de energia não vale; no texto da dissertação falar em **âncora de percentil**, não em "princípio de Pareto" | — |
| H07 | idem | 70 ≈ P79 em todos os TFs: o limiar fixo era um percentil disfarçado | se mantiver limiar fixo, defini-lo como percentil rolante |
| H08 | cauda de F | só o 5 min tem cauda de lei de potência (α ≈ 2.1): σ amostral é instável nesse TF | testar μ/σ robustos (mediana/MAD) |
| H09 | faixas 55/70/85 dos robôs | "forte" 70–85 é raro e "exaustão" ≥ 85 é comum; o clamp em ±100 empilha 10–13% dos candles no teto | não usar 85 como "saturação" |
| H10 | Bollinger 1.5σ/2.5σ | a hierarquia ignição < saturação é restaurada | — |
| H11 | argumento de não estacionariedade do documento-base | confirmado empiricamente: o limiar fixo acompanha o regime do dia, o adaptativo não | usar a tabela "por dia" como evidência na dissertação |
| H12 | uniformidade horária | não vem do tipo de limiar | ver H13 |
| H13 | baseline de volume com perfil intradiário | elimina a concentração na abertura | testar como definição canônica de `a` (backtest) |
| H14 | Bollinger gaussiano | 2.5σ/3σ são 2–8× mais frequentes que na normal | z robusto; revisar o rótulo "2.5σ = evento de cauda" |
| H15 | μ/σ com a janela incluindo o candle atual | mascara extremos e limita z a √19 | testar μ/σ sem o candle atual (leave-one-out) |
| H16 | migração Pareto → Bollinger | a migração é de legibilidade/estrutura, não de previsão | decidir a troca pelo critério operacional, não preditivo |
| H17 | persistência de atividade (volatility clustering) como base da ideia de "áreas de cor" | **5 min:** persistência clara (lift ajustado 1.59); **15 min:** persistência fraca e próxima do esperado (lift 1.11). A cor é mais confiável qualitativamente no 5 min, mas ainda não representa direção | construir áreas no 5 min; testar 10 min |
| H18 | anexo ("verde escuro = hold") | "manter posição" não tem apoio direcional | reescrever a narrativa para "ritmo acima do normal" |
| H19 | anexo ("vivo = exaustão/reversão") | sem reversão nem continuação detectáveis | reescrever para "alerta de volatilidade" (H20) |
| H20 | brilhante como alerta de atividade | o próximo candle é 1.44× (5 min) / 1.15× (15 min) maior | usar como gatilho de gestão de risco |
| H21 | "neutro = abstenção" | confirmado (sem edge) | — |
| H22 | teoria de percepção visual (pop-out) | cor rara (12–14%) → saliência | manter 1.5σ/2.5σ como convenção |
| H23 | volume na abertura | cor concentra na abertura | usar volume sazonal para mapa neutro ao horário |
| H24 | cor ≠ tendência | orçamento diário ≈ constante, independente da amplitude/direção do dia | não inferir tipo de dia pela quantidade de cor |
| H25 | próxima teoria | descrição das áreas candidatas; teste de comportamento ainda não executado | ver backlog H31 |
| H27 | σ robusto (MAD) com μ/σ sem o candle atual reduz o auto-mascaramento do brilhante | 5min: robusto gera 715 eventos vs 506 canônicos; lift robusto 1.27; expansão robusta 1.18× vs 1.70× canônica; 15min: robusto 36 vs 128; expansão 1.28× vs 1.36×; 10min e 20min também caem; em 30min/60min quase desaparece | **NÃO SUPORTADA**: a robusta não preserva a expansão do próximo range e praticamente desaparece em TFs maiores |
| H28 | O volume sazonal substitui o `a` canônico sem perder o alerta de volatilidade | 5min: expansão canônica = 1.2567×, sazonal = 1.2567×, dif = 0.00×, CV horário = 1.00; 15min: 1.5077× vs 1.5077×, dif = 0.00×, CV = 1.00 | **NÃO SUPORTADA**: a alternativa sazonal não altera a métrica nem reduz a dispersão horária; não há suporte para substituir o `a` canônico |

### H03 — robustez temporal (anexo, não hipótese nova)

- **Pergunta:** o critério original de H03 continua satisfeito em um bloco temporal que não participou da estimação?
- **Regra original preservada:** β > 0.25 e R² ≥ 0.80 para a relação log-log `body/ATR ~ a`, em 20 faixas equifrequentes. Não se alteraram definição do motor, variáveis ou limites de aprovação.
- **Desenho:** janela comum WIN 5min/15min de 2024-06-19 a 2026-05-14; treino nos primeiros 12 meses; holdout no intervalo restante. As bordas dos 20 quantis são obtidas apenas no treino e congeladas para o holdout; IC95% do β de holdout usa bootstrap por pregão.
- **Resultados:** ver tabela reproduzível em [ANALISE_ESCALONAMENTO_ECONOFISICO.md](ANALISE_ESCALONAMENTO_ECONOFISICO.md). Em ambos os TFs, treino e holdout satisfazem separadamente o critério original; os intervalos de β do holdout permanecem acima de zero.
- **Leitura:** isto sustenta robustez temporal dentro da janela disponível, mas não prova causalidade física, não substitui replicação em outros períodos e não implica direção nem desempenho operacional. H03 mantém seu ID e veredito; este é um anexo de validação.

## 3.1 Evidência e adequação dos dados para H29

- **Amostra usada:** 2020–2026, WIN, 5 min e 15 min; eventos de absorção: 1.273 no 5 min e 1.479 no 15 min; controle: 55.137 e 51.061 candles, respectivamente.
- **Evidência atual:** range/ATR médio é 1.60× vs 1.03× no 5 min e 1.71× vs 1.03× no 15 min; persistência de 1.56 e 1.67; $t_{exp}$ de +20.14 e +25.68.
- **Limitação:** os dados são suficientes para descrever atividade e persistência, mas não para concluir sobre direção, entrada, SL, SG, risco ou qualidade operacional. O retorno médio da absorção foi menor que o controle, portanto o evento não é um sinal direcional.
- **Validação temporal (anexo, não hipótese nova):** no split 2024-06-19 a 2025-06-18 / 2025-06-19 a 2026-05-14, treino e holdout passam a regra Welch original em 5min e 15min. Na sensibilidade pareada por pregão e mesma hora, IC95% do Δ range/ATR: 5min treino +0.185 [0.113, 0.261], holdout +0.346 [0.125, 0.657]; 15min treino +0.033 [−0.058, 0.125], holdout +0.098 [−0.020, 0.217]. Método e amostras em [VALIDACAO_TEMPORAL_H29.md](VALIDACAO_TEMPORAL_H29.md).
- **Leitura e limite:** o controle mais estrito sustenta diferença positiva no 5min nos dois blocos, mas é inconclusivo no 15min; por isso a robustez intrassessão de H29 é mais convincente no 5min. O Welch histórico continua sendo o critério formal já registado, sem alteração retroativa. Nenhum resultado demonstra causalidade, direção ou eficácia operacional. Próxima verificação: bloco temporal independente mais distante, se o acervo permitir; não alterar definição, limiar, frequência, controle ou horizonte.
- **Validação temporal (anexo, não hipótese nova):** corte fixo 2025-06-19 na janela comum 2024-06-19 a 2026-05-14; parâmetros originais preservados. Resultados e limitações em [VALIDACAO_TEMPORAL_H29.md](VALIDACAO_TEMPORAL_H29.md). O teste usa o Welch histórico de H29; inferência por pregão ainda é o próximo refinamento estatístico.

## 4. Backlog de hipóteses (a implementar)

| id | hipótese proposta | critério sugerido |
|:---|:---|:---|
| H26 | Janela em **tempo físico constante** (ex.: 100 min) torna 5/15/30 min comparáveis | persistência e % colorido equivalentes entre TFs |
| H28 | O volume sazonal substitui o `a` canônico sem perder o alerta de volatilidade | \|Δ expansão do range seguinte\| ≤ 0.03× e CV horário ≤ 0.15 |
| H29 | "Absorção" (a ≥ 2 com \|m\| < 0.3) tem comportamento próprio no 5 min (persistência 1.55; μ h3 = +21.7) | replica fora da amostra (2020–24) com \|t\| ≥ 3 |
| H30 | Em dias muito direcionais (\|C−O\|/amplitude no top 20%) a distribuição de cores no dia difere da dos demais | diferença no horário médio da 1ª cor ou na proporção de brilhantes |
| H31 | Áreas por cluster (≥ 2 candles de mesma família, 1 neutro): o preço retorna às bordas em até N candles mais que janelas aleatórias do mesmo horário e largura | o retorno observado deve ser maior que o controle, com \|t\| ≥ 3; neste teste o retorno observado foi menor nos dois TFs: 5 min 87.1% vs 95.0% (t = -8.21), 15 min 92.9% vs 95.1% (t = -3.54) |
| H32 | Os vereditos H06–H20 se mantêm em 2020–2024, nos timeframes com cobertura suficiente | mesmos vereditos com regras congeladas; auditar cobertura antes de comparar. A cobertura WIN 5min conhecida começa em 2024-06-19, então não sustenta uma conclusão 2020–2024 completa nesse TF |
| H33 | Trocar \|F\| ≥ 70 por "colorido" no robô V16 não muda o resultado no simulador | PnL/PF/edge equivalentes na mesma rodada |
| H34 | Entrada antecipada: com volume confiável, iniciar antes da ignição poderia capturar mais do range disponível, mesmo abaixo de 1,5σ? | estudo separado; definir previamente o que significa "volume confiável", regra de entrada/saída, custos e controle comparável; ainda não testada |
| H35 | Entrada na ignição: iniciar operação quando cruza 1,5σ e permanecer até saturação em 2,5σ poderia aproveitar o trecho entre os dois níveis? | estudo separado; definir execução no cruzamento, saídas/stop, custos, amostra fora da seleção e controles; ainda não testada |
| H36 | Quantas oportunidades operacionais válidas por sessão o motor permite, sob regras de sinal e de não duplicação previamente definidas? | definir “oportunidade válida” sem olhar PnL; reportar distribuição por sessão e intervalos de confiança, sem converter frequência em qualidade |
| H37 | Qual faixa de ganho/SG é compatível com a distribuição de deslocamento observada após uma oportunidade válida? | estudo operacional separado; definir preço de entrada, horizonte, custos e distribuição de excursão favorável; comparar faixas em dados fora da amostra |
| H38 | Qual regra de posicionamento do SL deve ser comparada: abertura, fechamento, mínima/máxima do candle de sinal ou outra referência estrutural? | comparar regras pré-definidas no mesmo conjunto de operações, com custos, gaps, excursão adversa e risco por operação; ainda não testada |
| H39 | A coincidência de um alarme sonoro de ignição ou saturação em dois ou mais timeframes aumenta a confiança do sinal? | comparar eventos coincidentes vs. eventos isolados em relação ao próximo range, retorno e frequência; não usar o número de alarmes como prova de direção ou qualidade operacional |

### Hipóteses exploratórias novas — H44–H48 (todas PENDENTES)

Estas propostas respondem perguntas que o painel atual ainda não resolve. Não fazem parte do painel automático e não têm veredito. Antes de qualquer teste, congelar evento, horizonte, controles, unidade de análise e divisão temporal. Começar com estatística por pregão/blocos, não tratar candles dependentes como observações independentes.

| id | pergunta / hipótese | evento e critério inicial | escopo de dados proposto |
|:---|:---|:---|:---|
| H44 | **A primeira cor após neutro carrega direção em algum horizonte?** | Evento = candle colorido fechado após ≥1 candle neutro dentro do mesmo pregão; excluir primeira barra do pregão. Medir retorno alinhado e excursões favorável/adversa em 1, 3 e 6 barras, comparando com controles do mesmo horário e timeframe. Relatar cada horizonte; direção só é apoiada se o efeito pré-definido tiver IC por pregão que exclua zero e magnitude prática definida antes do teste. | Exploração em WINFUT 5min de `2024_26`; validação cronológica em WINM26 5min de `2026`. 15min é réplica secundária. Não misturar “primeira cor do dia” com “primeira após neutro”. |
| H45 | **A expansão após saturação decai em quantas barras?** | Evento = estado brilhante fechado (`|est|=2`); comparar range/ATR futuro em h=1,3,6 com controles da mesma sessão/hora e regime. Estimar curva temporal e IC por pregão. Critério descritivo: identificar se a diferença evento−controle persiste até h=3 ou h=6; não inferir lado do preço. H20 já cobre apenas o próximo candle, então esta é uma extensão multi-horizonte, não sua repetição. | WIN 5min principal; replicar em 15min e no período WINM26 2026 após fechar a definição. |
| H46 | **Com esforço alto, absorção e impulso têm desfechos diferentes?** | Estratos pré-fixados por `a≥2`: absorção `|m|<0,3`, impulso `|m|≥0,7`, intermediário `0,3≤|m|<0,7`; comparar expansão futura range/ATR e retorno alinhado em 1 e 3 barras, com controle por hora/pregão. Reportar n e intervalos; não interpretar retorno como entrada. H29 já compara absorção com o restante, mas não faz esse contraste explícito entre estratos. | Começar em WIN 5min `2024_26`; replicar sem retunar em WINM26 `2026`. 15min secundário. |
| H47 | **A anatomia do candle (pavio superior/inferior) acrescenta informação descritiva além de `est`?** | Definir `w_up=(h−max(o,c))/range` e `w_dn=(min(o,c)−l)/range`; estratos exploratórios: diferença `w_up−w_dn` ≥0,2, ≤−0,2 ou intermediária. Desfecho primário proposto: retorno alinhado em 3 barras; secundários: range/ATR e excursões em até 6 barras. Comparar modelos com/sem anatomia no holdout por pregão, com limiares congelados e ajuste para múltiplas comparações. | Exploração 5min em `2024_26`; validação 5min em `2026`; 15min como análise secundária. Aplicar controle de múltiplas comparações por haver vários estratos. |
| H48 | **Os achados descritivos se mantêm entre janelas e séries de contrato sem duplicar timestamps?** | Hipótese de robustez/proveniência: recalcular métricas congeladas (H17, H20, H29, H44–H47 quando prontas) separadamente em períodos não sobrepostos; comparar `WINFUT` contínuo com contratos explícitos apenas em datas comuns e nunca contar observações coincidentes como replicações independentes. Resultado depende de auditoria de cobertura, duplicatas, gaps e seleção do contrato líquido. | `2024_26` (WINFUT, 5min disponível de 2024-06-19 a 2025-12-30) como desenvolvimento; `2026` (WINM26, 2026-01-02 a 2026-05-14) como holdout temporal inicial; `CandlesHistoricos2026` (WINQ26 em 5min, 2026-02-13 a 2026-07-24) como contrato alternativo, com sobreposição WINM26/WINQ26 marcada e não independente. |

### Auditoria de cobertura e seleção das três pastas solicitadas

- `2024_26/WINFUT_F_0_5min.csv`: 43.421 linhas brutas, 2024-06-19–2025-12-30. `2026/WINM26_F_0_5min.csv`: 7.430 linhas, 2026-01-02–2026-05-14. São blocos temporais adjacentes para análise cronológica, embora a rolagem de contrato exija cuidado.
- `CandlesHistoricos2026/WINFUT_F_0_5min.csv`: 33.592 timestamps, 2024-10-18–2025-12-30; os timestamps são subconjunto do WINFUT em `2024_26`, portanto **não** constituem amostra independente nem devem ser somados.
- `CandlesHistoricos2026/WINQ26_F_0_5min.csv`: 8.428 linhas, 2026-02-13–2026-07-24; sobrepõe-se temporalmente a WINM26 em 2026, mas é outro contrato e não é replicação temporal independente. O seu recorte pode ser usado para comparar série de contrato em datas coincidentes ou para um bloco posterior separado, após checar gaps/unidades.
- **Limitação importante do carregador atual:** `Contexto._path_for()` retorna o primeiro arquivo encontrado na ordem das pastas; ele não concatena as pastas. Assim, passar `--pastas 2024_26 2026 CandlesHistoricos2026` não garante uma série contínua: para 5min, pode carregar apenas o WINFUT de `2024_26` e ignorar os demais. Já `analise_ignicao_saturacao.py` concatena fontes e escolhe um contrato por pregão, mas sua lista canônica termina em `2026` e não inclui `CandlesHistoricos2026`. Corrigir/explicitar a seleção antes de chamar os resultados de cobertura 2026–julho.
- A janela documentada em H03/H29 e no estudo de ignição/saturação termina em **2026-05-14**; não cobre WINQ26 até julho. H03/H29 e H20 têm resultados descritivos, mas ainda restam paridade Profit×Python, H31 com controle pós-fechamento válido, robustez H32 dentro da cobertura real, e as hipóteses operacionais H34–H38/H41–H43. O notebook legado em `CandlesHistoryDatas/2024_26` falha no import de pandas e usa caminhos/parâmetros incompatíveis com o motor canônico; não contar como validação concluída.

### Casos concretos para inspeção visual (não são resultados de hipótese)

Os campos abaixo foram recalculados com `analise_candles.calcular()` na série indicada e servem somente para abrir uma ficha visual/procurar contexto. Foram escolhidos por seus atributos do motor; portanto, são exemplos selecionados e **não** podem compor a amostra confirmatória nem estimar desempenho. Guardar captura com barras anteriores/posteriores, contrato, timeframe, OHLC, volume, `m`, `a`, `F`, `μ`, `σ`, `z`, estado e qualidade do timestamp.

| pergunta inicial | série / timeframe / horário | leitura numérica preliminar | por que olhar / cautela |
|:---|:---|:---|:---|
| H44 — transição para primeira cor positiva | WINFUT, `2024_26`, 5min, 2025-06-10 09:05 | estado `VL`; F=+532,0; z=+4,29; a=6,12; m=+0,87 | Conferir barra anterior no mesmo pregão e se a janela começa após neutro; o estado e timestamp são exemplos, não evidência direcional. |
| H44 — transição para primeira cor negativa | WINFUT, `2024_26`, 5min, 2025-08-20 14:05 | estado `RV`; F=−430,3; z=−4,22; a=4,76; m=−0,90 | Par visual de família oposta; não selecionar só casos brilhantes na análise agregada. |
| H46 — esforço alto, corpo curto sem cor extrema | WINFUT, `2024_26`, 5min, 2025-08-12 09:00 | `a`=9,80; `m`=−0,03; F=−32,5; z=−1,34; N | Exemplo de esforço alto/corpo pequeno que fica neutro: útil para distinguir a geometria do candle do estado final. É barra de abertura e pede controle horário. |
| H46 — absorção que também é brilhante | WINFUT, `2024_26`, 5min, 2024-10-24 09:00 | `a`=13,09; `m`=−0,14; F=−186,6; z=−3,37; estado vermelho brilhante | Ilustra que “absorção” pelo critério `a, |m|` não determina cor/direção. Confirmar o rótulo exato no CSV calculado; tratar abertura separadamente. |
| H45/H48 — alerta de dado extremo | WINM26, `2026`, 5min, 2026-03-31 16:05 | estado vermelho brilhante; F=−4.659,6; z=−4,36; a=76,88; m=−0,61; range=330 | Inspecionar volume/unidade, barras ao redor, contrato e eventual notícia/rolagem antes de interpretar. Este ponto extremo não deve ser tomado como representativo. |

**Atenção à unidade:** `WINFUT` contínuo, contratos `WINM26`/`WINQ26`, volume e escalas de preço podem ter diferenças de fonte/ajuste. Estes casos são candidatos a verificação e podem ser reclassificados como problema de dados; não são sugestões de trade.

### Referência visual das hipóteses H34–H35

- **Origem:** print enviado pelo usuário em 2026-10-06, gráfico Profit identificado como **WINV26 · 5 min**; contadores de candles visíveis chegam a 70. O anexo mostra candles, regiões/faixas marcadas, o indicador `FORCA_WIN_ESTUDO_FMA` com os níveis de ignição/saturação e duas anotações amarelas.
- **Pergunta associada à anotação superior:** se houver volume considerado confiável, iniciar antes da ignição poderia capturar o range de pontuação mesmo abaixo do limiar de ignição (H34)?
- **Pergunta associada à anotação inferior:** a passagem pela ignição poderia ser gatilho para iniciar e manter a operação até alcançar a saturação (H35)?
- **Leitura textual visível do painel do indicador no print:** parâmetros 1,50 / 2,50 e valores mostrados aproximadamente `0,00; 12,89; 72,88; 112,87; -47,10; -87,09; 0,00` (ordem aparente dos sete plots; confirmar no Data Window antes de usar numericamente).
- **Limite do registro:** o print permanece anexado à conversa; não foi criado nem localizado arquivo de imagem no repositório. As perguntas são ideias para teste, não evidência de eficácia. Não inferir resultados a partir deste screenshot isolado.
- **Escopo futuro:** H34–H35 são hipóteses de execução/backtest, não mudanças no motor FMA. Estudá-las apenas depois da etapa atual de compreensão e paridade do indicador; manter a análise de reversões em capítulo separado.

### Hipóteses operacionais H36–H43 — fila, entrada, SL e SG

- **H36 — quantidade de operações válidas por dia:** primeiro definir “oportunidade válida” apenas pela regra do motor e pelos filtros de dados, sem usar resultado futuro. Medir quantas ocorrem por sessão (mediana, quantis e dias sem sinal); só depois estudar valor operacional.
- **H37 — faixa de SG:** não selecionar o alvo pelo melhor resultado histórico. Estudar a distribuição do deslocamento/excursão favorável a partir de uma entrada definida, com custos, horizonte e amostra de validação separados; testar poucas faixas predefinidas.
- **H38 — localização do SL:** tratar abertura, fechamento, mínima/máxima do candle de sinal e níveis estruturais como variantes distintas. Comparar no mesmo conjunto de sinais, incluindo gaps, excursão adversa, risco em pontos e regras de execução realistas.
- **H41 — entrada pela área do candle:** testar a entrada ao preço de abertura, fechamento, mínima ou máxima do candle de sinal, e depois testar igual opção no candle posterior. A variante é selecionada antes da comparação e não por desempenho observado.
- **H42 — SL pela área do candle:** comparar SL na mínima/máxima do candle de entrada, no fechamento ou na abertura, e avaliar também níveis estruturais próximos. O risco do teste será medido em pontos e em relação ao intervalo de entrada.
- **H43 — SG por disponibilidade de deslocamento:** comparar faixas calculadas a partir do próximo range/ATR, da área do próximo candle colorido e de faixas percentuais fixas. Não atribuir um número de pontos antes da distribuição do evento ser calculada.
- **Dependência e ordem:** H36–H43 só entram em análise operacional após concluir a descrição do motor e a paridade Profit × Python. Não misturar esta fila com o capítulo futuro de reversões. Nenhuma hipótese tem veredito ou parâmetro recomendado neste momento.

## 5. Decisões propostas (a confirmar)

1. **Linguagem da dissertação:** "âncora de percentil (≈ P79)" no lugar de "princípio de Pareto"; manter "cauda pesada" e "Pareto" apenas para a descrição da cauda no 5 min (H08).
2. **Papel da cor:** alerta de atividade/risco e mapa de energia (clusters). Evitar a tese "exaustão → reversão" e "escuro → continuação" (H18, H19) até haver teste novo.
3. **Próxima teoria (áreas):** 5 min, clusters de ≥ 2 candles com tolerância de 1 neutro, volume sazonal opcional; primeiro teste: H31.
4. **Robôs:** o resultado não justifica trocar o limiar 70 por Bollinger *por previsão* (H16); se a troca for desejada, validar no simulador como nova rodada numerada (H33), seguindo a estrutura de `Robots/Results/`.

## 6. Ordem canônica e estado da validação

1. **Modelo e dados:** fórmula, limiares, cores e análises Python documentados — concluído para o escopo 2024–2026.
2. **Instrumentação:** cópia do V18.2 preservada; indicador `FORCA_WIN_V18_2_estudo_fma.ntsl` foi compilado e executado no Profit pelo usuário em 2026-10-06; cores aparecem como esperado — smoke test concluído.
3. **Paridade NTSL × Python:** ainda pendente. O registro formal da checagem está em [PARIDADE_NTSL_PYTHON.md](PARIDADE_NTSL_PYTHON.md); usar os 10 alvos e comparar F, μ, σ, bandas e estado no mesmo timestamp. Executar sem ordens; carregar 39 barras anteriores e confirmar a série/unidade de Volume.
4. **Robustez temporal:** após paridade, rodar a análise ampliada de cinco anos e rever H06–H25 sem alterar a regra no meio da amostra.
5. **Teoria de áreas:** depois de congelar as cores, executar H31 (clusters de mesma família e teste de retorno às bordas contra controle aleatório).
6. **Estratégia operacional:** somente após essas etapas propor integração com robô e criar rodada de simulador separada; o indicador de estudo não é o robô.
7. **Gráficos:** construir/exportar apenas no fechamento da análise correspondente, a partir de métricas e conclusões já registradas nos documentos canônicos; evitar painéis intermediários que antecipem interpretação ou dupliquem trabalho. O HTML WIN atual é protótipo exploratório, não figura final.
