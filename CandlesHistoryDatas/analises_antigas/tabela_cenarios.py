import pandas as pd
import numpy as np
from pathlib import Path


def load(prefix, tf):
    frames = []
    for pasta in sorted(Path('.').glob('*/')):
        for f in pasta.glob(f'*{prefix}*_{tf}.csv'):
            try:
                df = pd.read_csv(f, sep=';', decimal=',',
                                 encoding='latin1', thousands='.')
                if len(df.columns) < 8:
                    continue
                cm = {df.columns[1]: 'Data', df.columns[2]: 'Hora', df.columns[3]: 'Open', df.columns[4]: 'High', df.columns[5]: 'Low', df.columns[6]: 'Close', df.columns[7]: 'Volume'}
                df = df.rename(columns=cm)
                df['dt'] = pd.to_datetime(
                    df['Data']+' '+df['Hora'], dayfirst=True, errors='coerce')
                df = df.dropna(subset=['dt']).sort_values(
                    'dt').reset_index(drop=True)
                for c in ['Open', 'Close', 'High', 'Low']:
                    df[c] = pd.to_numeric(df[c], errors='coerce')
                df['Volume'] = pd.to_numeric(
                    df['Volume'], errors='coerce').fillna(0)
                frames.append(
                    df[['dt', 'Open', 'High', 'Low', 'Close', 'Volume']].dropna())
            except:
                pass
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames).sort_values('dt').drop_duplicates('dt').reset_index(drop=True)


def sim(idxs, close_np, high_np, low_np, f_np, sl, tp):
    wins = losses = 0
    n_df = len(close_np)
    for i in idxs:
        il = f_np[i] > 0
        e = close_np[i]
        tgt = e+tp if il else e-tp
        stp = e-sl if il else e+sl
        out = None
        end = min(i+16, n_df)
        for j in range(i+1, end):
            h = high_np[j]
            l = low_np[j]
            if il:
                if l <= stp:
                    out = 'L'
                    break
                if h >= tgt:
                    out = 'W'
                    break
            else:
                if h >= stp:
                    out = 'L'
                    break
                if l <= tgt:
                    out = 'W'
                    break
        if out is None:
            cl = close_np[min(i+15, n_df-1)]
            out = 'W' if ((il and cl > e) or (not il and cl < e)) else 'L'
        if out == 'W':
            wins += 1
        else:
            losses += 1
    n = wins+losses
    wr = round(wins/n*100, 1) if n > 0 else 0
    return n, wins, losses, wr, round(wins*tp - losses*sl, 0)


def tabela(prefix, tf, sl, tp, nome):
    df = load(prefix, tf)
    if len(df) < 100:
        print(f'[{nome}] dados insuficientes')
        return
    corpo = df['Close'].values - df['Open'].values
    rng = np.where((df['High'].values-df['Low'].values) > 0,
                   df['High'].values-df['Low'].values, 0.0001)
    vm = pd.Series(df['Volume'].values).rolling(
        20, min_periods=1).mean().clip(lower=1).values
    f_np = np.clip((corpo/rng)*(df['Volume'].values/vm)*100, -100, 100)
    fa = np.abs(f_np)
    close_np = df['Close'].values
    high_np = df['High'].values
    low_np = df['Low'].values
    n_df = len(df)

    configs = {
        'a) VERDE 1o sinal (70-85 direto)': [i for i in range(1, n_df-15) if 70 <= fa[i] < 85 and fa[i-1] < 70],
        'b) FUCSIA 1o sinal (>=85 direto)': [i for i in range(1, n_df-15) if fa[i] >= 85 and fa[i-1] < 70],
        'c) VERDE->FUCSIA (seq obrigat.)': [i for i in range(1, n_df-15) if fa[i] >= 85 and 70 <= fa[i-1] < 85 and f_np[i]*f_np[i-1] > 0],
        'd) FUCSIA->VERDE (continuacao)': [i for i in range(1, n_df-15) if 70 <= fa[i] < 85 and fa[i-1] >= 85 and f_np[i]*f_np[i-1] > 0],
        'e) FUCSIA->FUCSIA (2x exaust)': [i for i in range(1, n_df-15) if fa[i] >= 85 and fa[i-1] >= 85 and f_np[i]*f_np[i-1] > 0],
        'f) TODOS >= 70 (sem filtro seq)': [i for i in range(n_df-15) if fa[i] >= 70],
    }
    print(f'\n=== {nome}  SL={sl}  TP={tp}  RR={round(tp/sl, 1)} ===')
    print(f'  {"Cenario":38}| {"n":>5} | {"Win%":>5} | {"PnL":>10} | Acao')
    for desc, idxs in configs.items():
        if not idxs:
            print(f'  {desc:38}| sem dados')
            continue
        n, w, l, wr, pnl = sim(idxs, close_np, high_np, low_np, f_np, sl, tp)
        if wr >= 42 and pnl > 0:
            rec = 'ENTRAR SEMPRE'
        elif pnl > 0 and wr >= 39:
            rec = 'ENTRAR'
        elif pnl > 0:
            rec = 'AGUARDAR'
        else:
            rec = 'EVITAR'
        print(f'  {desc:38}| {n:5d} | {wr:5.1f}% | {pnl:+10.0f} | {rec}')


tabela('WD', '15min', 20.0, 60.0, 'WDO 15min')
tabela('WI', '15min', 822.0, 2466.0, 'WIN 15min')
tabela('WD', '5min', 12.0, 36.0, 'WDO 5min')
tabela('WI', '5min', 342.0, 1026.0, 'WIN 5min')
print('\nConcluido.')
