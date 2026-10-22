# Estratégia de Análise Probabilística e Definição de Stop

## Objetivo
Analisar a mesma série de dados por três óticas (Prophet, ARIMA e LSTM) para:
- Estimar a probabilidade de operar a favor da tendência.
- Definir o range ideal de stop que seja seguro, mas não tão apertado a ponto de virar operação contrária.

---

## Passo 1 – Preparação dos Dados
- Carregar CSV (ex: WINQ26 diário).
- Normalizar preços e calcular retornos.
- Separar em treino/teste para validação.

---

## Passo 2 – Modelos Utilizados

### 🔹 Prophet
- Detecta **tendência e sazonalidade**.
- Saída: previsão de preço futuro + intervalo de confiança.
- Interpretação: intervalo estreito → maior probabilidade de continuidade.

### 🔹 ARIMA
- Modela **probabilidade de continuidade** da série.
- Saída: previsão pontual + erro padrão.
- Interpretação: erro padrão ajuda a definir o **stop ideal** (ex: 1,5x o desvio padrão da previsão).

### 🔹 LSTM
- Aprende **padrões não lineares**.
- Saída: previsão de sequência de preços.
- Interpretação: reforça operar a favor se prevê continuidade; alerta se prevê reversão.

---

## Passo 3 – Consolidação Probabilística
- Calcular métricas de erro (RMSE, MAE) para cada modelo.
- Ponderar os três resultados:
  - Se **2 de 3 modelos** apontam continuidade → operar a favor.
  - Se há divergência → reduzir posição ou aguardar confirmação.

---

## Passo 4 – Range Ideal de Stop
- Usar **volatilidade histórica** (ATR ou desvio padrão dos últimos 14 candles).
- Fórmula:
  

\[
  Stop = k \cdot \sigma
  \]


  onde \(k\) = 1,5 ou 2 conforme perfil de risco.
- Validar se o stop cobre o “ruído” sem comprometer o RR (Risk/Reward).

---

## Passo 5 – Decisão Final
- Se probabilidade de continuidade > 60% **e** RR ≥ 2:1 → **executar operação a favor**.
- Caso contrário → **não operar ou reduzir lote**.

---

## Benefícios do Pipeline
- Combina **estatística clássica (ARIMA)**, **modelagem de tendência (Prophet)** e **aprendizado profundo (LSTM)**.
- Garante visão probabilística robusta.
- Define stops baseados em volatilidade real, evitando operações contrárias.
