// ==============================================================================
// SISTEMA QUANTITATIVO: MOTOR DE EXECUCAO, CONTEXTO & COLORACAO TEMPORAL (NTSL)
// ARQUIVO: Robo_Microestrutura_Barreiras.ntsl
// ATIVO RECOMENDADO: Mini-Indice B3 (WIN) | TEMPO GRAFICO: 1 Minuto
//
// REGRAS DE COLORACAO POR CONTEXTO DE HORARIO:
//   1. FORA DO HORARIO (< 09:15 ou > 16:15): PRETO (clPreto) -> Bloqueado
//   2. CONSOLIDACAO / ALMOCO (12:00 as 14:00): CINZA (clCinza) -> Pausa
//   3. JANELA DE OURO (09:15-12:00) & MODERADO (14:00-16:15):
//      - Barras Normais: BRANCO (clBranco)
//      - Sinais de Alta: VERDE BRILHANTE / VERDE ESCURO
//      - Sinais de Baixa: VERMELHO BRILHANTE / VERMELHO ESCURO
// ==============================================================================

Parametro
  // --- Horarios das Janelas de Contexto ---
  HoraOuroInicio(0915);     // Inicio da Janela de Ouro (09:15)
  HoraOuroFim(1200);        // Fim da Janela de Ouro (12:00)
  HoraConsolInicio(1200);   // Inicio da Consolidacao / Almoco (12:00)
  HoraConsolFim(1400);      // Fim da Consolidacao (14:00)
  HoraModInicio(1400);      // Inicio da Tarde Moderada (14:00)
  HoraModFim(1615);         // Fim das Entradas (16:15)
  HoraZeramento(1720);       // Zeramento compulsorio de fim de pregao (17:20)

  // --- Parametros de Volatilidade e Stops ---
  PeriodoATR(20);           // Periodo do ATR para calculo de stops dinamicos
  MultStopGain(2.50);       // Stop Gain: 2.5x ATR (Convexidade assimetrica)
  MultStopLoss(0.50);       // Stop Loss: 0.5x ATR (Stop curto estrito)
  MaxBarrasTrade(20);       // Barreira Temporal: maximo de barras no trade (20 min)
  OffsetTicks(5);           // Offset de protecao para ordens Stop (em pontos)

  // --- Limiares de Deteccao de Regime ---
  MultBrilhante(1.70);      // Amplitude da barra >= 1.70x ATR -> Brilhante
  MultEscuro(1.30);         // Amplitude da barra >= 1.30x ATR -> Escuro

  // --- Configuracao de Alertas e Sinais ---
  HabilitaAlerta(1);        // 1 = Alerta Sonoro ativo | 0 = Silencioso
  DestacarSinais(1);        // 1 = Destaca Verde/Vermelho nas janelas ativas | 0 = 100% Branco

Var
  vATR              : Real;
  vTamBarra         : Real;
  vTamBarraAnt      : Real;
  vEstadoAtual      : Inteiro;
  vEstadoAnterior   : Inteiro;
  vStopGainPts      : Real;
  vStopLossPts      : Real;
  vBarrasNoTrade    : Inteiro;
  vAlvo             : Real;
  vStop             : Real;
  vEmJanelaAtiva    : Booleano;
  vEmConsolidacao   : Booleano;

Inicio
  // --------------------------------------------------------------------------
  // 1. DEFINICAO DAS JANELAS DE HORARIO
  // --------------------------------------------------------------------------
  vEmJanelaAtiva  := ((Time >= HoraOuroInicio) E (Time < HoraOuroFim)) Ou 
                     ((Time >= HoraModInicio) E (Time <= HoraModFim));
  vEmConsolidacao := (Time >= HoraConsolInicio) E (Time < HoraConsolFim);

  // --------------------------------------------------------------------------
  // 2. MOTOR DE VOLATILIDADE & DIMENSIONAMENTO DE STOPS
  // --------------------------------------------------------------------------
  vATR := AvgTrueRange(PeriodoATR, 0);

  vStopLossPts := Round(vATR * MultStopLoss);
  Se (vStopLossPts < 35.0) Entao
    vStopLossPts := 35.0;

  vStopGainPts := Round(vATR * MultStopGain);
  Se (vStopGainPts < 120.0) Entao
    vStopGainPts := 120.0;

  vTamBarra    := High - Low;
  vTamBarraAnt := High[1] - Low[1];

  // --------------------------------------------------------------------------
  // 3. CLASSIFICACAO DOS ESTADOS (MOTOR DE CONTEXTO)
  // --------------------------------------------------------------------------
  Se (vTamBarra >= (vATR * MultBrilhante)) Entao
  Inicio
    Se (Close >= Open) Entao vEstadoAtual := 3 Senao vEstadoAtual := 4;
  Fim
  Senao Se (vTamBarra >= (vATR * MultEscuro)) Entao
  Inicio
    Se (Close >= Open) Entao vEstadoAtual := 1 Senao vEstadoAtual := 2;
  Fim
  Senao
  Inicio
    vEstadoAtual := 0;
  Fim;

  // Estado Anterior (Barra [1]):
  Se (vTamBarraAnt >= (vATR[1] * MultBrilhante)) Entao
  Inicio
    Se (Close[1] >= Open[1]) Entao vEstadoAnterior := 3 Senao vEstadoAnterior := 4;
  Fim
  Senao Se (vTamBarraAnt >= (vATR[1] * MultEscuro)) Entao
  Inicio
    Se (Close[1] >= Open[1]) Entao vEstadoAnterior := 1 Senao vEstadoAnterior := 2;
  Fim
  Senao
  Inicio
    vEstadoAnterior := 0;
  Fim;

  // --------------------------------------------------------------------------
  // 4. COLORACAO POR CONTEXTO (PRETO, CINZA, BRANCO E SINAIS)
  // --------------------------------------------------------------------------
  // A) FORA DO HORARIO OPERACIONAL: PRETO
  Se (Nao vEmJanelaAtiva) E (Nao vEmConsolidacao) Entao
  Inicio
    PaintBar(clPreto);
  Fim
  // B) CONSOLIDACAO (ALMOCO): CINZA
  Senao Se vEmConsolidacao Entao
  Inicio
    PaintBar(clCinza);
  Fim
  // C) JANELAS ATIVAS (JANELA DE OURO & MODERADO): BRANCO / SINAIS
  Senao Se vEmJanelaAtiva Entao
  Inicio
    Se (DestacarSinais = 1) Entao
    Inicio
      Se (vEstadoAtual = 3) Entao
        PaintBar(RGB(0, 255, 0))        // Verde Brilhante (Climax Alta)
      Senao Se (vEstadoAtual = 1) Entao
        PaintBar(RGB(0, 120, 50))       // Verde Escuro (Expansao Alta)
      Senao Se (vEstadoAtual = 4) Entao
        PaintBar(RGB(255, 40, 40))      // Vermelho Brilhante (Climax Baixa)
      Senao Se (vEstadoAtual = 2) Entao
        PaintBar(RGB(140, 0, 0))        // Vermelho Escuro (Expansao Baixa)
      Senao
        PaintBar(clBranco);             // Barra Neutra: BRANCO
    Fim
    Senao
    Inicio
      PaintBar(clBranco);               // 100% Branco
    Fim;
  Fim;

  // --------------------------------------------------------------------------
  // 5. CONTROLE DE HORARIO (ZERAMENTO DE FIM DE DIA)
  // --------------------------------------------------------------------------
  Se (Time >= HoraZeramento) Entao
  Inicio
    Se HasPosition Entao ClosePosition;
    vBarrasNoTrade := 0;
  Fim
  Senao
  Inicio
    // ------------------------------------------------------------------------
    // 6. GESTAO DA POSICAO ABERTA (BARREIRA TRIPLA)
    // ------------------------------------------------------------------------
    Se HasPosition Entao
    Inicio
      vBarrasNoTrade := vBarrasNoTrade + 1;

      // TIME STOP (20 MINUTOS)
      Se (vBarrasNoTrade >= MaxBarrasTrade) Entao
      Inicio
        ClosePosition;
        vBarrasNoTrade := 0;
      Fim
      Senao
      Inicio
        Se IsBought Entao
        Inicio
          vAlvo := BuyPrice + vStopGainPts;
          vStop := BuyPrice - vStopLossPts;

          SellToCoverLimit(vAlvo);
          SellToCoverStop(vStop, vStop - OffsetTicks);
        Fim
        Senao Se IsSold Entao
        Inicio
          vAlvo := SellPrice - vStopGainPts;
          vStop := SellPrice + vStopLossPts;

          BuyToCoverLimit(vAlvo);
          BuyToCoverStop(vStop, vStop + OffsetTicks);
        Fim;
      Fim;
    Fim
    // ------------------------------------------------------------------------
    // 7. GATILHOS DE ENTRADA COM ALERTA SONORO (SOMENTE NAS JANELAS ATIVAS)
    // ------------------------------------------------------------------------
    Senao Se vEmJanelaAtiva Entao
    Inicio
      vBarrasNoTrade := 0;

      // CONTEXTO 1: FADE DA BARRA VERDE BRILHANTE (EXAUSTAO DE ROMPIMENTO)
      Se (vEstadoAnterior = 3) E (Close[1] > Open[1]) E (Close < Low[1]) Entao
      Inicio
        SellShortAtMarket;
        Se (HabilitaAlerta = 1) Entao Alert(clVermelho);
      Fim
      // CONTEXTO 2: FADE DA BARRA VERMELHA BRILHANTE (EXAUSTAO DE PANICO)
      Senao Se (vEstadoAnterior = 4) E (Close[1] < Open[1]) E (Close > High[1]) Entao
      Inicio
        BuyAtMarket;
        Se (HabilitaAlerta = 1) Entao Alert(clVerde);
      Fim
      // CONTEXTO 3: FLUXO CONVEXO NO REGIME NEUTRO (SG 2.5x / SL 0.5x)
      Senao Se (vEstadoAtual = 0) E (vEstadoAnterior = 0) Entao
      Inicio
        Se (Close > Media(20, Close)) E (Close > Open) E (Close > High[1]) Entao
        Inicio
          BuyAtMarket;
          Se (HabilitaAlerta = 1) Entao Alert(clVerde);
        Fim
        Senao Se (Close < Media(20, Close)) E (Close < Open) E (Close < Low[1]) Entao
        Inicio
          SellShortAtMarket;
          Se (HabilitaAlerta = 1) Entao Alert(clVermelho);
        Fim;
      Fim;
    Fim;
  Fim;
Fim;