# M18 — Estrutura intradiária (momentum do dia, faixas, dia da semana, gap, faixa de abertura)

| Campo | Valor |
|---|---|
| Status | ATIVO — ANALISE_001 concluída: **sem direção sustentada em 35 testes** |
| Instrumentos / timeframes | WINFUT (decide) e WDOFUT (replica), 30 min, 2014–2025 |
| Tese | Sinais de um trade por pregão têm margem sobre o custo muito maior que os de 30 e 60 min do M17; se a estrutura do pregão tem direção, ela aparece aqui |
| Reúne | candidatos M03 (abertura), M04 (sazonalidade), M07 (momentum da primeira hora) do catálogo |
| Método | [`METODO.md`](METODO.md) · Hipóteses: [`HIPOTESES.md`](HIPOTESES.md) (ID-H01 a ID-H05) |
| Análise | [`analises/ANALISE_001_estrutura_intradiaria.md`](analises/ANALISE_001_estrutura_intradiaria.md) |
| Código | `codigo/id_motor.py` (células e estatísticas) · `codigo/analise_001.py` |

## Resultado em uma tela

- **Momentum do dia (ID-H01), dia da semana (ID-H03), gap (ID-H04) e faixa de abertura (ID-H05): refutadas.** Maior `|t|` de 1,0 a 2,7 na descoberta; acerto entre 42% e 55%.
- **Sazonalidade por faixa (ID-H02): inconclusiva.** A faixa 09:30 do WIN rende +2,2 pb acima da média do dia (t = 3,45, 53% de acerto, 10 de 12 anos), mas no hold-out cai para t = 1,63, some em 2022–2025 e o WDO tem sinal oposto.
- **O gap continua, não é desfeito** no WIN (−13 pb até 10:00 nos gaps ≥ 0,5 ATRd, 10 de 12 anos, t = −2,7); no WDO é o contrário. Abaixo do limiar, sem veredito de achado.
- Só 1 célula em 35 passa `|t| ≥ 3` na descoberta, contra 0,1 esperada por acaso, e nenhuma replica.

## Reprodução por ano

`ANALISE_001_por_ano.csv` e a seção 3 do relatório trazem o excedente médio de cada célula em cada ano. Quando o `WINFUT` de 2026 existir, `python3 motores/M18_estrutura_intradiaria/codigo/analise_001.py` acrescenta o ano como coluna, sem mexer nos vereditos.

## Como rodar

```bash
python3 motores/M18_estrutura_intradiaria/codigo/analise_001.py   # ~10 s
```
