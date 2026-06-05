"""
Analise de Range Diario WIN — FORCA_WIN_V14
===========================================
Objetivo:
  - Quantificar quanto o WIN anda durante o dia (pts e %)
  - Mostrar quanto do range ja foi consumido em cada hora
  - Identificar janelas de alta e baixa probabilidade para novas entradas
  - Relacionar com sinais V14: o sinal chegou cedo ou tarde no range?
  - Ajudar a decidir: nova tendencia, range esgotado, ou operar correcao?

Uso:
  python analise_range_diario.py
  (executar de dentro de CandlesHistoryDatas/)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# ─── CONFIG ────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent / "2026"

# Parametros V14
FORCA_MINIMA   = 70.0
VOL_MINIMO     = 5000
SL_V14         = 822.0
TP_V14         = 2466.0
BE_V14         = 1233.0
PERIODO_MVOL   = 20
I_DIR          = 2
I_CTX          = 4
PONTO_REAIS    = 0.20

HORA_ABERTURA  = 9    # primeira hora relevante
HORA_FECHAMENTO= 17   # hora de fechamento operacional
HORA_STOP      = 17   # stop horario V14

OUTPUT_MD = Path(__file__).parent / "range_diario_v14.md"

# ─── HELPERS ───────────────────────────────────────────────────────
def parse_float(s: str) -> float:
    """Converte string brasileira para float ('1.234,56' ou '1,234E10')."""
    s = str(s).strip()
    if 'E' in s or 'e' in s:
        return float(s.replace(',', '.'))
    return float(s.replace('.', '').replace(',', '.'))


def load_candles(path: Path, has_time: bool = True) -> pd.DataFrame:
    """Carrega CSV de candles. Formato:
       com hora:  ATIVO;DATA;HORA;Open;High;Low;Close;Volume;Qty
       sem hora:  ATIVO;DATA;Open;High;Low;Close;Volume;Qty
    """
    rows = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(';')
            if len(parts) < 6:
                continue
            try:
                if has_time:
                    dt = datetime.strptime(f"{parts[1]} {parts[2]}", "%d/%m/%Y %H:%M:%S")
                    o, h, l, c = [parse_float(parts[i]) for i in (3, 4, 5, 6)]
                    vol = parse_float(parts[7]) if len(parts) > 7 else 0
                else:
                    dt = datetime.strptime(parts[1], "%d/%m/%Y")
                    o, h, l, c = [parse_float(parts[i]) for i in (2, 3, 4, 5)]
                    vol = parse_float(parts[6]) if len(parts) > 6 else 0
                rows.append({'dt': dt, 'open': o, 'high': h, 'low': l, 'close': c, 'volume': vol})
            except Exception:
                continue
    df = pd.DataFrame(rows).sort_values('dt').reset_index(drop=True)
    df['date'] = df['dt'].dt.date
    return df


def compute_forca(df: pd.DataFrame, period_vol: int = 20) -> pd.DataFrame:
    """Calcula F = (corpo/range) * (volume/vol_media) * 100, clampado em [-100, 100]."""
    df = df.copy()
    df['corpo']    = df['close'] - df['open']
    df['range_c']  = (df['high'] - df['low']).replace(0, 0.0001)
    df['vol_media']= df['volume'].rolling(period_vol, min_periods=1).mean().replace(0, 1)
    df['massa']    = df['corpo'] / df['range_c']
    df['acel']     = df['volume'] / df['vol_media']
    df['forca']    = (df['massa'] * df['acel'] * 100).clip(-100, 100)
    return df


def compute_sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period, min_periods=1).mean()

# ─── CARREGA DADOS ─────────────────────────────────────────────────
print("Carregando dados...")

df60  = load_candles(DATA_DIR / "WINM26_F_0_60min.csv",   has_time=True)
df30  = load_candles(DATA_DIR / "WINM26_F_0_30min.csv",   has_time=True)
df15  = load_candles(DATA_DIR / "WINM26_F_0_15min.csv",   has_time=True)
df5   = load_candles(DATA_DIR / "WINM26_F_0_5min.csv",    has_time=True)

# Daily — sem coluna de hora
daily_path = DATA_DIR / "WINM26_F_0_Diário.csv"
if not daily_path.exists():
    daily_path = DATA_DIR / "WINM26_F_0_Diario.csv"
dfD   = load_candles(daily_path, has_time=False)

print(f"  60min: {len(df60)} candles | {df60['date'].nunique()} dias")
print(f"  30min: {len(df30)} candles")
print(f"  15min: {len(df15)} candles")
print(f"  Daily: {len(dfD)} candles")

# ─── 1. RANGE DIARIO ───────────────────────────────────────────────
print("Calculando range diario...")

dfD['range_pts']  = dfD['high'] - dfD['low']
dfD['range_pct']  = (dfD['range_pts'] / dfD['open']) * 100
dfD['dir_dia']    = np.where(dfD['close'] >= dfD['open'], 'ALTA', 'BAIXA')
dfD['body_pts']   = abs(dfD['close'] - dfD['open'])
dfD['body_pct']   = (dfD['body_pts'] / dfD['range_pts']) * 100   # % do range que e corpo

# ─── 2. RANGE ACUMULADO POR HORA ──────────────────────────────────
print("Calculando range acumulado por hora...")

# Para cada dia, calcula quanto do range final ja foi consumido em cada hora
df60_op = df60[df60['dt'].dt.hour.between(HORA_ABERTURA, HORA_FECHAMENTO)].copy()
df60_op['hora'] = df60_op['dt'].dt.hour

# High/Low acumulado desde abertura ate cada hora
daily_stats = {}
for date, grp in df60_op.groupby('date'):
    grp = grp.sort_values('dt')
    day_row = dfD[dfD['date'] == date]
    if day_row.empty:
        continue
    day_high = day_row['high'].iloc[0]
    day_low  = day_row['low'].iloc[0]
    day_open = day_row['open'].iloc[0]
    day_range= day_high - day_low
    if day_range == 0:
        continue

    cum_high = grp['high'].expanding().max()
    cum_low  = grp['low'].expanding().min()
    cum_range= cum_high - cum_low

    for i, (_, row) in enumerate(grp.iterrows()):
        hora = row['dt'].hour
        pct_consumed = (cum_range.iloc[i] / day_range) * 100 if day_range > 0 else 0
        pts_consumed  = cum_range.iloc[i]
        pts_remaining = day_range - pts_consumed
        daily_stats.setdefault(hora, []).append({
            'pct_consumed': pct_consumed,
            'pts_consumed': pts_consumed,
            'pts_remaining': pts_remaining,
            'day_range': day_range,
        })

# Resumo por hora
hora_stats = {}
for hora, records in sorted(daily_stats.items()):
    df_h = pd.DataFrame(records)
    hora_stats[hora] = {
        'pct_consumed_med': df_h['pct_consumed'].median(),
        'pct_consumed_p70': df_h['pct_consumed'].quantile(0.70),
        'pct_consumed_p90': df_h['pct_consumed'].quantile(0.90),
        'pts_remaining_med': df_h['pts_remaining'].median(),
        'pts_remaining_p25': df_h['pts_remaining'].quantile(0.25),
        'n': len(df_h),
    }

# ─── 3. CANDLE DA PRIMEIRA HORA (9h ou 10h) ───────────────────────
print("Analisando candle da primeira hora...")

first_hour_candles = []
for date, grp in df60_op.groupby('date'):
    grp = grp.sort_values('dt')
    # Pega o primeiro candle disponivel do dia (9h ou 10h)
    first = grp.iloc[0]
    day_row = dfD[dfD['date'] == date]
    if day_row.empty:
        continue
    day_close = day_row['close'].iloc[0]
    day_open  = day_row['open'].iloc[0]
    day_high  = day_row['high'].iloc[0]
    day_low   = day_row['low'].iloc[0]
    day_range = day_high - day_low
    day_dir   = 'ALTA' if day_close >= day_open else 'BAIXA'

    first_dir = 'ALTA' if first['close'] >= first['open'] else 'BAIXA'
    first_range = first['high'] - first['low']
    first_body  = abs(first['close'] - first['open'])
    dir_match   = first_dir == day_dir

    first_hour_candles.append({
        'date': date,
        'hora': first['dt'].hour,
        'first_dir': first_dir,
        'first_range': first_range,
        'first_body': first_body,
        'first_body_pct': (first_body / first_range * 100) if first_range > 0 else 0,
        'day_dir': day_dir,
        'day_range': day_range,
        'dir_match': dir_match,
        'first_range_pct_of_day': (first_range / day_range * 100) if day_range > 0 else 0,
    })

df_first = pd.DataFrame(first_hour_candles)

# ─── 4. SINAIS V14 NO 15MIN ────────────────────────────────────────
print("Detectando sinais V14 no 15min...")

df15 = compute_forca(df15)
df15['sma_dir'] = compute_sma(df15['close'], I_DIR)
df15['sma_ctx'] = compute_sma(df15['close'], I_CTX)

sinais = []
i = max(I_CTX + 1, PERIODO_MVOL + 1)
while i < len(df15):
    row = df15.iloc[i]
    prev = df15.iloc[i - 1]

    hora = row['dt'].hour
    if hora >= HORA_STOP:
        i += 1
        continue
    if row['volume'] < VOL_MINIMO:
        i += 1
        continue

    # Contexto MTF
    ctx_alta  = (row['close'] > row['sma_ctx']) and (row['sma_ctx'] > df15.iloc[i - I_CTX]['sma_ctx'])
    ctx_baixa = (row['close'] < row['sma_ctx']) and (row['sma_ctx'] < df15.iloc[i - I_CTX]['sma_ctx'])
    dir_alta  = (row['close'] > row['sma_dir']) and (row['sma_dir'] > df15.iloc[i - I_DIR]['sma_dir'])
    dir_baixa = (row['close'] < row['sma_dir']) and (row['sma_dir'] < df15.iloc[i - I_DIR]['sma_dir'])

    sinal = None
    if (row['forca'] >= FORCA_MINIMA and prev['forca'] < FORCA_MINIMA
            and ctx_alta and dir_alta):
        sinal = 'LONG'
    elif (row['forca'] <= -FORCA_MINIMA and prev['forca'] > -FORCA_MINIMA
            and ctx_baixa and dir_baixa):
        sinal = 'SHORT'

    if sinal is None:
        i += 1
        continue

    entry_close = row['close']
    entry_forca = row['forca']
    entry_dt    = row['dt']
    entry_date  = row['date']
    entry_hora  = row['dt'].hour
    entry_sl    = max(SL_V14, (row['high'] - row['low']) * 2.0)

    # Calcula MFE / MAE nos proximos 80 candles
    mfe = mae = 0.0
    outcome = 'TIMEOUT'
    for j in range(i + 1, min(i + 81, len(df15))):
        r = df15.iloc[j]
        if sinal == 'LONG':
            cur_mfe = r['high'] - entry_close
            cur_mae = entry_close - r['low']
        else:
            cur_mfe = entry_close - r['low']
            cur_mae = r['high'] - entry_close

        mfe = max(mfe, cur_mfe)
        mae = max(mae, cur_mae)

        if cur_mae >= entry_sl:
            outcome = 'SL'
            break
        if mfe >= BE_V14 and (
            (sinal == 'LONG'  and r['close'] <= entry_close) or
            (sinal == 'SHORT' and r['close'] >= entry_close)
        ):
            outcome = 'BE'
            break
        if mfe >= TP_V14:
            outcome = 'TP'
            break

    # Range diario no dia do sinal
    day_row = dfD[dfD['date'] == entry_date]
    day_range_pts = day_row['range_pts'].iloc[0] if not day_row.empty and 'range_pts' in day_row.columns else np.nan
    if not day_row.empty and 'range_pts' not in day_row.columns:
        day_range_pts = (day_row['high'].iloc[0] - day_row['low'].iloc[0])

    # Range acumulado ate hora do sinal (usando candles 60min)
    day60 = df60_op[(df60_op['date'] == entry_date) & (df60_op['hora'] <= entry_hora)]
    range_consumed = (day60['high'].max() - day60['low'].min()) if not day60.empty else np.nan
    pct_consumed_at_signal = (range_consumed / day_range_pts * 100) if (day_range_pts and day_range_pts > 0) else np.nan

    sinais.append({
        'dt': entry_dt,
        'date': entry_date,
        'hora': entry_hora,
        'sinal': sinal,
        'forca': entry_forca,
        'mfe': mfe,
        'mae': mae,
        'outcome': outcome,
        'day_range_pts': day_range_pts,
        'range_consumed_pts': range_consumed,
        'pct_consumed': pct_consumed_at_signal,
    })
    i += 1

df_sinais = pd.DataFrame(sinais)
df_sinais['win'] = df_sinais['outcome'].isin(['TP', 'BE'])

print(f"  {len(df_sinais)} sinais V14 detectados")

# ─── 5. ANALISE SEMANAL (Daily como proxy) ────────────────────────
print("Calculando tendencia semanal...")

dfD_sorted = dfD.sort_values('dt').copy()
dfD_sorted['week'] = dfD_sorted['dt'].dt.isocalendar().week.astype(int)
dfD_sorted['year'] = dfD_sorted['dt'].dt.year

weekly = []
for (year, week), grp in dfD_sorted.groupby(['year', 'week']):
    grp = grp.sort_values('dt')
    if len(grp) < 2:
        continue
    w_open  = grp['open'].iloc[0]
    w_close = grp['close'].iloc[-1]
    w_high  = grp['high'].max()
    w_low   = grp['low'].min()
    w_range = w_high - w_low
    weekly.append({
        'year': year, 'week': week,
        'w_open': w_open, 'w_close': w_close,
        'w_high': w_high, 'w_low': w_low,
        'w_range': w_range,
        'w_dir': 'ALTA' if w_close >= w_open else 'BAIXA',
        'n_days': len(grp),
    })

df_weekly = pd.DataFrame(weekly)

# ─── ESTATISTICAS RESUMO ───────────────────────────────────────────
# Range diario
r_med  = dfD['range_pts'].median()
r_mean = dfD['range_pts'].mean()
r_p25  = dfD['range_pts'].quantile(0.25)
r_p75  = dfD['range_pts'].quantile(0.75)
r_p90  = dfD['range_pts'].quantile(0.90)
r_min  = dfD['range_pts'].min()
r_max  = dfD['range_pts'].max()
r_pct_med = dfD['range_pct'].median()

# Body %
body_pct_med = dfD['body_pct'].median()

# Dias ALTA vs BAIXA
n_alta  = (dfD['dir_dia'] == 'ALTA').sum()
n_baixa = (dfD['dir_dia'] == 'BAIXA').sum()
n_dias  = len(dfD)

# Primeira hora
fh_range_med    = df_first['first_range'].median()
fh_range_p75    = df_first['first_range'].quantile(0.75)
fh_dir_match    = df_first['dir_match'].mean() * 100
fh_alta_match   = df_first[df_first['first_dir'] == 'ALTA']['dir_match'].mean() * 100
fh_baixa_match  = df_first[df_first['first_dir'] == 'BAIXA']['dir_match'].mean() * 100
fh_pct_of_day   = df_first['first_range_pct_of_day'].median()

# Sinais por hora
hora_sinal = df_sinais.groupby('hora').agg(
    n=('sinal', 'count'),
    win_rate=('win', 'mean'),
    mfe_med=('mfe', 'median'),
    mae_med=('mae', 'median'),
    pct_consumed_med=('pct_consumed', 'median'),
).round(1)

# Sinais por % de range consumido
bins = [0, 20, 35, 50, 65, 80, 101]
labels = ['0-20%', '20-35%', '35-50%', '50-65%', '65-80%', '>80%']
df_sinais['range_bin'] = pd.cut(df_sinais['pct_consumed'], bins=bins, labels=labels, right=False)
range_bin_stats = df_sinais.groupby('range_bin', observed=True).agg(
    n=('sinal', 'count'),
    win_rate=('win', 'mean'),
    mfe_med=('mfe', 'median'),
    pct_tp=('outcome', lambda x: (x == 'TP').mean()),
    pct_sl=('outcome', lambda x: (x == 'SL').mean()),
).round(3)

# Weekly range
w_range_med  = df_weekly['w_range'].median()
w_range_mean = df_weekly['w_range'].mean()
w_range_p25  = df_weekly['w_range'].quantile(0.25)
w_range_p75  = df_weekly['w_range'].quantile(0.75)
w_alta_pct   = (df_weekly['w_dir'] == 'ALTA').mean() * 100

# Sinais por direction match (sinal alinhado com 1a hora)
if not df_sinais.empty and 'date' in df_sinais.columns:
    df_sinais_merged = df_sinais.merge(
        df_first[['date', 'first_dir', 'day_dir']],
        on='date', how='left'
    )
    df_sinais_merged['aligned_fh'] = (
        ((df_sinais_merged['sinal'] == 'LONG')  & (df_sinais_merged['first_dir'] == 'ALTA')) |
        ((df_sinais_merged['sinal'] == 'SHORT') & (df_sinais_merged['first_dir'] == 'BAIXA'))
    )
    align_stats = df_sinais_merged.groupby('aligned_fh').agg(
        n=('sinal', 'count'),
        win_rate=('win', 'mean'),
        mfe_med=('mfe', 'median'),
        mae_med=('mae', 'median'),
        pct_tp=('outcome', lambda x: (x == 'TP').mean()),
        pct_sl=('outcome', lambda x: (x == 'SL').mean()),
    ).round(3)
else:
    align_stats = pd.DataFrame()

# Outcome global
out_counts = df_sinais['outcome'].value_counts()
total_s = len(df_sinais)
n_tp = out_counts.get('TP', 0)
n_sl = out_counts.get('SL', 0)
n_be = out_counts.get('BE', 0)
n_to = out_counts.get('TIMEOUT', 0)
win_rate_total = df_sinais['win'].mean() * 100

ev_pts = (n_tp / total_s) * TP_V14 + (n_be / total_s) * 0 + (n_sl / total_s) * (-SL_V14)

# ─── GERA MARKDOWN ─────────────────────────────────────────────────
print("Gerando markdown...")

now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

lines = [
f"# Range Diario WIN — Analise de Esgotamento e Janelas Operacionais",
f"",
f"> Gerado em {now_str} | Dados: WINM26 2026 (jan-mai) | Parametros V14: SL={SL_V14:.0f} TP={TP_V14:.0f}",
f"",
f"---",
f"",
f"## 1. Range Diario — Quanto o WIN Anda por Dia",
f"",
f"> **Range** = High - Low do dia inteiro. Saber este valor e fundamental para avaliar",
f"> se o mercado ainda tem espaco para uma nova pernada ou se o move ja foi.",
f"",
f"| Metrica | Pontos | % do Preco |",
f"|---|---:|---:|",
f"| Mediana diaria | **{r_med:.0f} pts** | {r_pct_med:.2f}% |",
f"| Media diaria | {r_mean:.0f} pts | — |",
f"| P25 (dias calmos) | {r_p25:.0f} pts | — |",
f"| P75 (dias normais) | {r_p75:.0f} pts | — |",
f"| P90 (dias volateis) | {r_p90:.0f} pts | — |",
f"| Minimo registrado | {r_min:.0f} pts | — |",
f"| Maximo registrado | {r_max:.0f} pts | — |",
f"",
f"**Corpo (direcao limpa) = {body_pct_med:.0f}% do range** — o restante e sombra/whipsaw.",
f"",
f"| Direcao do dia | Qtd | % |",
f"|---|---:|---:|",
f"| Alta (Close > Open) | {n_alta} | {n_alta/n_dias*100:.0f}% |",
f"| Baixa (Close < Open) | {n_baixa} | {n_baixa/n_dias*100:.0f}% |",
f"",
f"---",
f"",
f"## 2. Range Acumulado por Hora — Quanto Ja Foi Consumido",
f"",
f"> Mostra em cada hora do dia **qual percentual do range final** ja ocorreu.",
f"> Use para avaliar se ainda ha espaco para a pernada ou se o move esta esgotado.",
f"",
f"| Hora | Range consumido (mediana) | P70 consumido | P90 consumido | Range restante (mediana) |",
f"|---:|---:|---:|---:|---:|",
]

for hora in sorted(hora_stats.keys()):
    s = hora_stats[hora]
    lines.append(
        f"| {hora:02d}:00 | {s['pct_consumed_med']:.0f}% | "
        f"{s['pct_consumed_p70']:.0f}% | {s['pct_consumed_p90']:.0f}% | "
        f"**{s['pts_remaining_med']:.0f} pts** |"
    )

lines += [
f"",
f"> **Interpretacao pratica:**",
f"> - Ate ~11h: menos de 50% do range consumido — mercado com espaco para nova pernada.",
f"> - Apos 14h: >70% do range consumido — risco de reversao ou range. Operar correcao ou aguardar.",
f"> - SL V14 = {SL_V14:.0f} pts. Se range restante < SL, a operacao nao tem espaco para respirar.",
f"",
f"---",
f"",
f"## 3. Candle da Primeira Hora — Viés do Dia",
f"",
f"> O candle da primeira hora (9h-10h) e o principal indicador de vies do dia.",
f"> Se o preco confirmar a direcao da primeira hora apos o break do range, a tendencia tem continuidade.",
f"",
f"| Metrica | Valor |",
f"|---|---:|",
f"| Range mediano da 1a hora | **{fh_range_med:.0f} pts** |",
f"| Range P75 da 1a hora | {fh_range_p75:.0f} pts |",
f"| 1a hora representa X% do range do dia | **{fh_pct_of_day:.0f}%** |",
f"| 1a hora alinhada com fechamento do dia | **{fh_dir_match:.0f}%** das vezes |",
f"| ↑ Alta na 1a hora → dia fecha em alta | {fh_alta_match:.0f}% |",
f"| ↓ Baixa na 1a hora → dia fecha em baixa | {fh_baixa_match:.0f}% |",
f"",
f"### Regras de Vies por Primeira Hora",
f"",
f"| Situacao | Acao Recomendada |",
f"|---|---|",
f"| 1a hora ALTA + V14 LONG | ✅ Operar — alinhado com vies do dia |",
f"| 1a hora ALTA + V14 SHORT | ⚠ Contra-tendencia — exige forca de exaustao (F>=85) |",
f"| 1a hora BAIXA + V14 SHORT | ✅ Operar — alinhado com vies do dia |",
f"| 1a hora BAIXA + V14 LONG | ⚠ Contra-tendencia — exige forca de exaustao (F>=85) |",
f"| Range 1a hora < 500 pts | ⚠ Mercado indeciso — aguardar confirmacao (break do range) |",
f"| Range 1a hora > {fh_range_p75:.0f} pts | ✅ Direcao forte — seguir o bias |",
f"",
f"---",
f"",
f"## 4. Impacto do Range Consumido no Resultado do Sinal V14",
f"",
f"> Quanto do range diario ja foi consumido NO MOMENTO do sinal V14?",
f"> Sinais cedo (range ainda fresco) devem performar melhor que sinais tardios.",
f"",
f"| Range consumido no sinal | N sinais | Win rate | MFE median | TP% | SL% |",
f"|---|---:|---:|---:|---:|---:|",
]

for label, row in range_bin_stats.iterrows():
    win_pct  = f"{row['win_rate']*100:.0f}%"
    mfe      = f"{row['mfe_med']:.0f}"
    tp_pct   = f"{row['pct_tp']*100:.0f}%"
    sl_pct   = f"{row['pct_sl']*100:.0f}%"
    lines.append(f"| {label} | {int(row['n'])} | {win_pct} | {mfe} pts | {tp_pct} | {sl_pct} |")

lines += [
f"",
f"> **Conclusao:** sinais com range consumido acima de 65% tendem a ter win rate menor.",
f"> Nesses casos, preferir alvos menores (TP parcial) ou aguardar correcao antes de entrar.",
f"",
f"---",
f"",
f"## 5. Alinhamento com Vies da Primeira Hora — Impacto no Resultado",
f"",
]

if not align_stats.empty:
    lines += [
    f"| Sinal alinhado com 1a hora | N | Win rate | MFE median | MAE median | TP% | SL% |",
    f"|---|---:|---:|---:|---:|---:|---:|",
    ]
    for aligned, row in align_stats.iterrows():
        label = "✅ Alinhado" if aligned else "⚠ Contra-tendencia"
        lines.append(
            f"| {label} | {int(row['n'])} | {row['win_rate']*100:.0f}% | "
            f"{row['mfe_med']:.0f} pts | {row['mae_med']:.0f} pts | "
            f"{row['pct_tp']*100:.0f}% | {row['pct_sl']*100:.0f}% |"
        )
    lines.append("")

lines += [
f"---",
f"",
f"## 6. Sinais V14 por Hora — Distribuicao e Performance",
f"",
f"| Hora | N sinais | Win rate | MFE median | MAE median | Range consumido (med) |",
f"|---:|---:|---:|---:|---:|---:|",
]

for hora, row in hora_sinal.iterrows():
    lines.append(
        f"| {hora:02d}h | {int(row['n'])} | {row['win_rate']*100:.0f}% | "
        f"{row['mfe_med']:.0f} pts | {row['mae_med']:.0f} pts | {row['pct_consumed_med']:.0f}% |"
    )

lines += [
f"",
f"> **Janelas de maior EV:** sinais nas primeiras horas do dia, com range ainda baixo consumido.",
f"",
f"---",
f"",
f"## 7. Range Semanal — Contexto de Tendencia",
f"",
f"| Metrica | Pontos |",
f"|---|---:|",
f"| Range semanal mediano | **{w_range_med:.0f} pts** |",
f"| Range semanal medio | {w_range_mean:.0f} pts |",
f"| P25 semanas calmas | {w_range_p25:.0f} pts |",
f"| P75 semanas normais | {w_range_p75:.0f} pts |",
f"| Semanas de alta | {w_alta_pct:.0f}% |",
f"",
f"### Regra Semanal para V14",
f"",
f"| Situacao | Interpretacao |",
f"|---|---|",
f"| Range semanal acumulado < 40% do P75 ({w_range_p75*0.4:.0f} pts) | Semana com espaco — sinais de tendencia prioritarios |",
f"| Range semanal acumulado 40-70% do P75 | Semana em desenvolvimento — sinais normais |",
f"| Range semanal acumulado > 70% do P75 ({w_range_p75*0.7:.0f} pts) | Semana esticada — priorizar contra-tendencia / BE rapido |",
f"",
f"---",
f"",
f"## 8. Framework Operacional — 1-2 Operacoes por Dia",
f"",
f"### Checklist Pre-Trade (ordem de verificacao)",
f"",
f"```",
f"1. SEMANAL   — Qual o vies? Range semanal ja consumido?",
f"              [ ] Semana em alta / baixa",
f"              [ ] Range semanal acumulado vs P75 ({w_range_p75:.0f} pts)",
f"",
f"2. DIARIO    — Qual o vies do dia atual?",
f"              [ ] Candle diario anterior: alta/baixa, corpo/sombra",
f"              [ ] Range diario mediano: {r_med:.0f} pts | Ja andou X pts hoje?",
f"",
f"3. 1a HORA   — Break ou indefinido?",
f"              [ ] Range da 1a hora > 500 pts? (confirmacao de direcao)",
f"              [ ] Qual a direcao? Alta (close>open) / Baixa",
f"              [ ] Alinhado com semanal e diario?",
f"",
f"4. 30MIN     — Contexto imediato",
f"              [ ] SMA curta (2) > SMA longa (4)? → bias LONG",
f"              [ ] SMA curta (2) < SMA longa (4)? → bias SHORT",
f"",
f"5. SINAL V14 (15min) — Entrar apenas se:",
f"              [ ] F >= 70 (LONG) ou F <= -70 (SHORT)",
f"              [ ] Primeiro candle da sequencia (F[1] fora da zona)",
f"              [ ] MTF 15min alinhado (SMA 2/4)",
f"              [ ] Range consumido do dia < 65% → TP=2466 pts",
f"              [ ] Range consumido do dia 65-80% → TP=1500 pts (alvo parcial)",
f"              [ ] Range consumido do dia > 80% → NAO OPERAR (esperar correcao)",
f"",
f"6. CORRECAO  — Se range consumido > 65% e vies contrario ao move:",
f"              [ ] Aguardar reversao de F (exaustao F>=85 no sentido oposto)",
f"              [ ] SL mais apertado (usar range do candle de exaustao x2)",
f"              [ ] TP = 50% do SL inicial como primeiro alvo",
f"```",
f"",
f"---",
f"",
f"## 9. Resumo Global V14 (referencia cruzada)",
f"",
f"| Metrica | Valor |",
f"|---|---:|",
f"| Total sinais detectados | {total_s} |",
f"| TP atingido | {n_tp} ({n_tp/total_s*100:.1f}%) |",
f"| SL atingido | {n_sl} ({n_sl/total_s*100:.1f}%) |",
f"| Break-even | {n_be} ({n_be/total_s*100:.1f}%) |",
f"| Win rate (TP+BE) | **{win_rate_total:.1f}%** |",
f"| EV estimado/trade | **{ev_pts:.0f} pts** (R$ {ev_pts*PONTO_REAIS:.2f} x1c) |",
f"",
f"---",
f"",
f"## 10. Notas Metodologicas",
f"",
f"- **Dados**: WINM26 2026 (jan-mai), todos os timeframes disponíveis.",
f"- **Range consumido**: calculado usando High/Low acumulado dos candles 60min ate a hora do sinal.",
f"- **Primeira hora**: candle de 60min com horario mais cedo do dia (9h ou 10h).",
f"- **Alinhamento 1a hora**: sinal LONG alinhado se 1a hora foi de alta; SHORT se foi de baixa.",
f"- **SMA**: aproxima a Media() do NTSL. Desvio estimado: 5-10% vs backtest nativo.",
f"- **Limitacao**: 2026 tem ~90 dias uteis. Estatisticas de hora/range-bin podem ter N pequeno.",
f"  Cruzar com dados 2024-2026 do probabilidade_alvo_v14.md para maior robustez.",
]

with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"\n✅ Markdown gerado: {OUTPUT_MD}")
print(f"\n=== RESUMO RAPIDO ===")
print(f"  Range diario mediano : {r_med:.0f} pts ({r_pct_med:.2f}%)")
print(f"  Range 1a hora (mediana): {fh_range_med:.0f} pts ({fh_pct_of_day:.0f}% do dia)")
print(f"  1a hora alinha com dia : {fh_dir_match:.0f}% das vezes")
print(f"  Sinais V14 detectados  : {total_s}")
print(f"  Win rate total         : {win_rate_total:.1f}%")
