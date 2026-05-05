"""
Análise completa: FORCA_WDO_V12 + FORCA_WIN_V12 vs V11
- Comparativo por timeframe
- Win/loss por lado (Compra/Venda)
- Transições de cor: vermelho→fúcsia (sequência de derrotas / momentum)
- Gera HISTORICO-RESULTADOS.md e ANALISE-V12.md
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

# ─── Análise de sequências: vermelho→fúcsia ──────────────────────────────────
# Vermelho: sinal de VENDA (V) = momentum vendedor (F ≤ -70)
# Fúcsia:   sinal de VENDA extremo (F ≤ -85) — no resultado = maior resultado positivo
# Proxy: usamos "após uma VENDA com ganho alto > media, o próximo trade V também ganha?"
# Análise de transições: perda → próximo trade / ganho → próximo trade
print("\n\n" + "=" * 70)
print("  ANÁLISE DE SEQUÊNCIAS — Probabilidade após DERROTA / VITÓRIA")
print("  (equivalente a: chance de vermelho→fúcsia continuar / reverter)")
print("=" * 70)

for ativo in ["WDO", "WIN"]:
    key = f"FORCA_{ativo}_V12"
    if key not in data:
        continue

    # Aggregar 5m (mais estatísticas)
    rows_5m = data[key].get("5m", {}).get("rows", [])
    if not rows_5m:
        continue

    print(f"\n  {ativo}_V12 @ 5m — Transições entre trades:")
    for lado in ["C", "V"]:
        desc = "COMPRA" if lado == "C" else "VENDA (vermelho/fúcsia)"
        filtered = [r for r in rows_5m if r["lado"] == lado]
        if len(filtered) < 3:
            continue

        after_loss = []    # próximo resultado após derrota
        after_win = []    # próximo resultado após vitória

        for i in range(len(filtered) - 1):
            cur = filtered[i]["res"]
            nxt = filtered[i + 1]["res"]
            if cur < 0:
                after_loss.append(nxt > 0)
            elif cur > 0:
                after_win.append(nxt > 0)

        # Max drawdown consecutivo
        max_consec_loss = 0
        cur_loss = 0
        for r in filtered:
            if r["res"] < 0:
                cur_loss += 1
                max_consec_loss = max(max_consec_loss, cur_loss)
            else:
                cur_loss = 0

        pct_win_after_loss = round(
            sum(after_loss) / len(after_loss) * 100, 1) if after_loss else 0
        pct_win_after_win = round(
            sum(after_win) / len(after_win) * 100, 1) if after_win else 0

        print(f"\n  [{ativo} {desc}]")
        print(
            f"    Após derrota  → win% próximo: {pct_win_after_loss:.1f}%  (n={len(after_loss)})")
        print(
            f"    Após vitória  → win% próximo: {pct_win_after_win:.1f}%  (n={len(after_win)})")
        print(f"    Max consecutivos negativos: {max_consec_loss}")

# ─── Distribuição de resultados: todos TF × ambos ativos ────────────────────
BUCKET_KEYS = ["≤ -100 (SL grande)", "-100 a -50", "-50 a -1", "zero (BE)", "1 a 50", "50 a 150", "> 150 (SG grande)"]

def bucket_rows(rows):
    b = defaultdict(int)
    for r in rows:
        v = r["res"]
        if v <= -100:   b["≤ -100 (SL grande)"] += 1
        elif v <= -50:  b["-100 a -50"] += 1
        elif v < 0:     b["-50 a -1"] += 1
        elif v == 0:    b["zero (BE)"] += 1
        elif v <= 50:   b["1 a 50"] += 1
        elif v <= 150:  b["50 a 150"] += 1
        else:           b["> 150 (SG grande)"] += 1
    return b

print("\n\n" + "=" * 70)
print("  DISTRIBUIÇÃO DOS TRADES — V12 (todos TF × WDO e WIN)")
print("  (entender se SL e SG estão calibrados por timeframe)")
print("=" * 70)

for ativo in ["WDO", "WIN"]:
    key = f"FORCA_{ativo}_V12"
    if key not in data:
        continue
    sl_ref  = {"WDO": 12,  "WIN": 342}[ativo]
    tp_ref  = {"WDO": 36,  "WIN": 1026}[ativo]
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
            print(f"  ⚠️  {ativo}: {big_loss_pct:.0f}% dos trades perderam > 100pts (acima do SL configurado de {sl_ref}pts)")
            print(f"      Trailing/BE não está contendo os piores casos — considere aumentar TrailingPasso.")

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
    f.write("## Análise de Sequências — vermelho→fúcsia\n\n")
    f.write("> **Vermelho** = sinal de venda forte (F ≤ -70) → entrada SHORT\n")
    f.write("> **Fúcsia**   = sinal de venda extremo (F ≤ -85) → SHORT de máxima prioridade\n\n")
    f.write("A análise de sequência usa os trades de VENDA (V) como proxy do sinal vermelho/fúcsia:\n\n")

    for ativo in ["WDO", "WIN"]:
        key = f"FORCA_{ativo}_V12"
        rows_5m = data.get(key, {}).get("5m", {}).get("rows", [])
        if not rows_5m:
            continue
        f.write(f"### {ativo}_V12 @ 5m\n\n")
        for lado in ["C", "V"]:
            desc = "COMPRA (verde/cyan)" if lado == "C" else "VENDA (vermelho/fúcsia)"
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
        f.write(f"### {ativo}_V12 — SL ref={sl_ref}pts | TP ref={tp_ref}pts\n\n")
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
        n   = s.get("n", 0)
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
            n12   = s12.get("n", 0)
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

    f.write("---\n\n")
    f.write("## Checklist para próxima versão (V13)\n\n")
    f.write("- [ ] Analisar se MaxPerdaDia está muito amplo (precisa calibrar)\n")
    f.write(
        "- [ ] Verificar se TrailingPasso=4 WDO é muito pequeno (noise de 4pts no 5min)\n")
    f.write(
        "- [ ] Testar se filtro de volume VolumeMinimo=2000 está eliminando bons trades\n")
    f.write(
        "- [ ] Considerar horário de operação mais restrito (evitar abertura e os últimos 30min)\n")
    f.write(
        "- [ ] WIN: avaliar se SL=342pts está correto — max perda registrada nos resultados\n")
    f.write(
        "- [ ] Backteste com fúcsia exclusivo (só trades F ≥ 85) vs todos (F ≥ 70)\n\n")

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
