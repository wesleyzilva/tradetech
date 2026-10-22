# M16 — Confluência de cor em múltiplos timeframes (alerta sonoro)

| Campo | Valor |
|---|---|
| Status | ATIVO — ANALISE_001 concluída: **sem vantagem direcional demonstrável**; alerta útil só como atenção |
| Instrumentos / timeframes | WIN (replicação em WDO); base 5, 15 e 30 min; superiores 15/30/60 min |
| Tese | A **mesma cor** (família e nível do M01) em mais de um timeframe ao mesmo tempo é um sinal mais confiável; o operador recebe um **alarme sonoro** e decide a entrada |
| Perguntas do operador | quantos pontos? qual estratégia? qual a probabilidade? qual o melhor risco/retorno? |
| Método | [`METODO.md`](METODO.md) · Hipóteses: [`HIPOTESES.md`](HIPOTESES.md) |
| Análise | [`analises/ANALISE_001_confluencia.md`](analises/ANALISE_001_confluencia.md) |
| Código | `codigo/cf_motor.py` (eventos, execução, estatística) · `codigo/analise_001.py` (gera o relatório) |

## Resultado em uma tela

- **Frequência:** a confluência é rara. Modo A (barras fecham juntas), nível colorido: 5+15 ≈ 0,4 alerta/pregão; 15+30 ≈ 0,8; 30+60 ≈ 0,5; três TFs ≈ 0,01–0,2. No nível brilhante quase não ocorre em 2+ TFs.
- **Pontos:** em 60 min após o alerta, a mediana do máximo favorável (MFE) é ~320 pts (5+15), ~450 (15+30) e ~420 (30+60) no WIN, e o máximo adverso (MAE) é praticamente igual. Em ~47 % a 53 % dos eventos o MFE supera o MAE: **é amplitude, não direção**.
- **Estratégias:** 0 de 114 combinações (continuação ou fade; 3 geometrias de stop e alvo) passam o critério com hold-out e replicação.
- **O que fica:** o alerta serve como atenção (amplitude esperada acima do normal em TFs altos); a entrada continua precisando de outro critério com evidência.

## Alinhamento no mesmo instante (ANALISE_002)

Testa o que se vê no gráfico: no minuto em que a barra do TF maior fecha, os TFs menores estão com a mesma cor, inclusive com os limiares fixos do robô (|F| ≥ 60 e |F| ≥ 80).

- **CF-H07 refutada.** O melhor caso (30+60, saturação) dá +50 pts em 60 min até 2019 (t = 2,6; acerta 53%) e −43 pts em 2020–2025. Nos conjuntos com 5 min, |t| < 1,6.
- **CF-H08 refutada.** O alinhamento não supera a cor do TF maior sozinho: a diferença troca de sinal entre os períodos.
- **CF-H09 refutada.** Limiar fixo e Bollinger dão o mesmo sinal; o limiar só multiplica a frequência por 2 a 6.
- MFE e MAE em 60 min continuam empatados (48% a 53% a favor da cor).

A leitura de por que o gráfico engana está na seção 7 de `analises/ANALISE_002_alinhamento.md`. O mapa de econofísica (o que já foi medido, o que falta, e o que sustenta um mestrado) está em `ECONOFISICA.md`.

## Como rodar

```bash
python3 motores/M16_confluencia_multitf/codigo/analise_001.py   # ~30 s
python3 motores/M16_confluencia_multitf/codigo/analise_002.py   # alinhamento no mesmo instante, ~10 s
```
