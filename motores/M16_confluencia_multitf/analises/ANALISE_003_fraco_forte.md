# ANALISE_003 — Lado pela tabela fraco/forte (5 min × 15 min)

> Gerado por `codigo/analise_003.py`. Faixas e critério em `HIPOTESES.md` (CF-H10, CF-H11), congelados antes de rodar.

Fraco = 70 ≤ |F| < 85. Forte = |F| ≥ 85. Lado = sinal de F. O número é o retorno de 60 min a favor desse lado, em pontos. `p` é a fração de eventos em que o lado acertou. Descoberta = WIN até 2025-06-30. Hold-out 1 = WIN de 2025-07 a 2025-12. 2026 = contratos M26 e Q26.

No guia operacional, fraco se chama "forte" (F 70–85) e forte se chama "exaustão" (F ≥ 85). Os cortes são os mesmos.

| combinação | descoberta | hold-out 1 | 2026 | WDO |
|---|---|---|---|---|
| 5 fraco, 15 branco | -21 pts · t=-0,7 · p=41% · n=251 | -21 pts · t=-0,5 · p=46% · n=89 | -50 pts (n=41) | 1 pts · t=1,0 · p=51% · n=296 |
| 5 forte, 15 branco | -7 pts · t=-0,3 · p=50% · n=356 | 2 pts · t=0,0 · p=49% · n=173 | 4 pts (n=58) | 1 pts · t=1,3 · p=48% · n=504 |
| 5 fraco × 15 fraco | 53 pts · t=0,4 · p=52% · n=21 | 162 pts · t=1,1 · p=55% · n=11 | — | 2 pts · t=0,6 · p=52% · n=42 |
| 5 fraco × 15 forte | -79 pts · t=-1,7 · p=48% · n=117 | 105 pts · t=1,5 · p=59% · n=51 | 228 pts (n=18) | -2 pts · t=-1,4 · p=45% · n=151 |
| 5 forte × 15 fraco | -118 pts · t=-1,2 · p=41% · n=41 | -19 pts · t=-0,1 · p=60% · n=20 | -378 pts (n=4) | 0 pts · t=0,0 · p=43% · n=69 |
| 5 forte × 15 forte | -3 pts · t=-0,1 · p=52% · n=452 | 37 pts · t=1,1 · p=51% · n=221 | -66 pts (n=78) | 1 pts · t=0,8 · p=50% · n=745 |
| 5 colorido × 15 oposto | 71 pts · t=1,5 · p=61% · n=105 | 45 pts · t=0,6 · p=57% · n=53 | -133 pts (n=20) | -1 pts · t=-0,3 · p=49% · n=154 |

**CF-H10:** nenhuma das 4 combinações do mesmo lado passa.

**CF-H11:** a história fraco-continua / forte-reverte não se sustenta.

Quatro células foram testadas. Uma delas pode passar de |t| = 2 por acaso; por isso o critério exige o mesmo sinal no hold-out.

