# Instruções de Agente para Detecção de Padrões em Dados de Candles

## 1) Objetivo principal
- A partir dos dados desta pasta, que contém informações de abertura, fechamento, máxima e mínima de candles em vários timeframes, o agente deve detectar e criar áreas de comportamento relevantes.
- Essas áreas serão geradas com base em outra especificação (arquivo de instruções secundário a ser implementado depois).

## 2) Contexto do dataset
- Local: `WESQUAD/DadosCandlesBacktest/`
- Campos esperados: opens, closes, highs, lows, timestamps, timeframe (diário, intradiário, etc.)
- Meta: estruturar e priorizar zonas de suporte/resistência ou de fluxo onde padrões se repetem.

## 3) Regras de geração de áreas
- O objetivo principal aqui é gerar áreas retangulares com base nas máximas e mínimas de candles.
- Para cada candle relevante:
  - `x` será a distância definida em pontos (e.g., 100); deve ser parametrizável no sistema como `x_pontos` ou `sg_sl_offset`.
  - Para área de máxima:
    - lado vertical começa em `high` e vai até `high + x`.
    - lado horizontal começa no candle atual (tempo `t`) e se estende `3` candles à direita (para frente no tempo) no mesmo timeframe.
  - Para área de mínima:
    - lado vertical começa em `low` e vai até `low - x`.
    - lado horizontal começa no candle atual (tempo `t`) e se estende `3` candles à direita (para frente no tempo).
- Parâmetros de ajustes:
  - `x_pontos`: quantidade de pontos utilizada para gerar área de SG (stop gain) e SL (stop loss) em torno das máximas/mínimas.
  - `sl_minimo`: menor distância de SL desejada (em pontos) para não ficar muito apertado.
  - `sg_minimo`: menor distância de SG desejada (em pontos) para garantir objetivo mínimo de lucro.
  - `timeframe_step`: duração de candle no timeframe usado para cálculo de extensão horizontal, usado em conjunto com 3 candles.
- Estas áreas são retângulos alinhados com eixos (sem rotação) definidos por (x0, y0) a (x0+3*timeframe_step, y1).
- As áreas devem ser geradas no mesmo timeframe que está sendo analisado; a validação em timeframes adjacentes fica como verificação adicional.
- Continuar reportando métricas de teste como número de toques, rejeições, e confluências multi-timeframe.

## 4) Entrega esperada
- Saída inicial: lista ordenada de áreas com descrição de critério e referências temporais.
- Formato sugerido: JSON ou Markdown tabelado (exemplo abaixo).

Exemplo de output:
```json
[
  {
    "area_id": "A1",
    "timeframes": ["15m", "1h"],
    "low": 1234.5,
    "high": 1241.2,
    "pontos_de_teste": 8,
    "notas": "Zona de resistência multi-timeframe detectada em x\n"
  }
]
```

## 5) Comportamento de processo
- Trabalhar em iterações curtas: identificar áreas, revisar com base em feedback e depois refiná-las.
- Registrar suposições, parâmetros e decisões usadas para gerar cada área.

## 6) Critérios de qualidade
- Reprodutibilidade: mesma entrada deve gerar áreas semelhantes em runs iguais.
- Transparência: parâmetros de threshold devem estar documentados.
- Flexibilidade: permitir ajuste das regras em arquivo de configuração/sinopse.

## 7) Análise Multi-timeframe e Prioridade de Timeframes
- Two-step analysis:
  - Contexto (análise estrutural e informacional): Semanal > Diário > 60m.
  - Operacional (sinergia intraday para execução): 60m > 30m > 15m (com inspeção extra em 5m e 2m para afinamento segundo disponibilidade).
- Prioridade de análise (peso maior para timeframe maior no contexto): Semanal > Diário > 60m > 30m > 15m > 5m > 2m.
- Processo:
  1. Contexto: Identificar áreas estruturais no timeframe maior disponível (p.ex., Semanal, Diário, 60m). Essas áreas são de fundo e definem os limites de referência.
  2. Operacional: Dentro do mesmo período (janela temporal) das áreas de contexto, construir a sinergia usando 60m/30m/15m para gerar suportes/resistências intraday, com 5m/2m como refinamento.
  3. Buscar zonas de suporte/resistência intradiária em 60m, 30m, 15m e marcar linhas horizontais conforme toques múltiplos, reversões e proximidade à área de contexto.
  4. Usar as áreas de contexto para validar, filtrar e priorizar setups operacionais (alarmar rejeições/rompimentos dentro da zona maior).
- Regras de harmonização:
  - Se uma área maior já contém a faixa de preço, só valida nos menores e marca as linhas instantaneamente como confluência.
  - Se área menor extrapola/passa fora da área maior, classificar como contrária ou rompimento potencial com menor peso.
  - Se a zona imediatamente acima ou abaixo não apresentar convergência (não houver confluência de timeframes maiores ou força de candles), considere a área como zona de não operação.
- Zonas de gatilho (fase preparatória, ainda não ordem):
  - Zona de gatilho = sobreposição de áreas de suporte/resistência dos 3 últimos candles analisados no timeframe operacional (60m/30m/15m).
  - Calcule para cada nível candidato quantas vezes os 3 candles intersectam o preço ou a faixa (open/high/low/close) no mesmo lado.
  - Densidade: quanto mais níveis sobrepostos (e quanto mais próximos), maior a força potencial da zona de gatilho.
  - Classificação simples de força:
    - fraca: 1-2 candles em sobreposição baixa ou espaçada;
    - média: 2-3 candles com sobreposição consistente e janela de preço estreita;
    - alta: 3 candles sobrepostos com alcance próximo (e.g., <5% do range total) + confluência de contexto (área maior).
  - Marcar zona de gatilho com atributos:
    - `tf`: timeframe de análise (60m/30m/15m),
    - `price_range`: [preço_inferior, preço_superior],
    - `density_score`: valor numérico (ex. de 0 a 100) da sobreposição;
    - `strength`: fraca/média/alta,
    - `context_overlap`: booleano se dentro da área de contexto superior (Semanal/Diário/60m).
- A zona de gatilho ainda não é o gatilho de execução, é sinal de maior atenção e validação futura.
- Inclua as métricas:
  - número de toques no nível,
  - direção predominante (baixa/alta),
  - tempo de duração na zona,
  - volume relativo por candle, se disponível.

## 8) Marcação de linhas no gráfico
- Linha principal (nível estrutural): preço no centro da área maior identificada.
- Linha secundária (intraday): níveis ativos em 30, 15, 5 que cruzam com o espaço temporal de cada área maior.
- Linha de confirmação: quando 3+ toques são detectados no nível em timeframe menor dentro da janela de 3 candles a frente no timeframe de origem, marcar como confirmação.

## 9) Refinamento de gatilho em 15m/5m/2m com Força de Candle (F=M*A)
- Objetivo: após definir zonas de gatilho (sobreposição 3 candles), refinamos o potencial em timeframes menores.
- Regra de força do robô `FORCA_SEMAFORO_CORES_55.ntfl`:
  - `fCorpo = Close - Open`
  - `fRange = max(High - Low, 0.0001)`
  - `fVolMedia = max(Media(PeriodoMediaVolume, Volume), 1)`
  - `fMassa = fCorpo / fRange`
  - `fAceleracao = Volume / fVolMedia`
  - `fForca = fMassa * fAceleracao * 100` (limitado a [-100, 100])
- Para candles de 15m/5m/2m dentro de zonas de gatilho:
  - calcule `fForca`; se `fForca >= 55` ou `fForca <= -55`, marque como validação de força para potencial gatilho.
  - não execute ordem automaticamente; use este valor para incrementar o `density_score` e `strength` da zona.
  - gatilho operacional futuro será acionado quando: (a) zona de gatilho alta/média + (b) ao menos 1 candle 5m/2m com `|fForca| >= 55` + (c) confirmação de rompimento/rejeição (definir em regra posterior).
- Refino de zona:
  - 5m e 2m fornecem contatos diretos no range da zona (tocar/romper/fechar dentro).
  - conte quantos desses candles tocam a faixa: 0-2 (baixo), 3-5 (médio), >5 (alto) em janela 3-5 candles.
  - combine com `fForca` para classificar o “pré-gatilho” (ex: `pre_trigger_score = density_score * 0.6 + forca_score * 0.4`).
  - gatilho efetivo é sempre em 2m: a execução futura deve ser condicionada à confirmação no candle de 2 minutos após a zona de pré-gatilho.

## 10) Objetivo do projeto e validação de assertividade
- O objetivo principal é verificar a assertividade da técnica, priorizando qualidade sobre quantidade de operações:
  - operar com menos setups por dia, focando em entradas de alto valor provável (confluência forte e F>=55/-55 em 2m).
  - medir ganhos em horizontes curtos (5 a 10 minutos) após a identificação de zona de gatilho.
  - calcular quantos pontos foram possíveis capturar ('points capture') dentro desse intervalo.
  - garantir SL o menor possível (mínimo `sl_minimo`) e R/R atrativo, com risco controlado.
  - evitar overtrading: rejeitar setups com confluência média/baixa e depth de zona acima/abaixo sem convergência.
  - operar sempre a favor do movimento com maior probabilidade de sucesso, usando o fluxo contexto → operacional → gatilho.
- Métricas de sucesso:
  - Taxa de acerto (win rate) em 5m/2m após confirmação de gatilho.
  - Reward/Risk médio em operações concluídas (pontos ganhos vs SL). 
  - drawdown máximo em série de perdas. 
  - consistência de `density_score` e `fForca` com resultados positivos.
  - tempo de execução: 5-10 min de observação pós-setup.

## 11) Próximos passos
- Criar o segundo arquivo de instruções detalhando o algoritmo de criação de áreas e parâmetros exatos.
- Adicionar casos de teste (sintéticos e reais) no mesmo diretório para validação.

