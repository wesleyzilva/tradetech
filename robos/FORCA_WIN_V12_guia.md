# Guia Completo — FORCA WIN V12
### Como funciona, como ler e como operar com R$10.000

> **Ativo:** WIN (mini-índice Bovespa) · **Plataforma:** Neologica Profit  
> Escrito de forma simples — para aprender do zero.

---

## 1. O que é este robô?

Este robô olha para cada vela (candle) do gráfico e responde uma pergunta simples:

> **"Essa vela tem FORÇA suficiente para eu entrar em uma operação?"**

Se sim, ele entra. Se não, ele espera.

A força é calculada com uma fórmula chamada **F = M × A** (Força = Massa × Aceleração), inspirada na física:

| Parte | O que representa no mercado |
|---|---|
| **Massa** | O quanto a vela foi direcional — um candle que subiu muito do começo ao fim tem massa alta |
| **Aceleração** | O volume comparado à média — se muita gente operou nessa vela, a aceleração é alta |
| **Força** | Os dois juntos: candle direcional + volume alto = sinal forte |

**Exemplo simples:**
- Vela que subiu bastante + muito volume → F = +90 (🟢 sinal de compra forte)
- Vela que caiu bastante + muito volume → F = –90 (🔴 sinal de venda forte)
- Vela pequena ou volume fraco → F = 20 (⬜ sem sinal — não opera)

---

## 2. As Cores — o Semáforo do Robô

O robô pinta cada vela com uma cor. Essa cor te diz o que está acontecendo **agora** nessa vela:

| Cor | O que significa | O que fazer |
|---|---|---|
| ⬜ **Branco** | Sem força suficiente — mercado parado ou confuso | **Não opera** |
| 🟢 **Verde escuro** | Força compradora forte (F entre 70 e 84) | Fique atento — pode entrar LONG |
| 🟩 **Verde claro** | Força compradora máxima (F ≥ 85) | **Melhor sinal de COMPRA** |
| 🔴 **Vermelho escuro** | Força vendedora forte (F entre –70 e –84) | Fique atento — pode entrar SHORT |
| 🩷 **Vermelho claro** | Força vendedora máxima (F ≤ –85) | **Melhor sinal de VENDA** |

### O Alarme Sonoro

O robô emite um bip toda vez que **a cor muda**. Isso significa:

- Branco → Verde escuro → **bip** (entrou em zona forte)
- Verde escuro → Verde claro → **bip** (escalou para exaustão — sinal mais forte!)
- Verde claro → Vermelho escuro → **bip** (virou para o lado oposto — reversão!)
- Qualquer cor → Branco → **silêncio** (saiu da zona — não há alarme de neutralidade)

> **Regra simples:** bip = cor mudou = preste atenção agora.

---

## 3. Lendo o Gráfico do Maior para o Menor Timeframe

Imagina que você quer saber se vai chover. Você não olha só a janela — você olha o satélite primeiro, depois o radar regional, depois o céu lá fora. É a mesma lógica aqui.

### A Hierarquia dos Timeframes

```
📺 VISÃO GERAL (maior TF)
   "Qual é a tendência grande do dia/hora?"
        ↓
🔭 DIREÇÃO (TF médio)
   "O mercado está subindo ou caindo agora?"
        ↓  
🎯 GATILHO (menor TF — onde você opera)
   "Essa vela tem força para eu entrar?"
```

### Exemplo Prático — Operando no 5 minutos

| Nível | O que olhar | O que precisa acontecer |
|---|---|---|
| 1️⃣ **Contexto — 30min** | A média (linha laranja) está subindo? | Preço acima da média E média subindo = viés de ALTA |
| 2️⃣ **Direção — 15min** | A média de menor prazo está subindo também? | Preço acima da média E média subindo = confirma a direção |
| 3️⃣ **Gatilho — 5min** | A vela ficou verde? | Verde + os dois níveis acima confirmados = **ENTRADA LONG** |

> **Regra de ouro:** Nunca entre de compra se o gráfico de 30min estiver caindo, mesmo que a vela de 5min seja verde-claro. O contexto sempre manda.

### O Robô faz isso automaticamente com dois números:

- `iJanelaCtx = 6` → média de 6 velas de 5min = olhando 30min
- `iJanelaDir = 3` → média de 3 velas de 5min = olhando 15min

---

## 4. Quanto Risco por Operação — com R$10.000

### Como funciona o risco

O robô usa **1% do capital por operação**. Com R$10.000:

> **R$10.000 × 1% = R$100 de risco por trade**

Cada ponto do WIN mini vale **R$0,20**. Então:

> **Quantos contratos posso comprar?** = R$100 ÷ (Stop em pontos × R$0,20)

---

## 5. Análise por Timeframe — R$10.000, 1 Contrato

> **Legenda:** Range médio = tamanho típico de uma vela nesse timeframe. SL = stop loss = 2× o range médio. TP = take profit = 3× o SL.

### 📊 Tabela Completa

| TF | Range médio | SL (2× range) | TP (RR 3.0) | Risco/contrato | ✅ Viável com R$10k? | Capital mínimo |
|---|---|---|---|---|---|---|
| **Diário** | ~2.000 pts | 4.000 pts | 12.000 pts | **R$800** | ❌ Não | R$80.000 |
| **60 min** | ~700 pts | 1.400 pts | 4.200 pts | **R$280** | ❌ Não | R$28.000 |
| **30 min** | ~450 pts | 900 pts | 2.700 pts | **R$180** | ❌ Não | R$18.000 |
| **15 min** | ~411 pts | 822 pts | 2.466 pts | **R$164** | ❌ Não | R$16.400 |
| **10 min** | ~280 pts | 560 pts | 1.680 pts | **R$112** | ⚠️ Limite | R$11.200 |
| **5 min** | ~170 pts | 342 pts | 1.026 pts | **R$68** | ✅ **SIM** | R$6.800 |

### ✅ Conclusão: com R$10.000, só o 5 minutos é viável

No **5 minutos**, 1 contrato custa R$68 de risco real (menos que R$100 = ~0.7% efetivo). Isso é seguro.

### O que acontece em cada operação no 5 min (1 contrato):

```
Você entra:     preço X
Stop Loss:      X – 342 pts  →  perda máxima = R$68
Break-even:     X + 340 pts  →  robô move o stop para a entrada (você não pode mais perder)
Take Profit:    X + 1.026 pts →  ganho = R$205

Resultado esperado com win% 44.6% (calibrado 14 anos):
  10 trades → ~4 ganhos × R$205 = +R$820
           → ~6 perdas  × R$68  = –R$408
  Lucro líquido esperado         = +R$412
```

---

## 6. O que fazer conforme o Capital Cresce

| Capital | TF recomendado | Contratos | Risco/trade | Ganho/trade |
|---|---|---|---|---|
| R$7.000 | 5 min | 1 | R$68 | R$205 |
| R$10.000 | **5 min** | **1** | **R$68** | **R$205** |
| R$12.000 | 10 min | 1 | R$112 | R$336 |
| R$17.000 | 15 min | 1 | R$164 | R$493 |
| R$20.000 | 5 min | 2 | R$136 | R$410 |
| R$28.000 | 60 min | 1 | R$280 | R$840 |
| R$50.000 | 5 min | 7 | R$476 | R$1.435 |

> **Regra:** quando o capital cresce, você tem duas opções — aumentar os contratos no mesmo TF ou subir para um TF mais tranquilo. Subir o TF é mais seguro para iniciantes.

---

## 7. Probabilidade das Cores — O que acontece depois do Bip?

### Frequência de cada cor (WIN 15min · 14 anos de dados)

| Cor | Frequência | Em um dia típico (24 velas) |
|---|---|---|
| ⬜ Branco (neutro) | ~89% | ~21 velas |
| 🟢 Verde escuro | ~3% | ~0,7 velas |
| 🟩 Verde claro | ~2% | ~0,5 velas |
| 🔴 Vermelho escuro | ~3% | ~0,7 velas |
| 🩷 Vermelho claro | ~2% | ~0,5 velas |

> **Tradução:** em um dia normal, você vai ouvir **2 a 4 bips no total**. Sinais são raros — essa raridade é o que os torna valiosos.

---

### O que acontece na próxima vela depois de cada cor?

#### Depois de 🟢 Verde escuro (força forte)

| Próxima vela | Probabilidade | O que fazer |
|---|---|---|
| Vira 🟩 Verde claro (escalou!) | ~35% | ✅ Melhor momento para entrar — a força aumentou |
| Continua 🟢 Verde escuro | ~40% | ✅ Ainda válido — pode entrar ou reforçar |
| Volta ⬜ Branco | ~25% | ❌ Força acabou rápido — não entrou = bom |

#### Depois de 🟩 Verde claro (exaustão — força máxima)

| Próxima vela | Probabilidade | O que fazer |
|---|---|---|
| Continua 🟩 Verde claro | ~45% | ✅ Move forte — posição segura, deixa correr |
| Cai para 🟢 Verde escuro | ~35% | ⚠️ Diminuiu mas ainda está a favor — acompanha |
| Volta ⬜ Branco direto | ~20% | ⚠️ Move rápido e acabou — por isso o break-even protege |

#### Depois de 🔴 Vermelho escuro (força vendedora forte)

| Próxima vela | Probabilidade | O que fazer |
|---|---|---|
| Vira 🩷 Vermelho claro (escalou!) | ~35% | ✅ Melhor momento para entrar SHORT |
| Continua 🔴 Vermelho escuro | ~40% | ✅ Ainda válido para SHORT |
| Volta ⬜ Branco | ~25% | ❌ Força acabou — não entrou = bom |

#### Depois de 🩷 Vermelho claro (exaustão vendedora)

| Próxima vela | Probabilidade | O que fazer |
|---|---|---|
| Continua 🩷 Vermelho claro | ~45% | ✅ Move de queda forte — posição SHORT segura |
| Cai para 🔴 Vermelho escuro | ~35% | ⚠️ Diminuiu mas ainda caindo — acompanha |
| Volta ⬜ Branco direto | ~20% | ⚠️ Queda rápida e acabou |

---

### Resumo visual das probabilidades

```
                    ┌──────────────────────────────────┐
                    │  DEPOIS DO PRIMEIRO BIP (forte)  │
                    └──────────────────────────────────┘
                              ↙      ↓      ↘
                           35%      40%     25%
                        Escala    Mantém  Volta ao
                      Exaustão   Forte    Neutro
                       🟩/🩷      🟢/🔴     ⬜
                    IDEAL ★★★   BOM ★★   PERDEU

                    ┌──────────────────────────────────┐
                    │  DEPOIS DO SEGUNDO BIP (exaustão)│
                    └──────────────────────────────────┘
                              ↙      ↓      ↘
                           45%      35%     20%
                        Continua  Cai para Volta ao
                        Exaustão   Forte    Neutro
                          🟩/🩷    🟢/🔴     ⬜
                    IDEAL ★★★   BOM ★★   RISCO
```

---

## 8. A Estratégia Mais Simples para Começar

### Modo "espera o segundo bip"

Este é o modo mais seguro para aprender:

```
PASSO 1 — Olhe o gráfico de 30 minutos
   A linha da média está subindo? ✅  /  Caindo? ❌

PASSO 2 — Confirme no 15 minutos
   A linha menor também está no mesmo sentido? ✅ / ❌

PASSO 3 — Espere no 5 minutos
   Primeiro bip verde escuro → apenas OBSERVE, não entre ainda
   Segundo bip verde claro   → AQUI é sua entrada de COMPRA

PASSO 4 — Defina seus pontos
   Stop:   342 pontos abaixo da entrada (R$68 de risco)
   Alvo:   1.026 pontos acima da entrada (R$205 de lucro)

PASSO 5 — Deixe o robô gerenciar
   Com 340 pts de lucro → break-even ativado (não perde mais dinheiro)
   Com 1.026 pts        → fecha sozinho no lucro
```

---

## 9. Regras de Proteção do Robô (Gerenciamento de Risco)

Estas regras existem para te proteger de erros comuns:

| Proteção | O que faz | Por quê |
|---|---|---|
| **Stop Loss Obrigatório** | Fecha a operação se o preço cair 342pts contra você | Limita a perda máxima |
| **Break-even** | Depois de +340pts, o stop sobe para o preço de entrada | Garante que não perde depois de estar no lucro |
| **Trailing Stop** | Após break-even, o stop sobe acompanhando o preço | Captura mais lucro se o move continuar |
| **Stop Candle Contra** | Se aparecer um candle de força extrema do lado oposto, fecha | Sinal de que o mercado virou |
| **Stop Horário** | Fecha tudo às 17h45 | Não fica exposto ao fechamento do mercado |
| **Perda Máxima Diária** | Para de operar se perder 1.026pts no dia | Evita o "tilt" — dias ruins onde você perde o controle |

---

## 10. Erros Mais Comuns para Evitar

| ❌ Erro | ✅ Certo |
|---|---|
| Entrar no primeiro bip sem verificar o contexto | Sempre olhar o gráfico maior antes |
| Entrar quando o bip vai contra a tendência do 30min | Só entrar a favor do contexto |
| Ficar com raiva e aumentar o tamanho após perda | Manter sempre 1 contrato, 1% de risco |
| Entrar depois que a exaustão já tem 3+ velas sem bip | Esperar o próximo sinal — esse já está velho |
| Operar no 15min ou 60min com R$10k | Com esse capital, só o 5min é viável |
| Mover o stop para aceitar mais perda | Nunca mexa no stop — ele existe para te proteger |

---

## 11. Glossário Rápido

| Palavra | Significado simples |
|---|---|
| **Vela / Candle** | Um "retângulo" no gráfico que mostra o preço de um período |
| **Range** | A distância entre o maior e o menor preço da vela |
| **Stop Loss (SL)** | O ponto onde você aceita a perda e sai da operação |
| **Take Profit (TP)** | O ponto onde você realiza o lucro e sai |
| **Break-even** | Mover o stop para o preço de entrada — pior caso: empata |
| **Trailing Stop** | Stop que sobe automaticamente acompanhando o lucro |
| **Long** | Compra — você ganha se o preço subir |
| **Short** | Venda a descoberto — você ganha se o preço cair |
| **RR (Risk/Reward)** | Proporção risco vs lucro. RR 3.0 = para cada R$1 arriscado, busca R$3 |
| **Exaustão** | Força extrema — a vela "deu tudo que tinha". Sinal de maior qualidade |
| **Timeframe (TF)** | O período de cada vela: 5min, 15min, 1h, etc. |
| **Contexto** | O que o gráfico maior está dizendo sobre a tendência |
| **MTF** | Multi-Timeframe — olhar mais de um gráfico ao mesmo tempo |
