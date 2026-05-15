"""
analise_stop_breakeven.py
--------------------------
Lê todos os CSVs de backtest em robos/resultados/ e responde:

  1. Qual o SL médio real das perdas? (quanto o robô realmente perde por trade)
  2. Distribuição das perdas — onde está o P50/P80/P90?
  3. Se eu reduzir o SL de X para Y, quantos trades perdedores seriam salvos
     versus quantos winners seriam cortados prematuramente?
  4. Simulação de break-even agressivo (BE ratio 0.25 / 0.33 / 0.50 / 0.75)
  5. Recomendação final por arquivo (ativo + timeframe)

Execute:
    "C:/Program Files/Python312/python.exe" anotacoes/analise_stop_breakeven.py
"""

import os
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent / "robos" / "resultados"

# ── helpers ──────────────────────────────────────────────────────────────────


def br_float(s):
    """Converte '1.365,00' → -1365.0 etc."""
    s = s.strip().replace('\xa0', '')
    if not s or s in ('-', ''):
        return 0.0
    return float(s.replace('.', '').replace(',', '.'))


def parse_csv(fpath):
    """
    Retorna lista de dicts por trade:
        res     : resultado da operação em pontos (+ = ganho, - = perda)
        ganho   : ganho máx. intra-trade (quando disponível, senão 0)
        perda   : perda máx. intra-trade (quando disponível, senão 0)
        lado    : 'C' ou 'V'
        medio   : 'Sim' | 'Não'
        total   : resultado acumulado até aqui
    """
    rows = []
    try:
        with open(fpath, encoding='latin-1') as f:
            lines = f.readlines()
    except Exception:
        return rows

    # localiza linha de cabeçalho
    hi = None
    for i, l in enumerate(lines):
        if 'Res. Opera' in l or ('Lado' in l and 'Abertura' in l):
            hi = i
            break
    if hi is None:
        return rows

    for line in lines[hi + 1:]:
        parts = line.rstrip('\n').split(';')
        if len(parts) < 15:
            continue
        try:
            lado = parts[6].strip()
            res = br_float(parts[14])
            ganho = br_float(parts[17]) if len(
                parts) > 17 and parts[17].strip() else 0.0
            perda = br_float(parts[18]) if len(
                parts) > 18 and parts[18].strip() else 0.0
            total = br_float(parts[20]) if len(
                parts) > 20 and parts[20].strip() else 0.0
            medio = parts[10].strip() if len(parts) > 10 else ''
            rows.append(dict(res=res, ganho=ganho, perda=perda, lado=lado,
                             medio=medio, total=total))
        except Exception:
            continue
    return rows


def percentile(sortedlist, pct):
    if not sortedlist:
        return 0.0
    i = int(len(sortedlist) * pct / 100)
    i = min(i, len(sortedlist) - 1)
    return sortedlist[i]


def simulate_breakeven(rows, be_ratio, sl_pts):
    """
    Simula: após mover SL p/ entrada quando lucro >= sl_pts*be_ratio*3 (= TP*be_ratio,
    assumindo RR=3), qualquer trade que virou negativo após atingir BE fecha no zero.

    Conservador: usamos res_real do trade:
      - se res > 0 e >= sl_pts * 3 * be_ratio → era winner de qualquer forma
      - se res < 0 mas ganho_max >= sl_pts * 3 * be_ratio → SALVO pelo BE → vira 0
      - resto: sem impacto
    """
    salvo = 0
    total_sim = 0.0
    for r in rows:
        tp_proxy = sl_pts * 3
        be_trigger = tp_proxy * be_ratio
        if r['res'] < 0 and r['ganho'] >= be_trigger:
            # o trade chegou a atingir o trigger do BE antes de voltar contra
            total_sim += 0.0   # fecha no zero (BE)
            salvo += 1
        else:
            total_sim += r['res']
    return total_sim, salvo


# ── main ─────────────────────────────────────────────────────────────────────

files = sorted(BASE.glob("*.csv"))

print("=" * 100)
print("  ANÁLISE DE STOP LOSS + BREAK-EVEN — TradeTech (WES)")
print("=" * 100)

for fpath in files:
    rows = parse_csv(fpath)
    if not rows:
        continue

    n = len(rows)
    wins = [r for r in rows if r['res'] > 0]
    losses = [r for r in rows if r['res'] < 0]
    zeros = [r for r in rows if r['res'] == 0]
    total_real = rows[-1]['total'] if rows else 0.0

    if not losses:
        continue

    abs_losses = sorted(abs(r['res']) for r in losses)
    abs_wins = sorted(r['res'] for r in wins)

    win_pct = round(len(wins) / n * 100, 1)
    avg_loss = sum(abs_losses) / len(abs_losses)
    avg_win = sum(abs_wins) / len(abs_wins) if abs_wins else 0
    rr_real = avg_win / avg_loss if avg_loss else 0

    p50_loss = percentile(abs_losses, 50)
    p75_loss = percentile(abs_losses, 75)
    p90_loss = percentile(abs_losses, 90)

    # SL proxy: mediana das perdas absolutas (o que o robô realmente sofreu)
    sl_proxy = p50_loss

    # --- cabeçalho do arquivo ---
    name = fpath.name.replace('.csv', '')
    print(f"\n{'─'*100}")
    print(f"  📁  {name}")
    print(f"{'─'*100}")
    print(
        f"  Trades: {n}   |  Wins: {len(wins)} ({win_pct}%)   |  Losses: {len(losses)}   |  Zeros: {len(zeros)}")
    print(f"  Total acumulado:  {total_real:+,.0f} pts")
    print(
        f"  Avg ganho:        {avg_win:,.1f} pts   |  Avg perda: {avg_loss:,.1f} pts   |  RR real: {rr_real:.2f}")

    print(f"\n  ── Distribuição das PERDAS (percentis) ──────────────────────────────────────")
    print(f"  P25: {percentile(abs_losses, 25):6.0f} pts  |  P50: {p50_loss:6.0f} pts  |"
          f"  P75: {p75_loss:6.0f} pts  |  P90: {p90_loss:6.0f} pts  |  Max: {abs_losses[-1]:6.0f} pts")

    # ── Impacto de reduzir SL ──────────────────────────────────────────────────
    # Testa: se SL fosse crop = P25, P50 (mediana), P75 das perdas
    # Quantos trades perdedores seriam "limitados" / "cortados antes"?
    print(f"\n  ── Simulação: Cortar SL no Percentil das Perdas ─────────────────────────────")
    print(
        f"  {'SL testado':>14}  {'Perdas > SL':>12}  {'Redução perda total':>20}  {'Nota'}")

    for label, sl_test in [
        ("P25 atual", percentile(abs_losses, 25)),
        ("P50 atual", p50_loss),
        ("P75 atual", p75_loss),
        ("SL doc WDO=20", 20.0),
        ("SL doc WIN=822", 822.0),
        ("SL doc 5min WDO=12", 12.0),
        ("SL doc 5min WIN=342", 342.0),
    ]:
        if sl_test <= 0:
            continue
        # perdas que excedem o SL testado: já atingiriam o stop antes
        acima = [x for x in abs_losses if x > sl_test]
        if not acima:
            continue
        # economia em pontos se SL fosse esse
        reducao = sum(x - sl_test for x in acima)
        # ATENÇÃO: reduzir SL pode cortar winners que momentaneamente foram contra
        # Estimativa: winners com ganho_max disponível cujo ganho teve drawdown intra > SL_test
        winners_cortados = sum(1 for r in wins if r['perda'] > sl_test) if any(
            r['perda'] > 0 for r in wins) else 0
        nota = f"cortaria ~{winners_cortados} winners" if winners_cortados > 0 else "sem winners a cortar"
        print(
            f"  {label:>14}: {len(acima):>4} perdas > SL  |  economia ~{reducao:+8.0f} pts  |  {nota}")

    # ── Simulação Break-even ───────────────────────────────────────────────────
    print(f"\n  ── Simulação: Break-even em diferentes ratios ────────────────────────────────")
    print(f"  {'BE Ratio':>10}  {'Trades salvos':>14}  {'Total simulado':>16}  {'Delta vs real':>16}")

    for be in [0.25, 0.33, 0.50, 0.75]:
        total_sim, salvo = simulate_breakeven(rows, be, sl_proxy)
        delta = total_sim - total_real
        print(
            f"  BE={be:.2f}:    {salvo:>5} trades   |  {total_sim:>+12,.0f} pts  |  delta: {delta:>+12,.0f} pts")

    # ── Recomendação ──────────────────────────────────────────────────────────
    print(f"\n  ── Recomendação ──────────────────────────────────────────────────────────────")
    if 'WDO' in name and '5m' in name:
        print(
            f"  ✅ WDO 5min: SL 9-12pts testado. P50 perda real = {p50_loss:.0f}pts.")
        print(
            f"     → Se P50 < 12: o SL=12 já está certo. Focar em BE=0.33 (mais proteção).")
        print(f"     → Se P50 > 12: o rôbo está perdendo mais que o SL configurado — revisar filtro volume.")
    elif 'WDO' in name:
        print(
            f"  ✅ WDO: SL configurado = 20pts. P50 perda real = {p50_loss:.0f}pts.")
        print(f"     → Avaliar SL=15 se P50 < 15 — reduz perdas sem comprometer muitos winners.")
    elif 'WIN' in name and '5m' in name:
        print(
            f"  ✅ WIN 5min: SL 342pts (doc). P50 perda real = {p50_loss:.0f}pts.")
        print(
            f"     → Avaliar SL={int(p50_loss*1.1):.0f} (P50×1.1) como SL mais justo.")
    elif 'WIN' in name:
        print(
            f"  ✅ WIN: SL configurado = 822pts. P50 perda real = {p50_loss:.0f}pts.")
        print(f"     → P50 < 822? Provavelmente tem saídas por sinal contrário (StopCandleContra).")
        print(f"     → Avaliar SL dinâmico = max(342, range_candle × 1.5) para WIN 5min.")
    elif 'SEMAFORO' in name:
        print(
            f"  ✅ SEMAFORO: P50 perda = {p50_loss:.0f}pts. WIN% = {win_pct}%.")
        print(f"     → Focar em BE=0.25 agressivo se o robô captura moves grandes frequentemente.")

print("\n" + "=" * 100)
print("  FIM DA ANÁLISE")
print("=" * 100)
print("""
PRÓXIMOS PASSOS SUGERIDOS:
─────────────────────────────────────────────────────────────────────────────
1. SL DINÂMICO TIGHT:
   - WDO 15min: testar StopMinimo=15, FatorRangeSL=1.2 (SL = max(15, range×1.2))
   - WDO 5min:  testar StopMinimo=9,  FatorRangeSL=1.5 (range médio 5min ~6pts)
   - WIN 15min: testar StopMinimo=600, FatorRangeSL=1.5
   - WIN 5min:  testar StopMinimo=250, FatorRangeSL=1.5

2. BREAK-EVEN AGRESSIVO (recomendado: V12):
   - BreakEvenRatio=0.33 → move SL p/ entrada após apenas 33% do TP
   - Adicionar "trailing stop parcial": após 50% do TP, mover SL para +10pts de lucro
     (não apenas zero, mas lock parcial de ganho)

3. TRAILING STOP (nova feature para V12):
   - Após atingir BE, cada X pontos adicionais de lucro → mover SL X/2 no mesmo sentido
   - Parâmetros sugeridos: TrailingPasso=10pts (WDO), 400pts (WIN)

4. FILTRO DE PERDA MÁXIMA DIÁRIA:
   - Parar se perda acumulada no dia >= 2 × SL
   - Já existe StopHorario — adicionar MaxPerdaDiaria

5. VERSÕES A CRIAR:
   - FORCA_WDO_V12_TightSL  → StopMinimo=12, BreakEvenRatio=0.33, TrailingPasso=10
   - FORCA_WIN_V12_TightSL  → StopMinimo=300, BreakEvenRatio=0.33, TrailingPasso=300
""")
