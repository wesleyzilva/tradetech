---
applyTo: "Robots/**,Robots/Results/**,CandlesHistoryDatas/**,README.md"
description: "Use when: analyzing Tradetech WIN scalper robots, Profit simulator CSVs, backtests, timeframe choice, risk/reward, probability of success, stop behavior, or NTSL execution parameters."
---

# Tradetech WIN Scalper Instructions

Use estas instrucoes sempre que analisar, editar ou documentar robos WIN scalper, resultados do simulador Profit, backtests locais ou decisao de parametros operacionais neste repositorio.

## Estrutura oficial de trabalho

- Versao viva do robo principal: `Robots/FORCA_WIN_V16_scalper_sinaisForca/FORCA_WIN_V16_scalper_sinaisForca`.
- Arquivos antigos na raiz de `Robots/` podem existir como historico; ao trabalhar no scalper principal, priorizar sempre a versao viva acima.
- Resultados do simulador ficam em: `Robots/Results/FORCA_WIN_V16_scalper_sinaisForca/`.
- Cada rodada de teste deve ficar em uma pasta numerada sequencialmente: `1/`, `2/`, `3/`, etc.
- Dentro de cada pasta numerada, manter:
  - backup/snapshot do codigo usado na rodada com data e horario, exemplo `FORCA_WIN_V16_scalper_sinaisForca_20260612_0846`;
  - CSVs exportados pelo Profit para cada timeframe testado, exemplo `FORCA_WIN_V16_scalper_sinaisForca_5.csv`.
- Ao comparar resultados, tratar cada pasta numerada como uma versao fechada de experimento.
- Antes de analisar uma pasta numerada, confirmar qual snapshot de codigo existe dentro dela e citar a pasta/rodada, nao apenas o nome do CSV.
- Nunca misturar CSVs de uma rodada com codigo de outra ao concluir sobre probabilidade, RR ou risco real.

## Decisao operacional atual

- Robo principal: `Robots/FORCA_WIN_V16_scalper_sinaisForca/FORCA_WIN_V16_scalper_sinaisForca`.
- Timeframe principal para operacao: **WIN 5min**.
- Timeframes `1min` e `2min`: nao priorizar para operacao; muito ruido e resultados recentes negativos/fracos.
- Timeframe `20min`: tratar como estudo separado/promissor, nao substituir o foco 5min sem novo backtest e replay dedicado.
- Timeframes `30min`, `45min` e `60min`: nao promover como foco sem evidencia nova; resultados recentes perderam consistencia no comparativo.
- `Robots/FORCA_WIN_V16_scalpercurto`: tratar como setup tatico de replay/estudo, 1 contrato, nao como robo principal.

## Parametros padrao do 5min

- `ForcaMinimaForte(70.0)`.
- `ForcaExaustao(85.0)`.
- `ForcaAlerta(55.0)` apenas visual por padrao.
- `PeriodoMediaVolume(20)`.
- `UsarFiltroVolume(true)`.
- `StopMinimo(280.0)` como gatilho de stop.
- `UsarOrdensProtecaoReal(true)`.
- `OffsetStopReal(30.0)`.
- Risco real planejado: **310 pts** por contrato.
- `TakeProfitNivel2(560.0)` para zona forte `70-85`, RR real aproximado `560 / 310 = 1.81`.
- `TakeProfitNivel3(840.0)` para exaustao `>=85`, RR real aproximado `840 / 310 = 2.71`.
- `UsarBreakEven(false)`.
- `UsarTrailingProporcional(false)`.
- `UsarBEPorCorOposta(false)`.
- `CandlesBrancosParaBE(0)`.
- `UsarStopCandleContra(false)`.
- `PermitirReversao(false)`.
- `BloquearReentradaMesmoCandle(true)`.
- `MaxBarrasEmPosicao(12)`.
- Stop horario: `17:45`; em NTSL/Profit, tratar `Time()` como **HHMM** (`1745`), nao HHMMSS (`174500`).
- `MaxContratos(3)`, mas quantidade ainda deve ser configurada no Profit enquanto `BuyAtMarket(iQtd)` nao estiver validado.

## Checklist obrigatorio ao analisar resultados

Ao analisar CSVs exportados pelo Profit:

- Ler CSV com separador `;` e encoding compativel com export latino (`latin-1` costuma funcionar).
- Usar `Res. Operacao (%)` como pontos e `Res. Operacao` como resultado financeiro.
- Nao reproduzir dados pessoais do export, como conta, titular ou identificadores de corretora.
- Comparar versoes em duas visoes:
  - periodo completo de cada pasta;
  - periodo comum entre as pastas, para evitar conclusao enviesada por janela diferente.
- Calcular no minimo:
  - quantidade de trades;
  - PnL em pontos e em reais;
  - win rate;
  - profit factor;
  - media por trade;
  - ganho medio;
  - perda media;
  - payoff/RR realizado = `ganho_medio / abs(perda_media)`;
  - probabilidade minima de breakeven = `1 / (1 + RR)`;
  - edge estatistico = `win_rate - breakeven_rate`;
  - max drawdown em pontos;
  - maior perda;
  - percentual de perdas `< -310 pts`;
  - percentual de perdas `< -560 pts`;
  - percentual de ganhos `>= 560 pts`;
  - percentual de ganhos `>= 840 pts`;
  - dias positivos versus negativos;
  - maior sequencia de perdas.

## Bloqueadores de conclusao

Antes de dizer que o caminho esta correto, verificar:

- Se existe trade abrindo depois de `17:45`.
- Se existe trade fechando em outro dia ou carregando overnight.
- Se existem muitas perdas abaixo de `-310 pts`.
- Se existe perda extrema abaixo de `-560 pts`.
- Se o resultado positivo depende de poucos outliers de ganho.

Se qualquer item acima aparecer, classificar a conclusao como provisoria e priorizar correcao/novo replay antes de recomendar operacao real.

## Criterios para dizer que estamos no caminho certo

Para o **5min** ser considerado operacionalmente promissor, procurar:

- PnL positivo em pontos e em reais.
- `Profit Factor >= 1.10` como minimo; ideal `>= 1.20`.
- Edge estatistico `>= 2 pp` acima da probabilidade minima de breakeven.
- Drawdown menor que a versao anterior.
- Perdas `< -310 pts` proximas de zero apos ajuste de stop real.
- Nenhuma posicao carregada overnight.
- Ganhos `>= 560 pts` suficientes para pagar a massa de stops.
- Resultado nao concentrado em poucos dias ou poucos trades.

Se o resultado estiver positivo mas com `PF < 1.10` ou edge menor que `2 pp`, chamar de **promissor, mas ainda fragil**.

## Formato recomendado de resposta

Ao responder uma analise, estruturar assim:

1. Recomendacao direta: operar, estudar, ajustar ou descartar.
2. Timeframe recomendado e parametros.
3. Tabela comparativa das versoes/pastas.
4. Probabilidade de sucesso: win rate, breakeven rate e edge.
5. RR realizado e RR planejado.
6. Risco real: max loss, perdas abaixo de `-310`, overnight e after-hours.
7. Conclusao: se o caminho esta correto, provisoriamente correto ou bloqueado.
8. Proximo teste necessario no simulador.

## Ao editar codigo

- Preservar mudancas nao relacionadas do usuario.
- Nao reverter delecoes ou arquivos fora do escopo sem pedido explicito.
- Depois de editar `Robots/**` ou `README.md`, validar com `get_errors` e `git diff --check`.
- Nao commitar nem fazer push sem pedido explicito.