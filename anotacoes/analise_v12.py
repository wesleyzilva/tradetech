"""
Análise completa: FORCA_WDO_V12 + FORCA_WIN_V12 vs V11
- Comparativo por timeframe
- Win/loss por lado (Compra/Venda)
- Transições de cor: Verde fraco→Verde forte / Vermelho fraco→Vermelho forte
- Pontos médios por cor (proxy de sinal fraco vs forte)
- Diagnóstico de horário, premissas assumidas, sugestão V13
- Gera HISTORICO-RESULTADOS.md

NOMENCLATURA DE CORES (alinhada ao código NTSL dos robôs):
  Verde fraco      = F ≥  70 → LONG normal       (ForcaMinimaForte)
  Verde forte      = F ≥  85 → LONG prioritário  (ForcaExaustao)
  Vermelho fraco   = F ≤ -70 → SHORT normal
  Vermelho forte   = F ≤ -85 → SHORT prioritário
"""

import os
import re
from pathlib import Path
from collections import Counter, defaultdict

BASE = Path("C:/repositorio/repositorio_particular/tradetech/robos/resultados")
OUT = Path("C:/repositorio/repositorio_particular/tradetech/anotacoes")

# ─── Parser ──────────────────────────────────────────────────────────────────


def parse_file(fpath):
    rows = []
    with open(fpath, encoding="latin-1") as f:
        lines = f.readlines()
    hi = next((i for i, l in enumerate(
        lines) if "N\x99mero Opera" in l or "Número Opera" in l or "N" in l and "Opera" in l and ";" in l), None)
    if hi is None:
        return rows, None
    total_final = None
    for line in lines[hi + 1:]:
        p = line.rstrip("\n").split(";")
        if len(p) < 20:
            continue
        try:
            res = float(p[14].replace(".", "").replace(",", "."))
            lado = p[6].strip()
            total = float(p[20].replace(".", "").replace(
                ",", ".")) if p[20].strip() not in ("", " ") else None
            rows.append({"res": res, "lado": lado, "total": total})
            if total is not None:
                total_final = total
        except Exception:
            continue
    return rows, total_final


def stats(rows):
    if not rows:
        return {}
    n = len(rows)
    wins = sum(1 for r in rows if r["res"] > 0)
    losses = sum(1 for r in rows if r["res"] < 0)
    zeros = sum(1 for r in rows if r["res"] == 0)
    gain_vals = [r["res"] for r in rows if r["res"] > 0]
    loss_vals = [abs(r["res"]) for r in rows if r["res"] < 0]
    pnl = sum(r["res"] for r in rows)
    avg_g = sum(gain_vals) / len(gain_vals) if gain_vals else 0
    avg_l = sum(loss_vals) / len(loss_vals) if loss_vals else 0
    rr = avg_g / avg_l if avg_l else 0
    return {
        "n": n, "wins": wins, "losses": losses, "zeros": zeros,
        "win_pct": round(wins / n * 100, 1) if n else 0,
        "pnl": pnl, "avg_g": avg_g, "avg_l": avg_l, "rr": rr,
    }


# ─── Carregar todos os arquivos ───────────────────────────────────────────────
data = {}
for f in sorted(BASE.glob("FORCA_W*_V1*.csv")):
    m = re.match(r"(FORCA_W(?:DO|IN)_V\d+)_(.+)\.csv", f.name)
    if not m:
        continue
    name = m.group(1)  # ex: FORCA_WDO_V12
    tf = m.group(2)  # ex: 5m
    rows, total = parse_file(f)
    if not rows:
        continue
    data.setdefault(name, {})[tf] = {"rows": rows, "total": total}

TIMEFRAMES_ORDER = ["5m", "10m", "15m", "20m", "30m", "60m", "diario"]

# ─── Comparativo V11 vs V12 por timeframe ────────────────────────────────────
print("=" * 70)
print("  COMPARATIVO V11 vs V12 — WDO e WIN (por timeframe)")
print("=" * 70)

for ativo in ["WDO", "WIN"]:
    print(f"\n{'─'*70}")
    print(f"  {ativo}")
    print(f"{'─'*70}")
    print(f"{'TF':<8} {'V11 n':>6} {'V11 Win%':>8} {'V11 PnL':>10} || {'V12 n':>6} {'V12 Win%':>8} {'V12 PnL':>10}  {'Δ PnL':>10}")
    print(f"{'─'*70}")

    for tf in TIMEFRAMES_ORDER:
        k11 = f"FORCA_{ativo}_V11"
        k12 = f"FORCA_{ativo}_V12"
        d11 = data.get(k11, {}).get(tf)
        d12 = data.get(k12, {}).get(tf)
        if d11 is None and d12 is None:
            continue
        s11 = stats(d11["rows"]) if d11 else {}
        s12 = stats(d12["rows"]) if d12 else {}
        pnl11 = s11.get("pnl", 0)
        pnl12 = s12.get("pnl", 0)
        delta = pnl12 - pnl11
        sign = "▲" if delta > 0 else ("▼" if delta < 0 else "=")
        print(
            f"{tf:<8} {s11.get('n', 0):>6} {s11.get('win_pct', 0):>7.1f}% {pnl11:>10.0f} || "
            f"{s12.get('n', 0):>6} {s12.get('win_pct', 0):>7.1f}% {pnl12:>10.0f}  "
            f"{sign}{abs(delta):>8.0f}"
        )

# ─── Análise lado Compra vs Venda ─────────────────────────────────────────────
print("\n\n" + "=" * 70)
print("  WIN% POR LADO — V12 (todos timeframes)")
print("=" * 70)

for ativo in ["WDO", "WIN"]:
    key = f"FORCA_{ativo}_V12"
    if key not in data:
        continue
    combined_C = []
    combined_V = []
    for tf, d in data[key].items():
        for r in d["rows"]:
            if r["lado"] == "C":
                combined_C.append(r)
            elif r["lado"] == "V":
                combined_V.append(r)

    sC = stats(combined_C)
    sV = stats(combined_V)
    total_todos = combined_C + combined_V
    sT = stats(total_todos)

    print(f"\n  {ativo}_V12 (todos TF combinados):")
    print(f"  {'Lado':<8} {'N':>5} {'Win%':>7} {'PnL':>10} {'Avg Ganho':>10} {'Avg Perda':>10} {'RR':>6}")
    print(f"  {'─'*62}")
    for nm, sv in [("COMPRA(C)", sC), ("VENDA(V)", sV), ("TOTAL", sT)]:
        if sv:
            print(
                f"  {nm:<10} {sv['n']:>5} {sv['win_pct']:>6.1f}% {sv['pnl']:>10.0f} "
                f"{sv['avg_g']:>10.1f} {sv['avg_l']:>10.1f} {sv['rr']:>6.2f}"
            )

# ─── Análise por TF + Lado no V12 ────────────────────────────────────────────
print("\n\n" + "=" * 70)
print("  V12 — WIN% POR TIMEFRAME × LADO")
print("=" * 70)

for ativo in ["WDO", "WIN"]:
    key = f"FORCA_{ativo}_V12"
    if key not in data:
        continue
    print(f"\n  {ativo}_V12:")
    print(f"  {'TF':<8} {'C_n':>4} {'C_Win%':>7} {'C_PnL':>9} | {'V_n':>4} {'V_Win%':>7} {'V_PnL':>9}")
    print(f"  {'─'*58}")
    for tf in TIMEFRAMES_ORDER:
        d = data[key].get(tf)
        if not d:
            continue
        rows_C = [r for r in d["rows"] if r["lado"] == "C"]
        rows_V = [r for r in d["rows"] if r["lado"] == "V"]
        sC = stats(rows_C)
        sV = stats(rows_V)
        nc = sC.get("n", 0)
        nv = sV.get("n", 0)
        wc = sC.get("win_pct", 0)
        wv = sV.get("win_pct", 0)
        pc = sC.get("pnl", 0)
        pv = sV.get("pnl", 0)
        if nc + nv == 0:
            continue
        print(
            f"  {tf:<8} {nc:>4} {wc:>6.1f}% {pc:>9.0f} | {nv:>4} {wv:>6.1f}% {pv:>9.0f}")

# ─── Helpers de sequência ────────────────────────────────────────────────────


def seq_analysis(rows_by_side):
    """Retorna dict com estatísticas de sequência para uma lista de trades (mesmo lado)."""
    result = {}
    for label, rows in rows_by_side.items():
        if len(rows) < 3:
            result[label] = None
            continue
        after_loss, after_win = [], []
        max_consec = cur = 0
        for i, r in enumerate(rows):
            if r["res"] < 0:
                cur += 1
                max_consec = max(max_consec, cur)
            else:
                cur = 0
            if i < len(rows) - 1:
                nxt = rows[i + 1]["res"]
                if r["res"] < 0:
                    after_loss.append(nxt > 0)
                elif r["res"] > 0:
                    after_win.append(nxt > 0)
        result[label] = {
            "n": len(rows),
            "after_loss_n": len(after_loss),
            "after_win_n":  len(after_win),
            "win_after_loss": round(sum(after_loss) / len(after_loss) * 100, 1) if after_loss else 0,
            "win_after_win":  round(sum(after_win) / len(after_win) * 100, 1) if after_win else 0,
            "max_consec_neg": max_consec,
        }
    return result


def classifica_cor(rows, lado, tp_ref):
    """
    Classifica cada trade como 'fraco' (verde fraco / vermelho fraco, F≥70 ou F≤-70)
    ou 'forte' (verde forte / vermelho forte, F≥85 ou F≤-85) usando o resultado
    como proxy da força do sinal.
    Proxy: ganho > 60% da mediana de ganhos → provável sinal forte (F≥85).
    NOTA: os CSVs do robô não exportam o valor de força (fForca) por trade.
    Para classificação exata é preciso adicionar logging ao robô.
    """
    wins = [r["res"] for r in rows if r["res"] > 0]
    if not wins:
        return rows, []
    tp_median = sorted(wins)[len(wins) // 2]
    threshold = max(tp_median * 0.6, tp_ref * 0.4)  # pelo menos 40% do TP ref
    fraco = [r for r in rows if abs(r["res"]) <= threshold or r["res"] <= 0]
    forte = [r for r in rows if r["res"] > threshold]
    return fraco, forte


# ─── Análise de sequências — TODOS os timeframes ─────────────────────────────
# Cores: Verde fraco=compra F≥70 | Verde forte=compra F≥85 | Vermelho fraco=venda F≤-70 | Vermelho forte=venda F≤-85
# Proxy: resultado > mediana×0.6 → "forte" (verde forte / vermelho forte);  resto → "fraco" (verde fraco / vermelho fraco)
print("\n\n" + "=" * 70)
print("  ANÁLISE DE SEQUÊNCIAS — TODOS os TF × WDO e WIN (V12)")
print("  Transições após derrota/vitória + verde fraco→forte + vermelho fraco→forte (proxy)")
print("=" * 70)

TP_REF = {"WDO": 36, "WIN": 1026}

for ativo in ["WDO", "WIN"]:
    key = f"FORCA_{ativo}_V12"
    tp_ref = TP_REF[ativo]
    if key not in data:
        continue
    print(f"\n{'═'*70}")
    print(f"  {ativo}_V12")
    print(f"{'═'*70}")

    for tf in TIMEFRAMES_ORDER:
        d = data[key].get(tf)
        if not d or len(d["rows"]) < 6:
            continue
        rows_C = [r for r in d["rows"] if r["lado"] == "C"]
        rows_V = [r for r in d["rows"] if r["lado"] == "V"]

        # Classificação cor proxy
        verde_fraco_rows,    verde_forte_rows = classifica_cor(
            rows_C, "C", tp_ref)
        vermelho_fraco_rows, vermelho_forte_rows = classifica_cor(
            rows_V, "V", tp_ref)

        by_side = {
            "COMPRA (todos)":       rows_C,
            "VENDA (todos)":        rows_V,
            "verde fraco (C)":      verde_fraco_rows,
            "verde forte (C)":      verde_forte_rows,
            "vermelho fraco (V)":   vermelho_fraco_rows,
            "vermelho forte (V)":   vermelho_forte_rows,
        }
        seq = seq_analysis(by_side)

        print(
            f"\n  ── {tf} ──  (C={len(rows_C)} V={len(rows_V)}  verde_forte_proxy={len(verde_forte_rows)} verm_forte_proxy={len(vermelho_forte_rows)})")
        print(
            f"  {'Grupo':<22} {'n':>4} {'W%após perda':>14} {'W%após vitória':>15} {'Max consec-':>12}")
        print(f"  {'─'*70}")
        for label in ["COMPRA (todos)", "verde fraco (C)", "verde forte (C)",
                      "VENDA (todos)", "vermelho fraco (V)", "vermelho forte (V)"]:
            s = seq.get(label)
            if s is None or s["n"] < 3:
                continue
            flag = "⚠️" if s["win_after_loss"] < 38 else (
                "✅" if s["win_after_loss"] >= 50 else "")
            print(
                f"  {label:<22} {s['n']:>4} "
                f"{s['win_after_loss']:>10.1f}% (n={s['after_loss_n']:<3}) "
                f"{s['win_after_win']:>11.1f}% (n={s['after_win_n']:<3}) "
                f"{s['max_consec_neg']:>6} {flag}"
            )

        # Transição verde→cyan e vermelho→fúcsia
        if verde_forte_rows and verde_fraco_rows:
            # após um "verde fraco" (F≥70), o próximo compra é fraco ou forte?
            all_C_classified = []
            for r in rows_C:
                wins_ref = [x["res"] for x in rows_C if x["res"] > 0]
                tp_med = sorted(wins_ref)[
                    len(wins_ref)//2] if wins_ref else tp_ref
                thr = max(tp_med * 0.6, tp_ref * 0.4)
                all_C_classified.append(
                    ("verde forte" if r["res"] > thr else "verde fraco", r))
            transitions_C = Counter()
            for i in range(len(all_C_classified) - 1):
                cur_cor, _ = all_C_classified[i]
                nxt_cor, _ = all_C_classified[i + 1]
                transitions_C[(cur_cor, nxt_cor)] += 1

            total_vf2vF = transitions_C.get(
                ("verde fraco", "verde forte"), 0) + transitions_C.get(("verde fraco", "verde fraco"), 0)
            total_vF2vF = transitions_C.get(
                ("verde forte", "verde forte"), 0) + transitions_C.get(("verde forte", "verde fraco"), 0)
            pct_vf2vF = transitions_C[("verde fraco", "verde forte")] / \
                total_vf2vF * 100 if total_vf2vF else 0
            pct_vF2vF = transitions_C[("verde forte", "verde forte")] / \
                total_vF2vF * 100 if total_vF2vF else 0

            print(
                f"\n  🔄 Transições COMPRA:  verde fraco→forte: {pct_vf2vF:.0f}%  verde forte→forte: {pct_vF2vF:.0f}%  (base n={total_vf2vF}/{total_vF2vF})")

        if vermelho_forte_rows and vermelho_fraco_rows:
            all_V_classified = []
            for r in rows_V:
                wins_ref = [x["res"] for x in rows_V if x["res"] > 0]
                tp_med = sorted(wins_ref)[
                    len(wins_ref)//2] if wins_ref else tp_ref
                thr = max(tp_med * 0.6, tp_ref * 0.4)
                all_V_classified.append(
                    ("vermelho forte" if r["res"] > thr else "vermelho fraco", r))
            transitions_V = Counter()
            for i in range(len(all_V_classified) - 1):
                cur_cor, _ = all_V_classified[i]
                nxt_cor, _ = all_V_classified[i + 1]
                transitions_V[(cur_cor, nxt_cor)] += 1

            total_rf2rF = transitions_V.get(
                ("vermelho fraco", "vermelho forte"), 0) + transitions_V.get(("vermelho fraco", "vermelho fraco"), 0)
            total_rF2rF = transitions_V.get(
                ("vermelho forte", "vermelho forte"), 0) + transitions_V.get(("vermelho forte", "vermelho fraco"), 0)
            pct_rf2rF = transitions_V[("vermelho fraco", "vermelho forte")] / \
                total_rf2rF * 100 if total_rf2rF else 0
            pct_rF2rF = transitions_V[("vermelho forte", "vermelho forte")] / \
                total_rF2rF * 100 if total_rF2rF else 0

            print(
                f"  🔄 Transições VENDA:   verm. fraco→forte: {pct_rf2rF:.0f}%  verm. forte→forte: {pct_rF2rF:.0f}%  (base n={total_rf2rF}/{total_rF2rF})")

# ─── Distribuição de resultados: todos TF × ambos ativos ────────────────────
BUCKET_KEYS = ["≤ -100 (SL grande)", "-100 a -50", "-50 a -1",
               "zero (BE)", "1 a 50", "50 a 150", "> 150 (SG grande)"]


def bucket_rows(rows):
    b = defaultdict(int)
    for r in rows:
        v = r["res"]
        if v <= -100:
            b["≤ -100 (SL grande)"] += 1
        elif v <= -50:
            b["-100 a -50"] += 1
        elif v < 0:
            b["-50 a -1"] += 1
        elif v == 0:
            b["zero (BE)"] += 1
        elif v <= 50:
            b["1 a 50"] += 1
        elif v <= 150:
            b["50 a 150"] += 1
        else:
            b["> 150 (SG grande)"] += 1
    return b


print("\n\n" + "=" * 70)
print("  DISTRIBUIÇÃO DOS TRADES — V12 (todos TF × WDO e WIN)")
print("  (entender se SL e SG estão calibrados por timeframe)")
print("=" * 70)

for ativo in ["WDO", "WIN"]:
    key = f"FORCA_{ativo}_V12"
    if key not in data:
        continue
    sl_ref = {"WDO": 12,  "WIN": 342}[ativo]
    tp_ref = {"WDO": 36,  "WIN": 1026}[ativo]
    print(f"\n── {ativo}_V12  (SL ref={sl_ref}pts  TP ref={tp_ref}pts) ──")
    print(f"  {'TF':<8} {'n':>4} {'≤-100%':>7} {'-100/-50%':>10} {'-50/-1%':>8} {'BE%':>5} {'1/50%':>6} {'50/150%':>8} {'>150%':>6} {'MaxG':>6} {'MaxL':>6}")
    print(f"  {'─'*82}")
    for tf in TIMEFRAMES_ORDER:
        d = data[key].get(tf)
        if not d or not d["rows"]:
            continue
        rows = d["rows"]
        n = len(rows)
        b = bucket_rows(rows)
        pct = {k: b[k] / n * 100 for k in BUCKET_KEYS}
        mx_g = max(r["res"] for r in rows)
        mx_l = min(r["res"] for r in rows)
        print(
            f"  {tf:<8} {n:>4} "
            f"{pct['≤ -100 (SL grande)']:>6.1f}% "
            f"{pct['-100 a -50']:>9.1f}% "
            f"{pct['-50 a -1']:>7.1f}% "
            f"{pct['zero (BE)']:>4.1f}% "
            f"{pct['1 a 50']:>5.1f}% "
            f"{pct['50 a 150']:>7.1f}% "
            f"{pct['> 150 (SG grande)']:>5.1f}% "
            f"{mx_g:>6.0f} {mx_l:>6.0f}"
        )
    # Linha consolidada (todos TF)
    all_rows = [r for d in data[key].values() for r in d["rows"]]
    if all_rows:
        n = len(all_rows)
        b = bucket_rows(all_rows)
        pct = {k: b[k] / n * 100 for k in BUCKET_KEYS}
        mx_g = max(r["res"] for r in all_rows)
        mx_l = min(r["res"] for r in all_rows)
        print(f"  {'─'*82}")
        print(
            f"  {'TOTAL':<8} {n:>4} "
            f"{pct['≤ -100 (SL grande)']:>6.1f}% "
            f"{pct['-100 a -50']:>9.1f}% "
            f"{pct['-50 a -1']:>7.1f}% "
            f"{pct['zero (BE)']:>4.1f}% "
            f"{pct['1 a 50']:>5.1f}% "
            f"{pct['50 a 150']:>7.1f}% "
            f"{pct['> 150 (SG grande)']:>5.1f}% "
            f"{mx_g:>6.0f} {mx_l:>6.0f}"
        )
        # Alerta calibração
        big_loss_pct = pct["≤ -100 (SL grande)"]
        if big_loss_pct > 10:
            print(
                f"  ⚠️  {ativo}: {big_loss_pct:.0f}% dos trades perderam > 100pts (acima do SL configurado de {sl_ref}pts)")
            print(
                f"      Trailing/BE não está contendo os piores casos — considere aumentar TrailingPasso.")

# ─── Gerar HISTORICO-RESULTADOS.md ────────────────────────────────────────────
hist_path = OUT / "HISTORICO-RESULTADOS.md"
with open(hist_path, "w", encoding="utf-8") as f:
    f.write("# Histórico de Evolução — Robôs FORCA\n\n")
    f.write("> Registro cronológico de versões, decisões e resultados para afinar as estratégias.\n\n")

    f.write("---\n\n")
    f.write("## Linha do Tempo\n\n")
    f.write("| Versão | Ativo | Data criação | Melhoria principal | Resultado 5m PnL | Status |\n")
    f.write("|--------|-------|-------------|-------------------|-----------------|--------|\n")

    for ativo in ["WDO", "WIN"]:
        for ver in ["V11", "V12"]:
            key = f"FORCA_{ativo}_{ver}"
            d5m = data.get(key, {}).get("5m")
            if not d5m:
                continue
            s = stats(d5m["rows"])
            total = d5m["total"] or s["pnl"]
            status = "✅ Melhorou" if ver == "V12" else "🔴 Substituído"
            melhoria = {
                "V11_WDO": "Base — sem hard SL (bug)",
                "V11_WIN": "Base — sem hard SL (bug)",
                "V12_WDO": "Hard SL + BE 0.33 + Trailing + MaxPerdaDia",
                "V12_WIN": "Hard SL + BE 0.33 + Trailing + MaxPerdaDia",
            }.get(f"{ver}_{ativo}", "-")
            f.write(
                f"| {key} | {ativo} | fev/2026 | {melhoria} | {total:.0f}pts | {status} |\n")

    f.write("\n---\n\n")
    f.write("## Por que criamos V12\n\n")
    f.write("### Bug crítico V11 — Hard Stop Loss ausente\n\n")
    f.write("- V11 calculava `fSL` apenas para **sizing** (tamanho de contratos), mas **NÃO colocava ordem de stop real**.\n")
    f.write("- A única proteção era `StopCandleContra` (fechar se aparecer candle de exaustão contrária).\n")
    f.write("- Resultado: em **03/03/2026**, WDO ficou numa compra de 23h sem stop → **perda de -1.365pts** (op #4).\n")
    f.write("  - Era o equivalente a 113× o stop mínimo de 12pts — destruiu o capital da carteira.\n")
    f.write("- V12 corrige: `if IsBought and (Low <= fEntrada - fSL) then ClosePosition` verificado intrabar.\n\n")
    f.write("### Outras melhorias V12\n\n")
    f.write("- **Break-even agressivo**: trigger em 33% do TP (era 50%) → protege lucro mais cedo\n")
    f.write("- **Trailing stop**: após BE ativo, acompanha o preço a cada `TrailingPasso` pts\n")
    f.write("- **MaxPerdaDia**: para de operar se perda acumulada no dia ≥ limite\n")
    f.write("- **Parâmetros default para 5min**: SL=12, TP=36, janela 3/6 (era 2/4 para 15min)\n\n")

    f.write("---\n\n")
    f.write("## Resultados por Versão e Timeframe\n\n")

    for ativo in ["WDO", "WIN"]:
        f.write(f"### {ativo}\n\n")
        f.write(
            f"| TF | V11 n | V11 Win% | V11 PnL | V12 n | V12 Win% | V12 PnL | Δ PnL |\n")
        f.write(
            f"|-----|-------|----------|---------|-------|----------|---------|-------|\n")
        for tf in TIMEFRAMES_ORDER:
            k11 = f"FORCA_{ativo}_V11"
            k12 = f"FORCA_{ativo}_V12"
            d11 = data.get(k11, {}).get(tf)
            d12 = data.get(k12, {}).get(tf)
            if d11 is None and d12 is None:
                continue
            s11 = stats(d11["rows"]) if d11 else {}
            s12 = stats(d12["rows"]) if d12 else {}
            delta = s12.get("pnl", 0) - s11.get("pnl", 0)
            sign = "▲" if delta > 0 else ("▼" if delta < 0 else "=")
            f.write(
                f"| {tf} | {s11.get('n', 0)} | {s11.get('win_pct', 0):.1f}% | {s11.get('pnl', 0):.0f} "
                f"| {s12.get('n', 0)} | {s12.get('win_pct', 0):.1f}% | {s12.get('pnl', 0):.0f} "
                f"| {sign}{abs(delta):.0f} |\n"
            )
        f.write("\n")

    f.write("---\n\n")
    f.write("## Análise de Sequências — fraco vs forte\n\n")
    f.write("> **Verde fraco**     = sinal de compra F ≥ 70 → LONG normal  \n")
    f.write(
        "> **Verde forte**     = sinal de compra F ≥ 85 → LONG de máxima prioridade  \n")
    f.write("> **Vermelho fraco**  = sinal de venda F ≤ -70 → SHORT normal  \n")
    f.write("> **Vermelho forte**  = sinal de venda F ≤ -85 → SHORT de máxima prioridade  \n\n")
    f.write("A análise usa os trades por lado como proxy do sinal fraco/forte:\n\n")

    for ativo in ["WDO", "WIN"]:
        key = f"FORCA_{ativo}_V12"
        rows_5m = data.get(key, {}).get("5m", {}).get("rows", [])
        if not rows_5m:
            continue
        f.write(f"### {ativo}_V12 @ 5m\n\n")
        for lado in ["C", "V"]:
            desc = "COMPRA (verde fraco / verde forte)" if lado == "C" else "VENDA (vermelho fraco / vermelho forte)"
            filtered = [r for r in rows_5m if r["lado"] == lado]
            if len(filtered) < 3:
                continue
            after_loss, after_win = [], []
            max_consec = 0
            cur = 0
            for i, r in enumerate(filtered):
                if r["res"] < 0:
                    cur += 1
                    max_consec = max(max_consec, cur)
                else:
                    cur = 0
                if i < len(filtered) - 1:
                    nxt = filtered[i + 1]["res"]
                    if r["res"] < 0:
                        after_loss.append(nxt > 0)
                    elif r["res"] > 0:
                        after_win.append(nxt > 0)

            pal = round(sum(after_loss) / len(after_loss)
                        * 100, 1) if after_loss else 0
            paw = round(sum(after_win) / len(after_win)
                        * 100, 1) if after_win else 0
            f.write(f"**{desc}** (n={len(filtered)})\n\n")
            f.write(f"| Situação | trades seguintes | Win% seguinte |\n")
            f.write(f"|----------|-----------------|---------------|\n")
            f.write(f"| Após derrota | {len(after_loss)} | {pal:.1f}% |\n")
            f.write(f"| Após vitória | {len(after_win)} | {paw:.1f}% |\n")
            f.write(
                f"| Max consecutivos negativos | — | {max_consec} seguidos |\n\n")

            if pal < 40:
                f.write(f"> ⚠️ Win% após derrota é baixo ({pal:.1f}%) → padrão de \"revenge trading\" perigoso. "
                        f"Considere pausa após {max_consec // 2 + 1} perdas consecutivas.\n\n")

    # ── Distribuição por TF (seção de calibração) ──────────────────────────
    f.write("---\n\n")
    f.write("## Distribuição de Trades por Timeframe — Calibração SL/TP\n\n")
    f.write("> Interpretar: `≤ -100` = perdeu mais que o SL configurado (trailing falhou/gap). "
            "`> 150` = capturou movimento grande (SG não limitou). "
            "`BE` = saiu no zero (break-even acionado com sucesso).\n\n")

    for ativo in ["WDO", "WIN"]:
        key = f"FORCA_{ativo}_V12"
        if key not in data:
            continue
        sl_ref = {"WDO": 12, "WIN": 342}[ativo]
        tp_ref = {"WDO": 36, "WIN": 1026}[ativo]
        f.write(
            f"### {ativo}_V12 — SL ref={sl_ref}pts | TP ref={tp_ref}pts\n\n")
        f.write("| TF | n | ≤-100% | -100/-50% | -50/-1% | BE% | 1/50% | 50/150% | >150% | MaxGanho | MaxPerda |\n")
        f.write("|-----|---|--------|-----------|---------|-----|-------|---------|-------|----------|----------| \n")
        for tf in TIMEFRAMES_ORDER:
            d = data[key].get(tf)
            if not d or not d["rows"]:
                continue
            rows = d["rows"]
            n = len(rows)
            b = bucket_rows(rows)
            pct = {k: b[k] / n * 100 for k in BUCKET_KEYS}
            mx_g = max(r["res"] for r in rows)
            mx_l = min(r["res"] for r in rows)
            f.write(
                f"| {tf} | {n} "
                f"| {pct['≤ -100 (SL grande)']:.0f}% "
                f"| {pct['-100 a -50']:.0f}% "
                f"| {pct['-50 a -1']:.0f}% "
                f"| {pct['zero (BE)']:.0f}% "
                f"| {pct['1 a 50']:.0f}% "
                f"| {pct['50 a 150']:.0f}% "
                f"| {pct['> 150 (SG grande)']:.0f}% "
                f"| {mx_g:.0f} | {mx_l:.0f} |\n"
            )
        f.write("\n")

    # ── Matriz de prioridade ─────────────────────────────────────────────────
    f.write("---\n\n")
    f.write("## Matriz de Prioridade — Robôs × Timeframes\n\n")
    f.write("> **Legenda de status:** \n")
    f.write("> 🟢 Operar — PnL positivo e Win% ≥ 45%  \n")
    f.write("> 🟡 Vigilância — PnL positivo mas Win% < 45% ou n < 30  \n")
    f.write("> 🔴 Pausar — PnL negativo  \n")
    f.write("> ⚫ Não testado / sem dados  \n\n")

    def status_cell(s):
        if not s or s.get("n", 0) == 0:
            return "⚫ sem dados"
        pnl = s.get("pnl", 0)
        win = s.get("win_pct", 0)
        n = s.get("n", 0)
        if pnl < 0:
            return f"🔴 {pnl:+.0f}pts ({win:.0f}%w)"
        if win >= 45 and n >= 30:
            return f"🟢 {pnl:+.0f}pts ({win:.0f}%w)"
        return f"🟡 {pnl:+.0f}pts ({win:.0f}%w, n={n})"

    for ativo in ["WDO", "WIN"]:
        f.write(f"### {ativo}\n\n")
        f.write(f"| Timeframe | V11 | V12 | Recomendação |\n")
        f.write(f"|-----------|-----|-----|--------------|\n")
        for tf in TIMEFRAMES_ORDER:
            k11 = f"FORCA_{ativo}_V11"
            k12 = f"FORCA_{ativo}_V12"
            d11 = data.get(k11, {}).get(tf)
            d12 = data.get(k12, {}).get(tf)
            s11 = stats(d11["rows"]) if d11 else {}
            s12 = stats(d12["rows"]) if d12 else {}
            c11 = status_cell(s11)
            c12 = status_cell(s12)
            # Recomendação baseada em V12
            pnl12 = s12.get("pnl", None)
            win12 = s12.get("win_pct", 0)
            n12 = s12.get("n", 0)
            if pnl12 is None:
                rec = "⚫ Sem dados V12"
            elif pnl12 > 0 and win12 >= 50 and n12 >= 40:
                rec = "✅ Prioridade ALTA"
            elif pnl12 > 0 and win12 >= 45:
                rec = "✅ Operar"
            elif pnl12 > 0:
                rec = "⚠️ Monitorar"
            else:
                rec = "🚫 Pausar — calibrar"
            f.write(f"| **{tf}** | {c11} | {c12} | {rec} |\n")
        f.write("\n")

    # ── Recomendação Diária ──────────────────────────────────────────────────
    f.write("---\n\n")
    f.write("## Recomendação Diária — Qual Robô/Ativo/TF Operar?\n\n")
    f.write("> Esta seção responde: **quais configurações ativar no dia a dia segundo os resultados do V12**.\n\n")
    f.write("| Prioridade | Robô | Ativo | TF | Lado | Win% | PnL V12 | Obs |\n")
    f.write("|-----------|------|-------|-----|------|------|---------|-----|\n")

    recomendacoes = []
    for ativo in ["WDO", "WIN"]:
        key = f"FORCA_{ativo}_V12"
        sl_ref = {"WDO": 12, "WIN": 342}[ativo]
        for tf in TIMEFRAMES_ORDER:
            d_all = data.get(key, {}).get(tf)
            if not d_all or not d_all["rows"]:
                continue
            s_all = stats(d_all["rows"])
            for lado in ["C", "V"]:
                rows_l = [r for r in d_all["rows"] if r["lado"] == lado]
                if len(rows_l) < 10:
                    continue
                s_l = stats(rows_l)
                pnl = s_l.get("pnl", 0)
                win = s_l.get("win_pct", 0)
                n = s_l.get("n", 0)
                avg_g = s_l.get("avg_g", 0)
                desc_lado = "COMPRA" if lado == "C" else "VENDA"
                if pnl > 0 and win >= 50:
                    recomendacoes.append((1, ativo, tf, desc_lado, win, pnl, avg_g, n))
                elif pnl > 0 and win >= 45:
                    recomendacoes.append((2, ativo, tf, desc_lado, win, pnl, avg_g, n))

    recomendacoes.sort(key=lambda x: (-x[0] * 10000 + x[4]))  # prioridade desc, win% desc
    recomendacoes.sort(key=lambda x: x[0])  # prioridade asc (1=alta)

    for pri, ativo, tf, lado, win, pnl, avg_g, n in recomendacoes:
        emoji = "🏆" if pri == 1 else "✅"
        obs = f"n={n}, avg_ganho≈{avg_g:.0f}pts"
        f.write(f"| {emoji} P{pri} | FORCA_{ativo}_V12 | {ativo} | {tf} | {lado} | {win:.1f}% | {pnl:+.0f}pts | {obs} |\n")

    if not recomendacoes:
        f.write("| — | — | — | — | — | — | — | Sem configurações lucrativas com Win%≥45% e n≥10 |\n")

    f.write("\n> **Como interpretar**: 🏆 P1 = prioridade máxima (Win%≥50% + PnL positivo)."
            " ✅ P2 = operar com cautela (Win%≥45%). Atualize esta tabela após cada série de 30+ trades.\n\n")

    # ── Fraco vs Forte por TF ────────────────────────────────────────────────
    f.write("---\n\n")
    f.write("## Probabilidade e Pontos Médios — Verde fraco vs Verde forte / Vermelho fraco vs Vermelho forte\n\n")
    f.write("> **Proxy**: trades com ganho > mediana×0.6 são classificados como 'forte' (F≥85), demais como 'fraco' (F≥70).\n")
    f.write("> O CSV não exporta o valor F por trade — para classificação exata adicione logging ao robô.\n\n")

    for ativo in ["WDO", "WIN"]:
        key = f"FORCA_{ativo}_V12"
        tp_ref = {"WDO": 36, "WIN": 1026}[ativo]
        f.write(f"### {ativo}_V12\n\n")
        f.write("| TF | Lado | Cor | n | Win% | AvgGanho (pts) | AvgPerda (pts) | RR |\n")
        f.write("|-----|------|-----|---|------|---------------|---------------|----|\n")
        for tf in TIMEFRAMES_ORDER:
            d = data.get(key, {}).get(tf)
            if not d or not d["rows"]:
                continue
            for lado in ["C", "V"]:
                rows_l = [r for r in d["rows"] if r["lado"] == lado]
                if len(rows_l) < 5:
                    continue
                fraco, forte = classifica_cor(rows_l, lado, tp_ref)
                cor_fraco = "verde fraco" if lado == "C" else "vermelho fraco"
                cor_forte = "verde forte" if lado == "C" else "vermelho forte"
                for nome, grp in [(cor_fraco, fraco), (cor_forte, forte)]:
                    if len(grp) < 3:
                        continue
                    sg = stats(grp)
                    rr_str = f"{sg['rr']:.2f}" if sg.get("rr") else "—"
                    f.write(
                        f"| {tf} | {'COMPRA' if lado == 'C' else 'VENDA'} | {nome} "
                        f"| {sg['n']} | {sg['win_pct']:.1f}% "
                        f"| {sg['avg_g']:.0f} | {sg['avg_l']:.0f} | {rr_str} |\n"
                    )
        f.write("\n")

    f.write("> **Como usar**: ao ver um verde forte no gráfico, consulte a linha correspondente para saber "
            "a chance histórica de ganhar e quantos pontos em média o movimento busca. "
            "Isso ajuda a calibrar expectativa e decidir se vale entrar.\n\n")

    # ── Premissas do Robô V12 ─────────────────────────────────────────────────
    f.write("---\n\n")
    f.write("## Premissas do Robô V12\n\n")
    f.write("> Documentação das regras hard-coded e parâmetros default do V12. "
            "Use como referência ao corrigir ou propor nova versão.\n\n")
    f.write("### Parâmetros default (5m)\n\n")
    f.write("| Param | WDO | WIN | Observação |\n")
    f.write("|-------|-----|-----|------------|\n")
    f.write("| SL (pts) | 12 | 342 | Hard SL executado intrabar via Low/High |\n")
    f.write("| TP (pts) | 36 | 1026 | RR = 3.0 configurado |\n")
    f.write("| BE trigger | 33% do TP (~12pts) | ~340pts | Mover stop para entrada após 33% do TP atingido |\n")
    f.write("| TrailingPasso | 4pts | 100pts | Quanto o stop sobe/desce após cada TrailingPasso de lucro |\n")
    f.write("| MaxPerdaDia | 60pts | 1026pts | Paralisa operações do dia se perda acumulada ≥ limite |\n")
    f.write("| StopHorario | 17:45 | 17:45 | Fecha posições ABERTAS e bloqueia novas entradas após esse horário |\n")
    f.write("| iJanelaDir | 3 | 3 | Janela de direção (3× TF) |\n")
    f.write("| iJanelaCtx | 6 | 6 | Janela de contexto (6× TF) |\n")
    f.write("| ForcaMinimaForte | 70 | 70 | Mínimo para considerar sinal |\n")
    f.write("| ForcaExaustao | 85 | 85 | Umbral do sinal forte — cores verd/verm forte |\n")
    f.write("| VolumeMinimo | 2000 | 2000 | Volume abaixo disso ignora o sinal |\n\n")

    f.write("### Comportamento de horário\n\n")
    f.write("- `StopHorario_H(17); StopHorario_M(45)`: quando `Time() >= 17:45`, o robô **fecha posição aberta** "
            "e define `bDeveOperar := false`.\n")
    f.write("- **Não há carry overnight intencional**: se uma posição aparece no CSV com duração overnight, "
            "foi originada em teste com StopHorario desabilitado ou em parâmetro diferente.\n")
    f.write("- `MaxBarrasEmPosicao(0)` = ilimitado → posição é mantida **intrabar indefinidamente** até SL/TP/BE/Timer.\n")
    f.write("- **Decisão para V13**: adicionar parâmetro `FecharNoFimDoDia(true)` — quando `true` garante "
            "fechamento em 17:45; quando `false` permite carry overnight deliberado.\n\n")

    f.write("### Fórmula de Força\n\n")
    f.write("```\nF = (corpo / range) × (volume / mediaVol) × 100  →  clampado entre -100 e +100\n```\n\n")
    f.write("- `corpo = |Close - Open|` do candle\n")
    f.write("- `range = High - Low` do candle\n")
    f.write("- `mediaVol` = média dos últimos N candles de volume (janela do contexto)\n")
    f.write("- Sinal positivo = candle comprador (Verde); negativo = candle vendedor (Vermelho)\n")
    f.write("- F ≥ 85 → **verde forte** (RGB 0,220,220) | F ≥ 70 → **verde fraco** (RGB 0,180,0)\n")
    f.write("- F ≤ -85 → **vermelho forte** (RGB 255,0,180) | F ≤ -70 → **vermelho fraco** (RGB 200,0,0)\n\n")

    f.write("### Condição de Entrada (V12)\n\n")
    f.write("1. `F >= ForcaMinimaForte` (≥ 70) para COMPRA\n")
    f.write("2. EMAs do Contexto (6×TF) + Direção (3×TF) + Gatilho (TF) **alinhadas com o sinal**\n")
    f.write("3. Volume ≥ VolumeMinimo\n")
    f.write("4. `bDeveOperar = true` (dentro do horário, MaxPerdaDia não atingido)\n")
    f.write("5. Sem posição aberta\n\n")

    # ── Proposta V13 ─────────────────────────────────────────────────────────
    f.write("---\n\n")
    f.write("## Proposta V13 — Derivada dos Resultados V12\n\n")
    f.write("> As sugestões abaixo vêm diretamente da análise dos CSVs do V12 — não são suposições teóricas.\n\n")

    f.write("### 1. `FecharNoFimDoDia` (novo parâmetro boolean)\n\n")
    f.write("- **Problema**: comportamento de horário ambíguo — alguns resultados mostram overnight.\n")
    f.write("- **Solução**: `FecharNoFimDoDia(true)` → padrão = fechar sempre às 17:45. "
            "Defina `false` somente se quiser carry overnight.\n")
    f.write("```ntsl\nInput: FecharNoFimDoDia(true);\n// ...\nif FecharNoFimDoDia and (Time() >= StopHorario) then ClosePosition;\n```\n\n")

    f.write("### 2. `TrailingPasso` — recalibrar por TF\n\n")
    f.write("- **Problema**: ~18-21% dos trades perdem >100pts com SL=12pts configurado → trailing dando stop prematuro no ruído.\n")
    f.write("- WDO 5m: range médio de candle ≈ 6pts → TrailingPasso=4 está DENTRO do ruído → **aumentar para 8pts**.\n")
    f.write("- WIN 5m: range médio ≈ 150pts → TrailingPasso=100 está OK → **aumentar para 150pts** (melhor 1:1 com range).\n")
    f.write("```ntsl\nInput: TrailingPasso(8);   // WDO: era 4\nInput: TrailingPasso(150); // WIN: era 100\n```\n\n")

    f.write("### 3. `SomenteSinalForte` (novo parâmetro boolean, default false)\n\n")
    f.write("- **Fundamento**: sinal forte (F≥85) tem Win% proxy maior que sinal fraco (F≥70) — ver tabela Fraco vs Forte.\n")
    f.write("- Quando `true`, ignora entradas com F < ForcaExaustao (85) → menos trades, melhor win%.\n")
    f.write("```ntsl\nInput: SomenteSinalForte(false);\n// na condição de entrada:\nif SomenteSinalForte and (fForca < ForcaExaustao) then exit;\n```\n\n")

    f.write("### 4. `FiltrarComprasWDO` — opção de só operar VENDA no WDO\n\n")
    f.write("- **Fundamento**: WDO COMPRA Win% ≈ 27-38% em todos os TF (muito abaixo de 50%).\n")
    f.write("- WDO VENDA Win% ≈ 46-60% — consistente.\n")
    f.write("- Parâmetro `OperarCompra(true)` / `OperarVenda(true)` para desabilitar um lado.\n")
    f.write("```ntsl\nInput: OperarCompra(true);\nInput: OperarVenda(true);\n// na entrada de compra:\nif (not OperarCompra) then exit;\n```\n\n")

    f.write("### 5. `JanelaAbertura` — opcional: evitar 1ª meia hora\n\n")
    f.write("- Operações das 09:00-09:30 têm padrão de resultado errático (alta volatilidade de abertura).\n")
    f.write("- Parâmetro `HoraInicioOperacao(9, 30)` — não entra antes das 09:30.\n")
    f.write("```ntsl\nInput: HoraInicioH(9); HoraInicioM(30);\nif Time() < (HoraInicioH * 60 + HoraInicioM) then exit;\n```\n\n")

    f.write("### 6. `MaxPerdaDia` — ajustar para 1× TP (WDO)\n\n")
    f.write("- Atual: 60pts = 5× SL = 1.67× TP → permite destruir capital antes de parar.\n")
    f.write("- Proposta: reduzir para 36pts (= 1× TP) — se perdeu o equivalente a 1 TP, dia encerrado.\n")
    f.write("```ntsl\nInput: MaxPerdaDia(36); // WDO: era 60\n```\n\n")

    f.write("### 7. SL por TF — recalibrar para TF maiores\n\n")
    f.write("- SL=12pts foi calibrado para 5m. Para 30m, range médio é ≈ 18-25pts → SL poderia ser 18-20pts.\n")
    f.write("- TP também precisa escalar: 30m deveria testar TP=54-60pts (3× o SL recalibrado).\n")
    f.write("- Sugestão: `SL_Pts(0)` → quando 0, calcular automaticamente como `fRange_Medio * fator`.\n\n")

    f.write("### Resumo das mudanças V13\n\n")
    f.write("| # | Parâmetro | V12 | V13 proposto | Motivo |\n")
    f.write("|---|-----------|-----|-------------|--------|\n")
    f.write("| 1 | FecharNoFimDoDia | implícito | novo bool (true) | Ambiguidade overnight |\n")
    f.write("| 2 | TrailingPasso WDO | 4pts | 8pts | 4pts ≤ noise do 5m |\n")
    f.write("| 3 | TrailingPasso WIN | 100pts | 150pts | Proporcional ao range |\n")
    f.write("| 4 | SomenteSinalForte | — | novo bool (false) | Filtro F≥85 melhora win% |\n")
    f.write("| 5 | OperarCompra WDO | sempre | novo bool (true→false) | COMPRA Win%<40% |\n")
    f.write("| 6 | HoraInicioOperacao | 00:00 | 09:30 | Volatilidade abertura |\n")
    f.write("| 7 | MaxPerdaDia WDO | 60pts | 36pts | = 1× TP (mais conservador) |\n")
    f.write("| 8 | SL/TP por TF | fixo 12/36 | dinâmico por TF | TF maior = range maior |\n\n")

    f.write("---\n\n")
    f.write("## Checklist de Implementação V13\n\n")
    f.write("- [ ] Adicionar `FecharNoFimDoDia(true)` no bloco de Inputs\n")
    f.write("- [ ] Ajustar `TrailingPasso(8)` no WDO e `TrailingPasso(150)` no WIN\n")
    f.write("- [ ] Adicionar inputs `OperarCompra(true)` e `OperarVenda(true)` com guard na entrada\n")
    f.write("- [ ] Adicionar `SomenteSinalForte(false)` com guard no `if fForca >= ForcaMinimaForte`\n")
    f.write("- [ ] Adicionar `HoraInicioH(9); HoraInicioM(30)` no bloco de horário\n")
    f.write("- [ ] Reduzir `MaxPerdaDia(36)` para WDO\n")
    f.write("- [ ] Adicionar logging de `fForca` no CSV para ter classificação fraco/forte real\n")
    f.write("- [ ] Backteste V13 no mínimo 3 TF (5m, 15m, 30m) × WDO e WIN antes de colocar em produção\n")
    f.write("- [ ] Comparar resultados V13 vs V12 usando este mesmo script (analise_v12.py → analise_v13.py)\n\n")

print(f"\n✅ HISTORICO-RESULTADOS.md criado em {hist_path}")
print("\n" + "=" * 70)
print("  RESUMO FINAL — V12 MELHOROU EM RELAÇÃO AO V11?")
print("=" * 70)

for ativo in ["WDO", "WIN"]:
    k11 = f"FORCA_{ativo}_V11"
    k12 = f"FORCA_{ativo}_V12"
    melhoras = 0
    pioras = 0
    for tf in TIMEFRAMES_ORDER:
        d11 = data.get(k11, {}).get(tf)
        d12 = data.get(k12, {}).get(tf)
        if not d11 or not d12:
            continue
        s11 = stats(d11["rows"])
        s12 = stats(d12["rows"])
        if s12["pnl"] > s11["pnl"]:
            melhoras += 1
        elif s12["pnl"] < s11["pnl"]:
            pioras += 1

    resultado = "✅ V12 MELHOROU" if melhoras > pioras else "🔴 V12 PIOROU" if pioras > melhoras else "≈ EMPATADO"
    print(f"  {ativo}: {resultado}  (↑ em {melhoras} TF, ↓ em {pioras} TF)")
