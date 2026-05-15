import pandas as pd, numpy as np
from pathlib import Path

def load_csv(fname):
    df = pd.read_csv(fname, sep=';', decimal=',', encoding='latin1')
    df['datetime'] = pd.to_datetime(df['Data'] + ' ' + df['Hora'], dayfirst=True)
    return df

base='WINJ26_F_0'
csv60=f'{base}_60min.csv'
csv15=f'{base}_15min.csv'
csv5=f'{base}_5min.csv'

for f in [csv60,csv15,csv5]:
    if not Path(f).exists():
        raise FileNotFoundError(f'Missing {f}')

f60 = load_csv(csv60).sort_values('datetime')
f15 = load_csv(csv15).sort_values('datetime')
f5 = load_csv(csv5).sort_values('datetime')

x_points=100
pt_value=0.01
x_val = x_points*pt_value
sl_min=50*pt_value
sg_min=80*pt_value

areas=[]
for idx,row in f60.iterrows():
    areas.append({'dt':row.datetime,'low':row['Mínimo']-x_val,'high':row['Máximo']+x_val,'orig_low':row['Mínimo'],'orig_high':row['Máximo']})
areas_df = pd.DataFrame(areas)

f5['fForca'] = (f5['Fechamento'] - f5['Abertura'])
frange = (f5['Máximo'] - f5['Mínimo']).replace(0,0.0001)
volmean = f5['Volume'].rolling(20,min_periods=1).mean().clip(lower=1)

f5['fForca'] = ((f5['Fechamento'] - f5['Abertura']) / frange) * (f5['Volume'] / volmean) * 100
f5['fForca'] = f5['fForca'].clip(-100,100)

candidates=[]
for i in range(2, len(f15)):
    c3 = f15.iloc[i-2:i+1]
    window_low = c3['Mínimo'].max()
    window_high = c3['Máximo'].min()
    overlap = max(0, window_high - window_low)
    rng = c3['Máximo'].max() - c3['Mínimo'].min()
    overlap_pct = overlap / (rng if rng > 0 else 1)
    if overlap_pct < 0.2:
        continue
    t = c3.iloc[-1].datetime
    sub = areas_df[(areas_df.dt <= t) & (areas_df.dt > t - pd.Timedelta('1h'))]
    if sub.empty:
        continue
    area = sub.iloc[-1]
    cclose = c3.iloc[-1]['Fechamento']
    if not (area.low <= cclose <= area.high):
        continue
    candidates.append({'candidate_dt': t, 'price': cclose, 'overlap_pct': overlap_pct, 'area_low': area.low, 'area_high': area.high})

trades=[]
for c in candidates:
    ctime = c['candidate_dt']
    future = f5[(f5.datetime > ctime) & (f5.datetime <= ctime + pd.Timedelta('10m'))].head(2)
    if future.empty:
        continue
    prev = f5[f5.datetime <= ctime].tail(1)
    if prev.empty:
        continue
    entry = prev.iloc[-1]['Fechamento']
    fval = prev.iloc[-1]['fForca']
    if abs(fval) < 55:
        continue
    direction = 'buy' if fval > 0 else 'sell'
    target = entry + sg_min if direction == 'buy' else entry - sg_min
    stop = entry - sl_min if direction == 'buy' else entry + sl_min
    outcome = 'none'
    for _, row in future.iterrows():
        h = row['Máximo']; l = row['Mínimo']
        if direction == 'buy':
            if l <= stop:
                outcome='loss'; break
            if h >= target:
                outcome='win'; break
        else:
            if h >= stop:
                outcome='loss'; break
            if l <= target:
                outcome='win'; break
    if outcome == 'none':
        last = future.iloc[-1]['Fechamento']
        if direction == 'buy':
            outcome='win' if last>=target else 'loss' if last<=stop else 'neutral'
        else:
            outcome='win' if last<=target else 'loss' if last>=stop else 'neutral'
    trades.append({'dt': ctime, 'entry': entry, 'dir': direction, 'fForca': fval, 'target': target, 'stop': stop, 'outcome': outcome, 'overlap_pct': c['overlap_pct']})

wins = sum(1 for t in trades if t['outcome']=='win')
losses = sum(1 for t in trades if t['outcome']=='loss')
neutrals = sum(1 for t in trades if t['outcome']=='neutral')
print('candidates', len(candidates), 'trades', len(trades))
print('wins', wins, 'losses', losses, 'neutrals', neutrals, 'winrate', round(wins/(wins+losses),4) if wins+losses>0 else None)
print('example trades', trades[:5])
with open('stats_winrate.txt','w',encoding='utf-8') as f:
    f.write(f'candidates {len(candidates)} trades {len(trades)}\n')
    f.write(f'wins {wins} losses {losses} neutrals {neutrals} winrate {round(wins/(wins+losses),4) if wins+losses>0 else None}\n')
