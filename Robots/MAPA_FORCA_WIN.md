# MAPA DE REGRAS — FORCA_WIN_V16

> Árvore de decisão por candle fechado, sincronizada com o fonte `FORCA_WIN_V16`.
> Legenda: ✅ implementado · 🔘 reservado/desligado · ⬜ pendente · 🧪 validar

---

```
CANDLE FECHADO
│
├── A. CALCULAR
│   ├── ✅ fForca = ((Close-Open)/(High-Low)) × (Volume/fVolMedia) × 100  clamped ±100
│   ├── ✅ Zona atual
│   │       ├──  3  F ≥ 85       exaustão compra
│   │       ├──  2  F 70–84      força compra operacional
│   │       ├──  1  F 55–69      alerta compra visual, sem entrada
│   │       ├──  0  |F| < 55     neutro/branco
│   │       ├── -1  F -55–-69    alerta venda visual, sem entrada
│   │       ├── -2  F -70–-84    força venda operacional
│   │       └── -3  F ≤ -85      exaustão venda
│   ├── ✅ bCtxAlta / bCtxBaixa  (same-TF MA20 — iJanelaCtx=20)
│   └── ✅ bDirAlta / bDirBaixa  (same-TF MA5 contra MA20 — iJanelaDir=5)
│
├── B. PINTAR CANDLE
│   ├── ✅ Contar mudanças de zona em bloco de 5 candles
│   │       └── bAlertaInstavel = true se ≥ 3 mudanças antes do reset do bloco
│   │
│   ├── ✅ Aplicar cor por zona
│   │       ├── Zona  3 → Verde forte      RGB(0,150,0)
│   │       ├── Zona  2 → Verde fraco      RGB(120,220,120)
│   │       ├── Zona  1 → Verde alerta     RGB(210,255,210)
│   │       ├── Zona  0 → Branco           RGB(255,255,255)
│   │       ├── Zona -1 → Vermelho alerta  RGB(255,220,220)
│   │       ├── Zona -2 → Vermelho fraco   RGB(255,120,120)
│   │       └── Zona -3 → Vermelho forte   RGB(180,0,0)
│   │
│   └── ✅ bAlertaInstavel ou bAlertaTardio? (override sobre qualquer cor)
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
│       │       ├── ✅ Comprado: Low  ≤ fEntrada − fSLAtivo → FECHAR
│       │       └── ✅ Vendido:  High ≥ fEntrada + fSLAtivo → FECHAR
│       │               └── padrão atual: StopMinimo=75 e FatorRangeSL=0
│       │
│       ├── D3. STOP CANDLE CONTRA
│       │       ├── ✅ Comprado: fForca ≤ −70 → FECHAR
│       │       └── ✅ Vendido:  fForca ≥  70 → FECHAR
│       │
│       ├── D4. ARMAR BREAK-EVEN (bBreakEven)
│       │       ├── ✅ Cor oposta aparece → bBreakEven = true
│       │       ├── ✅ 5 brancos consecutivos → bBreakEven = true
│       │       └── ✅ Lucro ≥ TakeProfit × 0.333 → bBreakEven = true
│       │               └── TakeProfit=150 → BE arma em ~50 pts
│       │
│       ├── D5. EXECUTAR BREAK-EVEN
│       │       └── ✅ bBreakEven = true AND Close voltou à entrada → FECHAR
│       │
│       ├── D6. TRAILING PROPORCIONAL
│       │       ├── ✅ Pré-condição: bBreakEven = true
│       │       ├── ✅ fPassoTrail = (TakeProfit − lucro) × 0.62
│       │       │       └── mínimo: TakeProfit × 0.10
│       │       └── ✅ Low/High cruza fTrailingRef → FECHAR
│       │
│       └── D7. TAKE PROFIT HARD
│               └── ✅ High/Low alcança fEntrada ± TakeProfit(150) → FECHAR
│
└── E. FORA DE POSIÇÃO — VERIFICAR ENTRADA
    │
    ├── E1. COMPRA
    │       ├── ✅ fForca ≥ 70  AND  fForca[1] < 70   (1º candle de força)
    │       ├── ✅ bCtxAlta AND bDirAlta               (MA20 subindo + MA5 acima da MA20)
    │       ├── ✅ Volume ≥ 5000                        (filtro absoluto, se ligado)
    │       └── ENTRAR LONG com fEntrada=Close, fSLAtivo=fSL, fTrailingRef=Close−fSL
    │
    └── E2. VENDA
            ├── ✅ fForca ≤ −70  AND  fForca[1] > −70  (1º candle de força)
            ├── ✅ bCtxBaixa AND bDirBaixa              (MA20 caindo + MA5 abaixo da MA20)
            ├── ✅ Volume ≥ 5000                         (filtro absoluto, se ligado)
            └── ENTRAR SHORT com fEntrada=Close, fSLAtivo=fSL, fTrailingRef=Close+fSL


BACKLOG
    ├── ⬜ Backtest V16 vs V14 no mesmo período
    ├── 🧪 Validar RR 2:1: SL=75 vs TP=150, BE em ~50pts e max 6 barras
    ├── ⬜ Confirmar se NTSL permite BuyAtMarket/SellShortAtMarket com quantidade calculada iQtd
    ├── ⬜ Avaliar janela deslizante real para instabilidade, em vez de blocos resetados
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
