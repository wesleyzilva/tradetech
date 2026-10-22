# Paridade NTSL × Python — FMA / análise de candles

## Objetivo

Este documento registra a checagem de consistência entre:

- a implementação canônica em Python, em [TeseFma_analiseCandle/analise_candles.py](analise_candles.py);
- a validação estatística em [TeseFma_analiseCandle/validacao_econofisica.py](validacao_econofisica.py);
- o estudo visual em Profit / NTSL, representado por `FORCA_WIN_V18_2_estudo_fma.ntsl` e pela cópia/estudo do indicador relacionado.

A finalidade não é transformar o motor em operação. A finalidade é responder uma pergunta metodológica simples e essencial:

> o estudo em Profit está descrevendo a mesma grandeza física e os mesmos limiares do motor em Python?

Se a resposta não for sim, a evidência não pode ser tratada como validação do motor ou como base para recomendação operacional.

---

## 1. Hierarquia correta da evidência

A ordem correta é:

1. Motor canônico em Python
   - definição de F, m, a, mu, sigma, z, fam, est, cores e estados;
   - fonte de verdade para a tese.

2. Validação estatística
   - os testes H27, H28, H29, H39 e demais blocos AUTO em [TeseFma_analiseCandle/validacao_econofisica.py](validacao_econofisica.py);
   - mede associação, persistência e expansão, sem transformar um padrão em direção operacional.

3. Estudo em NTSL / Profit
   - serve como replicação visual e de smoke test;
   - não substitui a referência canônica;
   - só é útil se estiver consistente com a série em Python no mesmo timestamp.

4. Estratégia operacional
   - entra somente depois que a paridade e a descrição do motor estiverem estáveis;
   - não é etapa da tese de motor, e sim deliberação independente.

---

## 2. O que está sendo comparado

A comparação deve ser feita em timestamps exatos, linha a linha, sem reduzir a análise à cor do candle.

### 2.1 Grandezas do motor

As grandezas canônicas são:

- F = m × a × 100
- m = variação relativa do corpo do candle ou equivalente no código do motor
- a = aceleração / componente de volume ou sinal de intensidade
- mu = média móvel da janela de referência
- sigma = desvio padrão da janela de referência
- z = (F - mu) / sigma
- fam = família / sinal dominante (verde, vermelho, neutro)
- est = estado do motor (ignição, saturação, neutro, etc.)

### 2.2 O que precisa ser comparado em paridade

Na referência Python de cada timestamp, registrar:

- data e hora
- OHLC
- volume e unidade do volume na fonte Python
- F
- a
- m
- mu
- sigma
- z
- faixa/range
- família / cor Python
- estado / ignição / saturação Python
- limiares usados (`1.5σ`, `2.5σ`; limiares distintos de robô devem ser identificados separadamente)

No Profit, comparar somente os campos que a interface efetivamente disponibiliza: timestamp/horário, índice da barra no dia, OHLC indicado no gráfico e plots/cores/escala visíveis do indicador. Não exigir os componentes internos acima como valores Profit enquanto não forem expostos pelo estudo.

O diagnóstico correto é feito pela comparação dos valores numéricos, não pela aparência visual.

---

## 3. Regras de aceitação da paridade

A paridade numérica só é aceita quando:

1. o timestamp coincide exatamente;
2. as grandezas numéricas correspondentes (incluindo `F`) estão expostas nos dois ambientes e batem dentro da tolerância admissível;
3. os limiares e a ordem da janela são iguais;
4. a família e o estado são equivalentes;
5. a unidade de volume e o cálculo de aceleração são consistentes;
6. não há “correção” baseada apenas em cor visual quando os valores numéricos divergem.

Se o Profit não expõe as grandezas internas, não declarar paridade numérica: registrar `VISUAL_SOMENTE` após validar timestamp, candle e OHLC. Essa classificação é evidência útil de correspondência visual, mas não satisfaz os critérios de paridade matemática.

### Critério prático

- F, m, a, mu, sigma e z devem ser compatíveis numericamente;
- casamento por timestamp com zero ambiguidade;
- divergência visual não pode ser usada como argumento para ajustar o código sem primeiro medir a diferença em dados.

Se houver divergência entre a imagem e os números, a hipótese correta é: a visualização precisa ser recalibrada ou o cálculo está em outra unidade. O código Python não pode ser “arrumado” só para parecer consistente com a cor de um print.

---

## 4. Checklist de execução

### Passo 1 — preservar a referência canônica

- manter [TeseFma_analiseCandle/analise_candles.py](analise_candles.py) como origem do motor;
- não reescrever a lógica do motor para encaixar uma imagem de Profit;
- não alterar limiares sem registro explícito em hipótese nova.

### Passo 2 — preparar o lote de casos

- usar um lote de 10 alvos de paridade, como informado no fluxo de trabalho da tese;
- carregar as 39 barras consecutivas anteriores ao alvo na mesma série temporal usada pelo motor, sem interpretar isso como número de barras do dia anterior;
- evitar argumentos de execução que usem ordens reais.

### Passo 3 — comparar valores por timestamp

Para cada caso, registrar:

- `dt`
- `OHLC`
- `volume`
- `m`
- `a`
- `F`
- `mu`
- `sigma`
- `z`
- `fam`
- `est`
- `limiar` do indicador

### Passo 4 — classificar o resultado

Classificar cada caso em um destes estados:

- `PARIDADE_OK`: valores e estados consistentes;
- `PARIDADE_DIVERGE`: divergência numérica relevante;
- `VISUAL_SOMENTE`: aparência sem suporte numérico;
- `INCONCLUSIVO`: dados insuficientes ou janela não equivalente.

### Passo 5 — documentar a correção, não a fantasia

Se houver divergência:

- escrever o caso;
- registrar o timestamp e o valor divergente;
- testar se a diferença é por unidade, janela, offset, timezone ou rolagem de candle;
- refazer a comparação antes de mexer em limiares.

---

## 4.1 Lote Python preparado em 2026-10-07

Foi criado um lote diagnóstico reproduzível para WINQ26 5min, com dez timestamps entre junho e julho de 2026. O gerador [gerar_casos_paridade_ntsl.py](gerar_casos_paridade_ntsl.py) lê o CSV original e calcula a referência pelo motor canônico; a saída é [PARIDADE_NTSL_CASOS.csv](PARIDADE_NTSL_CASOS.csv). A tabela agora prioriza os quatro casos de junho em ordem cronológica e identifica separadamente o candle do dia, as 39 barras de contexto e o timestamp da barra mais antiga desse contexto.

**Significado de 39:** não é “o candle número 39 do dia anterior”, nem a quantidade disponível no dia anterior. São as **39 barras imediatamente anteriores ao candle-alvo na série ordenada**. A fórmula canônica calcula `a` usando a média de volume das 20 barras anteriores; depois calcula `μ` e `σ` numa janela de 20 valores de `F`, que inclui o atual. Para que esses 20 valores de `F` tenham suas referências de volume completas, o primeiro `F` da janela precisa de mais 19 barras anteriores: $20+19=39$. Como o cálculo Python percorre a série sem reiniciar a cada sessão, essas barras podem atravessar o fechamento de um dia para o seguinte. A coluna `context_start_timestamp` mostra exatamente a mais antiga das 39 barras; `context_start_candle_no` informa seu número dentro da própria sessão. `source_rows_before_target` apenas informa quantas linhas existem desde o início do arquivo e **não** é a janela exigida.

Casos de junho, na ordem que vamos revisar primeiro:

| Caso | Timestamp Python | Candle no dia | Barras do mesmo dia anteriores | Barra mais antiga das 39 de contexto |
|---|---|---:|---:|---|
| P10 | 2026-06-01 10:20 | 17 | 16 | 2026-05-29 16:30 (candle 95 da sessão) |
| P03 | 2026-06-11 13:10 | 51 | 50 | 2026-06-11 09:55 (candle 12 da sessão) |
| P01 | 2026-06-15 09:20 | 5 | 4 | 2026-06-12 15:30 (candle 92 da sessão) |
| P05 | 2026-06-23 13:05 | 50 | 49 | 2026-06-23 09:50 (candle 11 da sessão) |

Exemplo P01: o alvo é o candle 5 do dia, logo só há quatro candles do mesmo dia antes dele. O cálculo ainda tem o contexto anterior desde 12/06 às 15:30; por isso, ao reproduzi-lo, não se deve reiniciar as médias no começo do pregão sem confirmar que o Profit também as reinicia. Para P10 e P01, uma janela contínua de 39 barras inclui sessão(ões) anterior(es).

- P01–P02: neutro, incluindo um caso próximo de −1,5σ;
- P03–P04: verde escuro próximo de +1,5σ;
- P05–P06: verde brilhante, um próximo de +2,5σ e um extremo;
- P07–P08: vermelho escuro, próximos de −1,5σ e −2,5σ;
- P09–P10: vermelho brilhante, próximo do limite e um mais distante.

**Estado da comparação:** a referência Python está preenchida. O Profit não exibe `m`, `a`, `F`, `μ`, `σ` e `z` como valores numéricos por candle; portanto, a comparação possível é visual/de identificação: timestamp, número da barra, OHLC e plots/escala do indicador. P01 já tem evidência visual de timestamp, candle 5 e OHLC coincidentes. Os cálculos internos não podem ser declarados numericamente em paridade com base nisso. A escolha estratificada serve para inspeção diagnóstica, não é amostra aleatória nem teste de desempenho.

**Lote anterior:** a instrução de domínio registra uma observação de divergência visual em cinco de dez casos WINQ26 Jun–Jul/2026, mas não localizei nesta cópia do repositório o gerador, a lista dos dez timestamps nem as observações numéricas do Profit que permitam reproduzi-la. Não atribuir esse relato ao lote P01–P10 recém-criado. Se a lista ou capturas antigas estiverem disponíveis, preservar como lote histórico distinto.

### O que a comparação Profit × Python pode certificar

No indicador atual, `m`, `a`, `F`, `μ`, `σ` e `z` são valores calculados e disponíveis no relatório Python, não valores numéricos expostos por candle no Profit. Não pedir nem inventar campos numéricos Profit para essas grandezas. Registrar no CSV a referência Python e, do Profit, apenas o que é observável: timestamp, número sequencial da barra na sessão, OHLC identificável na escala do candle, nome do indicador e correspondência visual de plots/cores/escala.

Com esses dados é possível certificar que se selecionou a mesma barra e documentar uma correspondência visual do indicador. **Não é possível certificar a igualdade numérica das fórmulas internas, de `F` ou de `z` somente por captura da escala/cores.** Se no futuro houver uma saída numérica por barra no Profit, essa comparação poderá ser ampliada sem substituir a referência Python.

## 4.2 Roteiro de reprodução e capturas de evidência no Profit

O lote P01–P10 é uma referência diagnóstica, não certificação oficial nem teste de rentabilidade. Uma captura comprova o que estava visível no Profit; **não substitui os valores numéricos com precisão suficiente**. Para uma auditoria repetível, seguir esta ordem sem mudar fórmula ou limiares no meio da coleta:

1. **Congelar a versão:** usar o indicador de estudo FMA sem ordens, preservar o fonte NTSL exato compilado e registrar nome/versão e data da compilação. Não usar nem alterar a referência original. Este workspace não contém uma cópia legível do fonte `FORCA_WIN_V18_2_estudo_fma.ntsl`; se ele existir apenas no Profit/local, registrar a versão usada e guardar uma cópia de auditoria no local seguro do projeto.
2. **Fixar o gráfico:** selecionar contrato específico `WINQ26` (não `WINFUT` contínuo), periodicidade 5 minutos, mesma fonte/histórico de barras e sessão usada pela referência. Conferir data/hora do Profit e se o horário exibido identifica abertura ou fechamento da barra. Registrar isso em `profit_bar_time_basis` para cada caso.
3. **Carregar contexto:** assegurar que as 39 barras imediatamente anteriores já estejam carregadas antes do alvo, além da barra-alvo fechada. Usar `context_start_timestamp` como início de contexto. Não contar apenas barras do pregão atual; para candle 5, por exemplo, há somente quatro barras do dia antes do alvo, então a janela vem também de sessões anteriores. Não comparar candle em formação.
4. **Selecionar o timestamp exato:** conferir `timestamp` e OHLC da linha Python com a barra do gráfico. Se horário ou OHLC não casar, parar naquele caso: verificar convenção de abertura/fechamento, fuso, sessão, ativo/contrato e ajustes do histórico antes de ler cores.
5. **Confirmar a barra:** no Profit, validar o horário selecionado, número da barra do dia/sessão e OHLC indicados no gráfico/escala do candle. Comparar esses campos com `timestamp`, `candle_no_python` e OHLC Python. Se divergir, revisar convenção horário de abertura/fechamento, contrato, sessão e fonte dos candles.
6. **Inspecionar o indicador:** deixar visíveis nome do estudo, escalas e plots/cores. Anotar o que a escala efetivamente demonstra; valores no eixo ou rótulos do último candle não devem ser atribuídos à barra selecionada sem indicação explícita do Profit. Os números internos `m`, `a`, `F`, `μ`, `σ` e `z` ficam registrados somente como referência Python.
7. **Fazer a captura auditável:** um print por caso, nomeado `P01_WINQ26_5min_2026-06-15_0920_candle05.png`, salvo em `TeseFma_analiseCandle/graficos_motor/paridade_profit/`. Deixar visíveis ativo/contrato, 5min, data/hora selecionada, posição/número da barra, OHLC/escala do candle e nome/escala do indicador. Se não couber, fazer dois prints complementares. Preservar os originais e ocultar dados pessoais/financeiros desnecessários.
8. **Preencher a planilha:** registrar os valores visuais observados em `profit_visual_*`, `profit_candle_no`, `profit_bar_time_basis`, `evidence_screenshot` e notas. Manter sem preenchimento as métricas Python-only nos campos de referência Profit; vazio não significa zero nem divergência.
9. **Classificar corretamente:** primeiro validar timestamp e OHLC; depois registrar se os plots/cores são visualmente consistentes com a referência qualitativa Python. Use `VISUAL_SOMENTE` quando só a aparência/escala está disponível; `INCONCLUSIVO` se nem a barra puder ser identificada; `PARIDADE_DIVERGE` apenas para divergência observável definida; `PARIDADE_OK` fica reservado a uma comparação numérica real de variáveis equivalentes. Escala e cor, isoladamente, não provam igualdade de `F`/`z`.

### Quadro mínimo que cada print deve permitir auditar

| Elemento | Deve estar identificável |
|---|---|
| Instrumento | WINQ26 — contrato exato, não série contínua |
| Período | 5 minutos |
| Barra | data e hora selecionada e sua convenção temporal |
| Dados-base | OHLC visível na escala/seleção do candle; número sequencial da barra |
| Indicador | nome/versão do estudo NTSL e escala/plots/cores visíveis |
| Métricas internas | `m`, `a`, `F`, `μ`, `σ`, `z` como referência Python; não solicitar como leitura Profit se não forem expostas |
| Arquivo | nome corresponde ao `case_id`; captura original sem alteração dos números |

“Certificação” aqui significa **trilha interna de reprodução e auditoria**. Com os dados atualmente visíveis no Profit, a certificação cobre identificação da barra e inspeção visual, não equivalência numérica das fórmulas internas nem direção, timing de entrada, stop/alvo ou rentabilidade.

### Triagem do print P01 recebido em 2026-10-07

O print atualizado mostra WINQ26 5min, o estudo `FORCA_WIN_ESTUDO_FMA`, o tooltip `15/06/2026 09:20`, o candle número **5** e os níveis OHLC: abertura 176.420, máxima 176.480, mínima 176.150 e fechamento 176.315. Eles coincidem com P01 no Python; também se veem a escala e os plots do indicador. É uma melhora suficiente para **identificar e documentar a mesma barra**.

O print não transforma escala/plots em leitura numérica de `m`, `a`, `F`, `μ`, `σ` ou `z` daquela barra. Os rótulos do eixo/plots podem representar valores do último ponto ou escala do painel, não necessariamente o ponto selecionado; por isso não os registrei como números da barra. P01 passa a ter status **identificação visual da barra confirmada; paridade matemática interna não verificável por esta interface**. A captura continua anexada à conversa e não foi arquivada no diretório local de evidências.

O número 5 corresponde ao quinto registro de candle do dia na série Python, contando a primeira barra disponível (09:00) como 1. O CSV passa a trazer `candle_no_python` para todos os casos e `profit_candle_no` para a observação Profit; o horário 09:20 coincide com o timestamp Python deste caso.

## 5. O que é aceitável como evidência e o que não é

### 5.1 Aceitável

- comparação de valores em timestamps idênticos;
- teste de estabilidade da série em python;
- gráfico/print do estudo como smoke test visual;
- comparação de histograma, expansão e persistência em dados reais.

### 5.2 Não aceitável

- achar que uma cor bonita no Profit é prova de validade do motor;
- ajustar limiares pelo visual sem usar a série de dados;
- dizer que o sinal “funciona” porque o print parece coerente;
- usar contagem de cores como evidência de direção ou de qualidade operacional.

---

## 6. Limites da inferência

Mesmo com paridade aceita, ainda há limites rigorosos:

- a análise de motor não é análise de execução;
- a cor não prova direção;
- a persistência e a expansão são descrições de comportamento, não sinal de entrada;
- a existência de um evento de alta força não define regra de SL, SG, risco, timing ou quantidade;
- a tese de motor e a tese operacional são capítulos distintos.

Em outras palavras:

> a paridade confirma que o indicador está descrevendo a mesma estrutura matemática em ambos os ambientes.

Mas ela não confirma que esse comportamento é operacionalmente rentável.

---

## 7. Status esperado da validação

### O que o motor prova

- a estrutura matemática do cálculo é coerente;
- a cor/família/estado são frutos de uma lógica interna consistente;
- a expansão e a persistência de certos eventos podem ser descritas empiricamente;
- certos padrões têm associação maior com eventos posteriores, dentro do escopo do estudo.

### O que o motor só sugere

- que alguns eventos podem servir como alerta de energia ou risco;
- que certos clusters ou estados podem anteceder comportamento distinto;
- que a cor e a intensidade podem ser úteis como contexto, mas sem garantia operacional.

### O que ainda é hipótese

- direção, execução, timing, stop, target e racionamento de risco;
- “ignição antes da entrada”, “saturação como saída”, “multitimeframe como confirmação”;
- qualquer regra que dependa de operação real ou de backtest para ser validada.

---

## 8. Conclusão metodológica

A paridade NTSL × Python é a etapa correta antes de qualquer recomendação operacional. Ela é a forma de transformar uma ideia visual em um fato verificável.

A regra de ouro desta tese é:

> não trocar a lógica do motor por uma aparência do gráfico; primeiro confirme o número, depois avalie a interpretação.

Até a paridade estar concluída, a análise permanece em nível de motor e de hipótese descritiva, não em nível de estratégia executável.

---

## 9. Referências locais

- [TeseFma_analiseCandle/analise_candles.py](analise_candles.py)
- [TeseFma_analiseCandle/validacao_econofisica.py](validacao_econofisica.py)
- [TeseFma_analiseCandle/HIPOTESES.md](HIPOTESES.md)
- [.github/instructions/tradetech-win-scalper.instructions.md](../.github/instructions/tradetech-win-scalper.instructions.md)

A próxima etapa após esta paridade é revisar os eventos em separado, sem transformar o resultado em regra operacional e sem usar a cor como prova final de eficácia.
