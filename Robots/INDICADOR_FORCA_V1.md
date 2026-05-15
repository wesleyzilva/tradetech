# INDICADOR_FORCA_V1 — Documentação Técnica

> **Versão:** 1.0 · **Plataforma:** Neologica Profit (NTFL) · **Ativos:** WDO e WIN  
> **Tipo:** Indicador visual — **sem ordens** · somente coloração e histograma  
> **Uso:** Aplique no gráfico junto com qualquer robot NTSL para visualização de força

---

## O que faz?

Indicador visual puro baseado na fórmula F = M × A. Não envia ordens. Oferece:
- **PaintBar:** coloração das barras no gráfico principal com 7 tons + tratamento especial para doji e volume expresso
- **Histograma (sub-painel):** valor de F plotado como barras coloridas (positivo = compra, negativo = venda)
- **Linhas de threshold:** marcadores visuais nos níveis ±40, ±60, ±80 e zero
- **Destaque de zona S/R:** candle amarelo quando preço toca zona sem força
- **Volume expresso (gold):** Plot9 dourado quando volume > 1.5× média

---

## Esquema de Cores — 7 tons + especiais

### Compradores (positivo)

| Cor | Força | Significado | Ação manual |
|-----|-------|-------------|-------------|
| 🩶 **Cinza** | F +40 a +59 | Força compradora fraca | Observar — não entrar |
| 🟢 **Verde** `RGB(0,200,0)` | F +60 a +79 | Força compradora forte | **Potencial entrada LONG** |
| 🟦 **Cyan** `RGB(0,220,220)` | F > +80 | Exaustão compradora | **Entrada LONG — máxima prioridade** |

### Vendedores (negativo)

| Cor | Força | Significado | Ação manual |
|-----|-------|-------------|-------------|
| 🩶 **Cinza** | F –40 a –59 | Força vendedora fraca | Observar — não entrar |
| 🔴 **Vermelho** `RGB(200,0,0)` | F –60 a –79 | Força vendedora forte | **Potencial entrada SHORT** |
| 🩷 **Fúcsia** `RGB(255,0,180)` | F < –80 | Exaustão vendedora | **Entrada SHORT — máxima prioridade** |

### Neutros

| Cor | Condição | Significado | Ação manual |
|-----|----------|-------------|-------------|
| ⬜ **Branco** | F –40 a +40 | Sem força direcional | Skip |
| ⬛ **Branco (Doji)** | `corpo/range < 15%` (LimiarDoji) | Indecisão — corpo muito pequeno | **Skip obrigatório** |
| 🟡 **Amarelo** | Preço em zona S/R, F < limiar | Zona ativa sem confirmação | **Aguardar força** |

### Volume Expresso

| Cor | Condição | Significado |
|-----|----------|-------------|
| 🟡 **Gold Plot9** `RGB(255,215,0)` | Volume > 1.5× média | Atividade institucional — **confirma qualquer sinal na mesma barra** |

---

## Por que Doji recebe branco obrigatório?

```
F = (corpo/range) × (volume/mediaVolume)

Doji: corpo ≈ 0, range > 0
  → corpo/range → 0
  → F → 0 independente do volume

Um doji com volume alto NÃO é um sinal direcional — é indecisão com liquidez.
A cor branca força o trader a ignorar esse candle.
Parâmetro: LimiarDoji = 0.15 (15% de corpo/range → abaixo disso = doji)
```

---

## Volume Expresso (Gold) — Como Interpretar

```
Condição: Volume_atual > RatioVolumeExpresso × Media_Volume(20)
Padrão:   Volume > 1.5× a média dos últimos 20 candles

Plot9 gold aparece abaixo (ou acima) da barra no histograma
→ Institucional entrou neste candle
→ Se alinhado com força direcional (verde/cyan/vermelho/fúcsia): SINAL FORTE
→ Se em doji ou branco: liquidez sem direção, não confirma sinal
```

---

## Saídas do Indicador

| Plot | Painel | O que exibe |
|------|--------|-------------|
| **Plot1** | Sub-painel | Histograma de F (positivo = compra, negativo = venda), colorido por zona |
| **Plot2** | Sub-painel | Linha de zero (referência) |
| **Plot3** | Sub-painel | Linha em +ForcaFraca (40) e –ForcaFraca (40) |
| **Plot4** | Sub-painel | Linha em +ForcaForte (60) e –ForcaForte (60) |
| **Plot5** | Sub-painel | Linha em +ForcaExaustao (80) e –ForcaExaustao (80) |
| **Plot6-8** | Sub-painel | Linhas adicionais de threshold |
| **Plot9** | Sub-painel | Gold (volume expresso) — barra dourada quando vol > 1.5× média |
| **PaintBar** | Gráfico principal | Coloração das barras (7 tons + doji + zona) |

---

## Como Usar com os Robots

### Configuração recomendada no Profit

```
Gráfico 1 (visual):
  └── INDICADOR_FORCA_V1 (NTFL) → paintbar + histograma
      └── Configure ZonaPontos para o ativo:
            WDO 15min: 20 pts | WIN 15min: 822 pts

Gráfico 1 (execução, mesma janela):
  └── FORCA_WDO_V11 ou FORCA_WIN_V11 (NTSL) → envia ordens
      └── HabilitarOperacoes = true para ordens reais
      └── HabilitarOperacoes = false para apenas monitorar cores
```

> O indicador (NTFL) e o robot (NTSL) usam a mesma fórmula F=M×A, então as cores são consistentes. Você vê pelo indicador exatamente o que o robot está "pensando".

---

## Leitura Visual — Passo a Passo para Operação Manual

### 1. Verificar alinhamento MTF
- Candles acima da EMA de contexto no TF maior? → viés de alta
- Candles abaixo? → viés de baixa
- Sem definição clara → aguardar

### 2. Identificar o tom no candle atual
```
Doji (branco forçado)         → Skip sem exceção
Branco (F < ±40)              → Skip
Cinza (F ±40–59)              → Observar, não entrar
Verde/Vermelho (F ±60–79)     → Potencial entrada, verificar MTF
Cyan/Fúcsia (F > ±80)         → Entrada prioritária, verificar MTF
Amarelo (zona sem força)      → Aguardar próximo candle com força
```

### 3. Gold Plot9 presente?
- Sim + Verde/Cyan/Vermelho/Fúcsia → **sinal reforçado** (institucional confirmou)
- Sim + Branco/Cinza → indecisão com liquidez → skip

### 4. Aguardar fechamento do candle
> **Nunca agir antes do candle fechar.** A cor pode mudar até o último segundo.  
> Confirme o fechamento → entre no próximo candle (mercado, na abertura).

---

## Parâmetros do Indicador

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| `ForcaFraca` | 40.0 | Início da zona fraca (cinza) |
| `ForcaForte` | 60.0 | Início da zona forte (verde/vermelho) |
| `ForcaExaustao` | 80.0 | Início da exaustão (cyan/fúcsia) |
| `LimiarDoji` | 0.15 | corpo/range < 15% = doji → branco forçado |
| `RatioVolumeExpresso` | 1.5 | Volume > 1.5× média → gold |
| `PeriodoMediaVolume` | 20 | Período da média de volume |
| `JanelaZona` | 3 | Candles para trás para detectar zona S/R |
| `ZonaPontos` | 20.0 | Amplitude da zona (WDO: 20 · WIN: 822) |
| `ToleranciaZona` | 5.0 | Margem de toque (WDO: 5 · WIN: 200) |
| `MostrarZona` | true | false = desativa coloração de zona |
| `MostrarAlertas` | true | Alerta sonoro em F ≥ ForcaForte |

---

## Diferença em relação ao FORCA_WDO_V11 (que também pinta barras)

| Aspecto | INDICADOR_FORCA_V1 | FORCA_WDO_V11 |
|---------|-------------------|----------------|
| Tipo | NTFL (visual puro) | NTSL (envia ordens) |
| Tons | **7 tons** (fraca/forte/exaustão para cada lado) | 4 tons |
| Doji | ✅ Branco forçado | ❌ Não tratado |
| Volume expresso | ✅ Gold Plot9 | ❌ Não plotado |
| Zona S/R amarelo | ✅ Sim | ✅ Sim |
| Histograma F | ✅ Sub-painel completo | ❌ Sem histograma |
| Ordens | ❌ Não envia | ✅ Envia |
