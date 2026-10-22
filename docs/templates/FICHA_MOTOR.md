# M## — <nome do motor>

| Campo | Valor |
|---|---|
| Status | CANDIDATO \| ATIVO \| EM PAUSA \| ARQUIVADO |
| Instrumentos / timeframes | |
| Tese (1 parágrafo) | |
| Sinal | definição operacional |
| Gestão de saída | |
| Robô vigente | `robo/…` |
| Simulador | `codigo/…` (+ testes em `tests/`) |
| Baseline | `analises/ANALISE_001_…` |
| Veredito vigente | |

## Como reproduzir
```bash
python motores/<motor>/codigo/analise_001.py
python -m unittest tests.<teste>
```

## Mapa do motor
- `HIPOTESES.md` — registro e vereditos
- `METODO.md` — convenções da simulação
- `deltas/` — mudanças propostas/decididas
- `CHANGELOG.md` — versões do robô

## Dados necessários e lacunas
