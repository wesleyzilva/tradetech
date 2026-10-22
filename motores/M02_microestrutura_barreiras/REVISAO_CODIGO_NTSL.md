# M02 — Revisão do código NTSL (v1, 2026-10-22)

Arquivo: [`robo/Robo_Microestrutura_Barreiras_v1_20261022.ntsl`](robo/Robo_Microestrutura_Barreiras_v1_20261022.ntsl). Formato RAID (Riscos · Premissas · Problemas · Decisões). Cada item aponta para a hipótese/delta que o trata.

## O que o código faz bem

- Estrutura clara em 7 blocos (janelas → ATR/stops → estados → cores → zeramento → gestão → entrada).
- Parâmetros nomeados no cabeçalho, zeramento de fim de pregão e janelas bloqueando o almoço.
- Prioridade explícita entre contextos e entrada **só sem posição** (sem pirâmide nem reversão acidental).
- Pisos de stop/alvo e barreira de tempo previnem distâncias degeneradas.
- Cores informam o estado — útil para inspeção visual contra os cálculos do Python.

## Problemas (I)

| ID | Linha/bloco | Problema | Impacto medido | Tratamento |
|---|---|---|---|---|
| I01 | §6 gestão | Stop e alvo só são enviados **depois** da barra de entrada (a posição já existe no fechamento da barra seguinte à ordem). A barra de entrada fica sem proteção. | perfil fiel × ideal: −6,2 × −3,9 pts/trade (WINFUT 1 min); pior trade −1.017 × −165 | `DELTA_001`, `MB-H05` |
| I02 | §6 `SellToCoverStop(vStop, vStop − OffsetTicks)` | Stop-**limit** com limite a 5 pts do gatilho. Se o mercado atravessa o limite antes da ordem existir, ela fica passiva e só executa se o preço **voltar**; o trade passa a depender da barreira de tempo. `OffsetTicks` é descrito como "ticks" mas está em **pontos** (5 pts = 1 tick do WIN). | 462 trades (15,4 %) com stop passivo; média −107 pts/trade, pior −1.585 | `DELTA_001`, `MB-H05` |
| I03 | §6 | Alvo/stop são **recalculados a cada barra** com o ATR corrente: o alvo pode andar para longe/perto sem o preço se mover. Com `BuyPrice` fixo, o risco efetivo varia ao longo do trade. | não medido isoladamente | novo delta: fixar SL/SG no ATR do sinal |
| I04 | §2 | Piso de SL de 35 pts: em 1 min o ATR mediano é ~98 pts (SL nominal 48), então o piso vale em 32 % dos trades; MAE ≥ SL em 83 % dos trades. Stop dentro do ruído ⇒ 64 % das saídas são SL. | WR 19–21 % ≈ breakeven 21 % | `MB-H03` |
| I05 | §7 | Frequência: ~30 trades por pregão. Sem limite diário, cooldown ou filtro de custo. | custo de 2–5 pts/trade supera qualquer margem | `DELTA_002`, `MB-H07` |
| I06 | §3 | ATR calculado **incluindo a barra atual**: a barra grande infla o próprio limiar e é subclassificada (mesmo efeito do M01-H15). | não medido | `MB-H11` |
| I07 | §7 ctx 1/2 | Fade exige que a barra **seguinte** feche além da mín/máx da brilhante. Na prática quase nunca ocorre (18 + 28 sinais contra 5.532 do ctx 3 em 99 pregões). O robô é, na prática, um rompedor de fluxo neutro. | 99,2 % dos sinais são ctx 3 | `MB-H01`, `MB-H02` |
| I08 | §7 ctx 3 | O rompimento de barra neutra (< 1,3 × ATR) com SMA20 não tem continuação direcional medida. | retorno alinhado ≈ 0, |t| ≤ 1,6 (WINFUT 1 min) | `MB-H02` (REFUTADA) |
| I09 | §5/§6 | `ClosePosition` na barreira de tempo/zeramento: ordens de alvo/stop enviadas na barra anterior podem continuar pendentes no livro (depende da implementação do Profit) e abrir posição oposta. | não testável sem o Profit | verificar no Profit; cancelar ordens pendentes antes de `ClosePosition` |
| I10 | geral | O NTSL pode avaliar a lógica **a cada tick** da barra em formação; o desenho do estudo (e a réplica) assume avaliação no fechamento. Sinais que "piscam" intrabarra podem entrar em barras que depois não confirmam. | desconhecido | `MB-H12` (paridade) |

## Riscos (R)

| ID | Risco | Mitigação sugerida |
|---|---|---|
| R01 | Sem limite de perda diário nem de nº de trades | contador de trades e `PerdaDiariaMax` em pontos |
| R02 | Quantidade fixa/implícita; `BuyAtMarket` sem quantidade | parametrizar `Qtd` |
| R03 | Rolagem de contrato (vencimento do WIN) | bloquear 2 dias antes do vencimento ou rolar manualmente |
| R04 | Leilão/abertura: ATR calculado com barras do dia anterior no início do pregão | iniciar apenas após N barras do dia |
| R05 | Parâmetros descritos nos comentários não são usados: `PeriodoATR` ok, mas SMA fixa em 20 (`Media(20, Close)`), `HoraConsolFim` só para cor | transformar em parâmetros |
| R06 | Horário do zeramento (17:20) após o fechamento do WIN regular em certas datas (horário de verão dos EUA) | checar calendário B3 |

## Premissas (A)

| ID | Premissa | Como validar |
|---|---|---|
| A01 | `Time` é HHMM e se refere ao horário da barra (abertura) | comparar cores no Profit com `est` do Python em timestamps exatos |
| A02 | `AvgTrueRange(20, 0)` = média simples de 20 TR incluindo a barra atual | idem |
| A03 | Ordens a mercado enviadas no fechamento executam na abertura seguinte | trade log do Profit |
| A04 | `BuyPrice`/`SellPrice` = preço médio de entrada | trade log do Profit |

## Decisões vigentes (D)

| ID | Decisão (herdada do v1) | Estado |
|---|---|---|
| D01 | Barreira tripla assimétrica SL 0,5 × ATR / SG 2,5 × ATR / 20 barras | mantida até haver evidência de edge no sinal |
| D02 | Janelas 09:15–12:00 e 14:00–16:15 | mantida; `MB-H06` pendente |
| D03 | Zeramento às 17:20 | mantida |
| D04 | Estados 1,3 / 1,7 × ATR | mantida; `MB-H11` pendente |

## Recomendação de evolução (ordem)

1. **Medir paridade** (`MB-H12`) com um export do Profit — destrava todo o resto.
2. **Não mexer no sinal ainda**: o sinal ctx 3 não tem edge detectável; mexer em limiares seria *data mining* com 99 pregões.
3. Deltas de **execução** (stop a mercado, SL/SG fixados no ATR do sinal, cooldown) reduzem risco de cauda e custo e não dependem de ter edge.
4. Reaproveitar o **estado brilhante** como alerta de volatilidade (M01 H20) em vez de fade; testar em dados novos (`MB-H13`).
5. Só depois de ≥ 300 pregões de 1 min: varredura de parâmetros com hold-out e contagem de combinações.
