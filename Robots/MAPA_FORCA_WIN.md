# MAPA DE REGRAS — FORCA_WIN_V16

> Árvore de decisão por candle fechado. Para rastreamento no Figma.
> Legenda: ✅ implementado · 🔘 reservado/desligado · ⬜ pendente · 🧪 validar

---

```
CANDLE FECHADO
│
├── A. CALCULAR
│   ├── ✅ fForca = ((Close-Open)/(High-Low)) × (Volume/fVolMedia) × 100  clamped ±100
│   ├── ✅ Zona atual
│   │       ├──  2  F ≥ 85   exaustão compra
│   │       ├──  1  F 70–84  força compra
│   │       ├──  0  |F| < 70 neutro
│   │       ├── -1  F -70–84 força venda
│   │       └── -2  F ≤ -85  exaustão venda
│   ├── ✅ bCtxAlta / bCtxBaixa  (proxy 60min — iJanelaCtx=4)
│   └── ✅ bDirAlta / bDirBaixa  (proxy 30min — iJanelaDir=2)
│
├── B. PINTAR CANDLE
│   ├── ✅ Contar mudanças de zona na janela (5 candles, máx 3)
│   │       └── bAlertaInstavel = true se ≥ 3 mudanças
│   │
│   ├── ✅ Volume < fVolMedia?
│   │       └── SIM → BRANCO (sem cor de sinal)
│   │
│   ├── ✅ Volume ≥ fVolMedia → aplicar cor por zona
│   │       ├── Zona  2 → Verde forte  RGB(0,150,0)
│   │       ├── Zona  1 → Verde fraco  RGB(120,220,120)
│   │       ├── Zona  0 → Branco       RGB(255,255,255)
│   │       ├── Zona -1 → Verm. fraco  RGB(255,120,120)
│   │       └── Zona -2 → Verm. forte  RGB(180,0,0)
│   │
│   └── ✅ bAlertaInstavel? (override sobre qualquer cor)
│           ├── Zona > 0 → Cyano  RGB(0,220,220)
│           ├── Zona < 0 → Fúcsia RGB(255,0,180)
│           └── Zona = 0 → mantém branco
│
├── C. STOP HORÁRIO
│   └── ✅ Hora ≥ 17:45 → FECHAR POSIÇÃO + bloquear novas entradas
│
├── D. EM POSIÇÃO?
│   │
│   ├── NÃO → ir para bloco E (entradas)
│   │
│   └── SIM → iBarras++
│       │
│       ├── D1. MAX BARRAS
│       │       └── ✅ iBarras ≥ 6 → FECHAR
│       │
│       ├── D2. HARD SL INTRABAR
│       │       ├── ✅ Comprado: Low  ≤ fEntrada − 150 → FECHAR
│       │       └── ✅ Vendido:  High ≥ fEntrada + 150 → FECHAR
│       │
│       ├── D3. STOP CANDLE CONTRA
│       │       ├── ✅ Comprado: fForca ≤ −70 → FECHAR
│       │       └── ✅ Vendido:  fForca ≥  70 → FECHAR
│       │
│       ├── D4. ARMAR BREAK-EVEN (bBreakEven)
│       │       ├── ✅ Cor oposta aparece → bBreakEven = true
│       │       ├── ✅ 5 brancos consecutivos → bBreakEven = true
│       │       └── ✅ Lucro ≥ fTPAtivo × 0.333 → bBreakEven = true
│       │               ├── Zona ±2 (100pts): BE arma em ~33pts
│       │               └── Zona ±1  (50pts): BE arma em ~17pts
│       │
│       ├── D5. EXECUTAR BREAK-EVEN
│       │       └── ✅ bBreakEven = true AND Close voltou à entrada → FECHAR
│       │
│       ├── D6. TRAILING (somente iZonaEntrada = ±2)
│       │       ├── ✅ Pré-condição: bBreakEven = true
│       │       ├── ✅ fPassoTrail = (fTPAtivo − lucro) × 0.62
│       │       │       └── mínimo: fTPAtivo × 0.10
│       │       └── ✅ Low/High cruza fTrailingRef → FECHAR
│       │
│       └── D7. TAKE PROFIT HARD
│               ├── ✅ Zona ±2: High/Low alcança fEntrada ± 100pts → FECHAR
│               └── ✅ Zona ±1: High/Low alcança fEntrada ±  50pts → FECHAR
│
└── E. FORA DE POSIÇÃO — VERIFICAR ENTRADA
    │
    ├── E1. COMPRA
    │       ├── ✅ fForca ≥ 70  AND  fForca[1] < 70   (1º candle de força)
    │       ├── ✅ bCtxAlta AND bDirAlta               (MTF alinhado)
    │       ├── ✅ Volume ≥ 5000                        (filtro absoluto)
    │       └── ENTRAR
    │               ├── ✅ Zona  2 → fTPAtivo = 100pts · trailing ativo após BE
    │               └── ✅ Zona  1 → fTPAtivo =  50pts · apenas BE, sem trailing
    │
    └── E2. VENDA
            ├── ✅ fForca ≤ −70  AND  fForca[1] > −70  (1º candle de força)
            ├── ✅ bCtxBaixa AND bDirBaixa              (MTF alinhado)
            ├── ✅ Volume ≥ 5000                         (filtro absoluto)
            └── ENTRAR
                    ├── ✅ Zona −2 → fTPAtivo = 100pts · trailing ativo após BE
                    └── ✅ Zona −1 → fTPAtivo =  50pts · apenas BE, sem trailing


BACKLOG
    ├── ⬜ Backtest com TP dinâmico por zona
    ├── 🧪 Validar RR: SL=150 vs TP=100/50 — winrate mínimo necessário ~60–75%
    ├── ⬜ Guard fTPAtivo > 0 no cálculo de BE (I03 do RAID)
    └── 🔘 UsarAlertaMudancaTardia — reservado para ativação futura
```

---

## COMO USAR NO FIGMA

1. Cada nó vira um **card** (sticky note ou shape)
2. Cor dos cards por status:
   - ✅ **Verde** — implementado e em uso
   - 🔘 **Cinza** — reservado, código existe mas desligado
   - ⬜ **Amarelo** — pendente / backlog
   - 🧪 **Laranja** — implementado mas aguarda validação
3. Blocos A–E viram **frames/swimlanes** em sequência horizontal (esquerda → direita)
4. Bloco D é vertical com sub-decisões em cascata (de cima para baixo = ordem de prioridade)
5. Ao concluir/validar um item: deletar o card ou mover para frame "CONCLUÍDO"
