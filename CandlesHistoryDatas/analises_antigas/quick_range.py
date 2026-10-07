import statistics

def pf(s):
    s = str(s).strip()
    if 'E' in s or 'e' in s:
        return float(s.replace(',', '.'))
    return float(s.replace('.', '').replace(',', '.'))

rows = []
with open('2026/WINM26_F_0_Diário.csv', encoding='utf-8') as f:
    for line in f:
        p = line.strip().split(';')
        if len(p) < 6:
            continue
        try:
            rows.append({
                'date':  p[1],
                'open':  pf(p[2]),
                'high':  pf(p[3]),
                'low':   pf(p[4]),
                'close': pf(p[5]),
            })
        except Exception:
            pass

from datetime import datetime as _dt
rows = sorted(rows, key=lambda x: _dt.strptime(x['date'], '%d/%m/%Y'))
ranges_all = [r['high'] - r['low'] for r in rows]
pct_all    = [(r['high'] - r['low']) / r['open'] * 100 for r in rows]
ranges_s   = sorted(ranges_all)
pct_s      = sorted(pct_all)
n = len(ranges_s)

med   = statistics.median(ranges_s)
mean  = sum(ranges_s) / n
p25   = ranges_s[int(n * 0.25)]
p75   = ranges_s[int(n * 0.75)]
p90   = ranges_s[int(n * 0.90)]
pct_med = statistics.median(pct_s)
pct_p75 = pct_s[int(n * 0.75)]
pct_p90 = pct_s[int(n * 0.90)]

last = rows[-1]['close']

# Hoje: queda de 1.62% (usuario informou)
move_pct = 1.62
move_pts = last * (move_pct / 100)

SL, TP, BE = 822, 2466, 1233

print(f"=== RANGE DIARIO WIN — {n} dias uteis (2026) ===")
print(f"  Mediana      : {med:.0f} pts  ({pct_med:.2f}%)")
print(f"  Media        : {mean:.0f} pts")
print(f"  P25 (calmo)  : {p25:.0f} pts")
print(f"  P75 (normal) : {p75:.0f} pts  ({pct_p75:.2f}%)")
print(f"  P90 (volatil): {p90:.0f} pts  ({pct_p90:.2f}%)")
print()
print(f"=== HOJE: queda de {move_pct}% | ref close ontem = {last:.0f} ===")
print(f"  Move em pts          : {move_pts:.0f} pts")
print(f"  vs mediana ({med:.0f})    : {move_pts/med*100:.0f}% consumido")
print(f"  vs P75     ({p75:.0f})    : {move_pts/p75*100:.0f}% consumido")
print(f"  vs P90     ({p90:.0f})    : {move_pts/p90*100:.0f}% consumido")
print()
remaining_med = med - move_pts
remaining_p75 = p75 - move_pts
remaining_p90 = p90 - move_pts
print(f"  Range restante (vs mediana) : {remaining_med:.0f} pts")
print(f"  Range restante (vs P75)     : {remaining_p75:.0f} pts")
print(f"  Range restante (vs P90)     : {remaining_p90:.0f} pts")
print()
print(f"=== VEREDICTO PARA SINAL V14 ===")
print(f"  SL={SL} | TP={TP} | BE={BE}")
if remaining_p75 >= TP:
    print(f"  TP FULL ({TP} pts) cabe em P75?  SIM  — sinal normal")
elif remaining_p75 >= BE:
    print(f"  TP FULL ({TP} pts) cabe em P75?  NAO")
    print(f"  BE   ({BE} pts) cabe em P75?   SIM  — reduzir alvo para ~{int(remaining_p75*0.8)}-{int(remaining_p75*0.9)} pts")
else:
    print(f"  TP FULL ({TP} pts) cabe em P75?  NAO")
    print(f"  BE   ({BE} pts) cabe em P75?   NAO  — range esgotado, aguardar correcao")
    if remaining_p90 >= BE:
        print(f"  BE cabe em P90 ({remaining_p90:.0f} pts restantes)?  SIM — operar so se dia volatil (P90)")

print()
print("=== ULTIMOS 15 DIAS ===")
for r in rows[-15:]:
    rg  = r['high'] - r['low']
    pc  = rg / r['open'] * 100
    bdy = abs(r['close'] - r['open'])
    bd_pct = bdy / rg * 100 if rg else 0
    dr  = 'ALTA' if r['close'] >= r['open'] else 'BAIXA'
    print(f"  {r['date']}  {dr:<5}  range={rg:>5.0f} pts ({pc:.2f}%)  corpo={bd_pct:.0f}%")
