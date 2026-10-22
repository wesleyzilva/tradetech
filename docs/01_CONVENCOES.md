# Convenções canônicas

Regras que valem para **todos os motores**. Se uma análise as violar, o resultado não entra nos índices de hipóteses.

## 1. Identificadores

| Objeto | Formato | Exemplo | Onde vive |
|---|---|---|---|
| Motor | `M##_nome_curto` | `M02_microestrutura_barreiras` | `motores/` |
| Hipótese | `<prefixo>-H##` (prefixo de 2 letras do motor; M01 mantém `H##` legado) | `MB-H01`, `H29` | `motores/<motor>/HIPOTESES.md` |
| Análise | `ANALISE_###_slug` | `ANALISE_001_baseline` | `motores/<motor>/analises/` |
| Delta | `DELTA_###_slug` | `DELTA_001_protecao_na_entrada` | `motores/<motor>/deltas/` |
| Robô (NTSL) | `Nome_v<N>_<AAAAMMDD>.ntsl` | `Robo_Microestrutura_Barreiras_v1_20261022.ntsl` | `motores/<motor>/robo/` |
| Lote de dados | `<ano-ini>-<ano-fim>[_sufixo]` ou `<ano>-<1S|2S>_<contrato>` | `2024-2025`, `2026-2S_Q26` | `dados/candles/` |

Prefixos já reservados: `MB` (M02), `FM` (reservado para M01 em novas hipóteses; as antigas ficam `H01–H48`), `OR` (M03), `VW` (M04), `TS` (M05), `SZ` (M06), `VR` (M07), `LL` (M08), `CF` (M16), `ML` (M17), `ID` (M18). Ver `docs/03_CATALOGO_MOTORES.md`.

Numeração nunca é reaproveitada. Hipótese refutada continua no registro com veredito; regra mudada ⇒ **novo ID**.

## 2. Ciclo de uma hipótese

```
PENDENTE → (regra congelada) → EXECUTADA → CONFIRMADA | REFUTADA | INCONCLUSIVA
```

1. **Escrever antes de olhar:** enunciado, estatística, critério de veredito, conjunto de dados, controle e horizonte, **antes** de rodar. Isso é o "congelamento".
2. **Rodar** com script versionado em `codigo/` (ou na pasta da tese no M01) que regenera o relatório.
3. **Veredito** pela regra congelada, sem reinterpretar. Se a regra estiver errada, abra um novo ID.
4. **Replicar** em conjunto independente (outro contrato, outro período, outro timeframe) antes de promover para o robô.

### Regras de veredito (padrão)

- **|t| ≥ 3** no conjunto de descoberta (t agrupado por pregão, ver §4) e **|t| ≥ 2 com o mesmo sinal** em pelo menos um conjunto independente ⇒ CONFIRMADA.
- Sinal oposto, ou |t| < 2 no conjunto independente ⇒ não confirmada (INCONCLUSIVA se o poder estatístico é baixo; REFUTADA se o intervalo exclui o efeito mínimo relevante).
- Registrar **quantos testes** foram feitos na análise; com N testes, um |t| ≈ 3 isolado aparece por acaso. Hipóteses ancoradas numa tabela de 20 células exigem replicação.
- Resultados descritivos (frequências, distribuições) não precisam de teste, mas devem dizer que são descritivos.

## 3. Dados

- CSVs brutos em `dados/candles/<lote>/` são **imutáveis**: não editar, não duplicar. Para um novo export, criar novo lote (ou arquivo com período no nome) e rodar `python ferramentas/auditar_candles.py`.
- Ler sempre via `tradetech.dados` (`carregar_serie`, `catalogo_arquivos`), nunca por glob recursivo. Série **padrão** é a única usada por padrão; a série `_alt` (preço ajustado) fica fora (diferença de 5.700–7.200 pts no WIN).
- Timestamps são da **abertura** da barra. Sinal no fechamento da barra `i` ⇒ ordem a mercado na abertura de `i+1`.
- Só usar **pregões completos** (≥ 90 % das barras do p95 do arquivo) em estatísticas por pregão.
- `Volume` do export Profit é **financeiro**; para esforço usar `Quantidade` (contratos).
- **Liquidez:** `carregar_serie` descarta, por padrão, os pregões de contratos `WIN*` com `Quantidade` diária < 1 milhão (`sessoes_liquidas`). Contrato fora do vencimento líquido quase não negocia (WINM26 em jan–mar/2026: 68 a 17 mil por dia, contra 7 a 18 milhões no líquido) e distorce cor, ATR e volume relativo. Usar `liquido=False` só para auditar.
- Contrato contínuo (`WINFUT`) tem *gaps* de rolagem entre pregões: nunca calcular retorno cruzando pregões sem tratar o gap.
- Não reproduzir dados pessoais de exports de corretora.

## 4. Método estatístico

- **Unidade amostral = pregão.** Trades/eventos intradia são dependentes; t-stats agregam por pregão (cluster).
- **Controle nulo obrigatório** para qualquer regra de entrada: mesma janela, mesma frequência, mesma geometria de saída, lado/barra sorteados (≥ 100 repetições). O resultado do motor é um percentil desse nulo.
- **Custos explícitos:** relatar bruto e com 2 e 5 pts por trade (WIN) / equivalente em WDO. Um motor só é "positivo" se o for com custo.
- **Hold-out cronológico:** descobrir em um período, validar em outro (nunca embaralhar).
- **Pior caso na barra:** quando stop e alvo estão na mesma barra, assumir stop primeiro.
- **Sem otimização no baseline:** o baseline de um motor usa os parâmetros do fonte. Varreduras de parâmetros são deltas, com hold-out e contagem de combinações testadas.
- **Paridade antes de conclusão:** o simulador Python deve ter testes sintéticos (`tests/`) e, quando possível, paridade com o Profit (`PARIDADE_*`).

## 5. Relatórios e reprodutibilidade

- Todo relatório numérico é **gerado por script**, com cabeçalho "Gerado por …, não editar à mão". Texto interpretativo manual vai em `HIPOTESES.md` ou no delta.
- Números em pontos de WIN (1 pt = R$ 0,20/contrato) salvo menção.
- Comandos de reprodução ficam no topo de cada script (docstring) e no `README.md` do motor.
- Nada de caminhos absolutos ou específicos da máquina.

## 6. Deltas (o fluxo de evolução)

Um **delta** é uma mudança **única e pequena** no motor com hipótese, medição antes/depois e decisão. Fluxo:

1. `cp docs/templates/DELTA.md motores/<motor>/deltas/DELTA_###_slug.md` e preencher *Hipótese*, *Mudança*, *Métrica primária*, *Critério de decisão* (status `PROPOSTO`).
2. Congelar (status `CONGELADO`): commit só com o delta, antes de rodar.
3. Implementar via `Params`/`com()` no simulador (uma única alavanca) e rodar a mesma análise do baseline sobre os **mesmos** conjuntos + o hold-out.
4. Registrar resultados no próprio delta e a decisão: `ADOTADO` (vira nova versão do robô `v<N+1>` e novo baseline), `REJEITADO` ou `ADIADO`.
5. Atualizar `HIPOTESES.md` (links para o delta) e o `CHANGELOG.md` do motor.

Uma alavanca por delta; se dois efeitos se misturam, não se sabe o que funcionou.

## 7. Commits

Mensagens curtas e descritivas, um commit por mudança lógica (dados / código / análise / documentação). Relatórios regenerados entram no mesmo commit do código que os gerou.

## 8. Classificação das análises

Toda análise que entra na trilha do robô ganha uma linha em `docs/registro/analises.csv` e aparece em `docs/04_REGISTRO_ANALISES.md` (gerado por `python ferramentas/indexar_analises.py`).

- **Id:** `<motor>-A###` (`M16-A002`). O retrato do ano usa `ANO-<ano>`. Numeração não se reaproveita.
- **Classe:** `direcao`, `volatilidade`, `geometria`, `execucao`, `descritiva`, `econofisica` ou `legado`. Uma classe principal por análise; o efeito secundário vai na nota.
- **Decisão para o robô:** `USAR`, `NAO_USAR`, `CONDICIONAL`, `PENDENTE` ou `FORA_DO_PROTOCOLO`. Quem consolida as decisões é `docs/05_TRILHA_ROBO.md`.
- Análise sem linha no registro não serve de argumento para mudar o robô.
- O ano corrente (`docs/ano_foco/`) é estudo de comportamento. Número que só aparece nesse ano não vira parâmetro.
