#!/usr/bin/env python3
"""Analisa todos os CSVs de resultado e gera MDs por grupo."""
import os
import re
from collections import defaultdict
from datetime import datetime

RESULT_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_br_float(s):
    if not s:
        return None
    s = s.strip().replace('\xa0', '').replace(' ', '')
    if s in ('', '-', 'N/A', '0'):
        return 0.0
    try:
        return float(s.replace('.', '').replace(',', '.'))
    except:
        return None


def analyze_csv(filepath):
    try:
        with open(filepath, encoding='latin-1', errors='replace') as f:
            lines = f.readlines()
    except:
        return None

    header_idx = None
    for i, line in enumerate(lines):
        if 'Abertura' in line and 'Fechamento' in line:
            header_idx = i
            break
    if header_idx is None:
        return None

    raw_headers = lines[header_idx].split(';')
    headers = [h.strip() for h in raw_headers]

    trades = []
    for line in lines[header_idx+1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split(';')
        if len(parts) < 5:
            continue
        row = dict(zip(headers, parts))

        res = parse_br_float(row.get('Res. Intervalo Bruto', ''))
        if res is None:
            continue

        res_pct = parse_br_float(row.get('Res. Intervalo (%)', '')) or 0
        lado = row.get('Lado', '').strip()
        abertura = row.get('Abertura', '').strip()
        fechamento = row.get('Fechamento', '').strip()
        # Try to parse Tempo Operacao key (encoding may vary)
        tempo_key = next((k for k in headers if 'Tempo' in k), '')
        tempo = row.get(tempo_key, '').strip()

        preco_c_key = next(
            (k for k in headers if 'Compra' in k and 'Qtd' not in k and 'Res' not in k), '')
        preco_v_key = next(
            (k for k in headers if 'Venda' in k and 'Qtd' not in k and 'Res' not in k), '')
        preco_c = parse_br_float(row.get(preco_c_key, ''))
        preco_v = parse_br_float(row.get(preco_v_key, ''))

        trades.append({'res': res, 'res_pct': res_pct, 'lado': lado,
                       'abertura': abertura, 'fechamento': fechamento,
                       'tempo': tempo, 'preco_c': preco_c, 'preco_v': preco_v})

    if not trades:
        return None

    resultados = [t['res'] for t in trades]
    ganhos = [r for r in resultados if r > 0]
    perdas = [r for r in resultados if r < 0]
    empates = [r for r in resultados if r == 0]

    total = len(resultados)
    win_rate = len(ganhos)/total*100 if total else 0
    pnl_total = sum(resultados)
    avg_g = sum(ganhos)/len(ganhos) if ganhos else 0
    avg_p = sum(perdas)/len(perdas) if perdas else 0
    rr = abs(avg_g/avg_p) if avg_p else 0
    max_g = max(ganhos) if ganhos else 0
    max_p = min(perdas) if perdas else 0

    lados = defaultdict(int)
    for t in trades:
        lados[t['lado']] += 1

    # streak analysis
    max_win_seq = max_lose_seq = cur_w = cur_l = 0
    for r in resultados:
        if r > 0:
            cur_w += 1
            cur_l = 0
            max_win_seq = max(max_win_seq, cur_w)
        elif r < 0:
            cur_l += 1
            cur_w = 0
            max_lose_seq = max(max_lose_seq, cur_l)
        else:
            cur_w = cur_l = 0

    # date range
    dates = [t['abertura'] for t in trades if t['abertura']]

    return {
        'total': total,
        'n_ganhos': len(ganhos),
        'n_perdas': len(perdas),
        'n_empates': len(empates),
        'win_rate': win_rate,
        'pnl_total': pnl_total,
        'avg_ganho': avg_g,
        'avg_perda': avg_p,
        'rr': rr,
        'max_ganho': max_g,
        'max_perda': max_p,
        'lados': dict(lados),
        'max_win_seq': max_win_seq,
        'max_lose_seq': max_lose_seq,
        'data_inicio': dates[0][:10] if dates else '?',
        'data_fim': dates[-1][:10] if dates else '?',
        'trades': trades,
    }


def group_files(files):
    groups = defaultdict(list)
    for f in sorted(files):
        if f.startswith('FORCA_SEMAFORO_CORES_SOM_WIN'):
            groups['SEMAFORO_WIN'].append(f)
        elif f.startswith('FORCA_SEMAFORO_CORES_SOM_WDO'):
            groups['SEMAFORO_WDO'].append(f)
        elif f.startswith('FORCA_SEMAFORO_CORES_SOM_30m'):
            groups['SEMAFORO_MISTO_30m'].append(f)
        elif f.startswith('FORCA_WDO_V11'):
            groups['WDO_V11'].append(f)
        elif f.startswith('FORCA_WDO_V12'):
            groups['WDO_V12'].append(f)
        elif f.startswith('FORCA_WDO_V13'):
            groups['WDO_V13'].append(f)
        elif f.startswith('FORCA_WIN_V11'):
            groups['WIN_V11'].append(f)
        elif f.startswith('FORCA_WIN_V12'):
            groups['WIN_V12'].append(f)
        elif f.startswith('FORCA_WIN_V13'):
            groups['WIN_V13'].append(f)
    return groups


def tf_from_name(fname):
    m = re.search(r'_(\d+m|diario|60m)\.csv', fname, re.I)
    return m.group(1) if m else fname


def rating(pnl, win_rate, rr):
    score = 0
    if pnl > 0:
        score += 1
    if pnl > 500:
        score += 1
    if win_rate >= 40:
        score += 1
    if win_rate >= 45:
        score += 1
    if rr >= 1.5:
        score += 1
    if rr >= 2.0:
        score += 1
    return '⭐' * score if score > 0 else '❌'


def generate_md(group_name, files_data):
    ativo = 'WIN' if 'WIN' in group_name else 'WDO' if 'WDO' in group_name else 'MISTO'
    versao = ''
    tipo = ''
    if 'SEMAFORO' in group_name:
        tipo = 'Semáforo Cores+Som'
    elif 'V11' in group_name:
        versao = 'V11'
    elif 'V12' in group_name:
        versao = 'V12'
    elif 'V13' in group_name:
        versao = 'V13'
    if versao:
        tipo = f'Força {versao}'

    title = f"ANALISE-{group_name}"

    lines = []
    lines.append(f"# {title}")
    lines.append(f"")
    lines.append(
        f"> **Ativo:** {ativo} | **Robô:** {tipo} | **Análise gerada em:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"")
    lines.append(f"## Resumo por Timeframe")
    lines.append("")
    lines.append(
        "| TF | Ops | Win% | PnL (pts) | Avg Ganho | Avg Perda | RR | Max+ | Max- | Seq+↑ | Seq-↓ | Rating |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|")

    summaries = []
    for fname, r in files_data:
        if r is None:
            continue
        tf = tf_from_name(fname)
        rt = rating(r['pnl_total'], r['win_rate'], r['rr'])
        lines.append(
            f"| {tf} | {r['total']} | {r['win_rate']:.1f}% | {r['pnl_total']:+.0f} | "
            f"{r['avg_ganho']:+.0f} | {r['avg_perda']:+.0f} | {r['rr']:.2f} | "
            f"{r['max_ganho']:+.0f} | {r['max_perda']:+.0f} | "
            f"{r['max_win_seq']} | {r['max_lose_seq']} | {rt} |"
        )
        summaries.append((tf, r))

    lines.append("")
    lines.append("## Análise por Timeframe")
    lines.append("")

    best_tf = max(summaries, key=lambda x: x[1]['pnl_total'], default=None)
    worst_tf = min(summaries, key=lambda x: x[1]['pnl_total'], default=None)

    for tf, r in summaries:
        tag = ""
        if best_tf and tf == best_tf[0]:
            tag = " 🏆 **MELHOR**"
        if worst_tf and tf == worst_tf[0]:
            tag = " ⚠️ **PIOR**"

        lines.append(f"### {tf}{tag}")
        lines.append("")

        # Pnl consistency
        pnl_pos = "LUCRATIVO" if r['pnl_total'] > 0 else "NEGATIVO"
        lines.append(f"- **Período:** {r['data_inicio']} → {r['data_fim']}")
        lines.append(
            f"- **Resultado geral:** {pnl_pos} — PnL `{r['pnl_total']:+.0f} pts`")
        lines.append(
            f"- **Operações:** {r['total']} total | {r['n_ganhos']} ganhos | {r['n_perdas']} perdas | {r['n_empates']} empates")
        lines.append(f"- **Win Rate:** `{r['win_rate']:.1f}%`")
        lines.append(
            f"- **Médias:** Ganho médio `{r['avg_ganho']:+.0f} pts` | Perda média `{r['avg_perda']:+.0f} pts`")
        lines.append(f"- **RR implícito:** `{r['rr']:.2f}`")
        lines.append(
            f"- **Range de pontos:** Maior ganho `{r['max_ganho']:+.0f}` | Maior perda `{r['max_perda']:+.0f}`")
        lines.append(
            f"- **Sequências:** Máx ganhos seguidos `{r['max_win_seq']}` | Máx perdas seguidas `{r['max_lose_seq']}`")
        if r['lados']:
            c_count = r['lados'].get('C', 0)
            v_count = r['lados'].get('V', 0)
            lines.append(
                f"- **Direção:** {c_count} Compras | {v_count} Vendas")
        lines.append("")

    lines.append("## Insights para Próximos Ajustes")
    lines.append("")

    # Auto-generate insights
    positivos = [(tf, r) for tf, r in summaries if r['pnl_total'] > 0]
    negativos = [(tf, r) for tf, r in summaries if r['pnl_total'] <= 0]

    if positivos:
        tfs_pos = ', '.join(f'`{tf}`' for tf, _ in positivos)
        lines.append(
            f"- ✅ **TFs lucrativos:** {tfs_pos} — manter ou refinar parâmetros")
    if negativos:
        tfs_neg = ', '.join(f'`{tf}`' for tf, _ in negativos)
        lines.append(
            f"- ❌ **TFs negativos:** {tfs_neg} — revisar SL/TP ou descartar")

    # RR analysis
    low_rr = [(tf, r) for tf, r in summaries if 0 < r['rr'] < 1.5]
    if low_rr:
        lines.append(
            f"- ⚠️ **RR baixo (<1.5):** {', '.join(f'`{tf}`' for tf, _ in low_rr)} — aumentar TP ou reduzir SL")

    high_lose_seq = [(tf, r) for tf, r in summaries if r['max_lose_seq'] >= 5]
    if high_lose_seq:
        lines.append(f"- 🔴 **Alta sequência negativa (≥5):** {', '.join(f'`{tf}`' for tf,
                     _ in high_lose_seq)} — considerar filtro de mercado ou pausa")

    lines.append("")
    lines.append("## Próximos Experimentos Sugeridos")
    lines.append("")
    lines.append("- [ ] Testar ajuste de SL em ±10% nos TFs lucrativos")
    lines.append(
        "- [ ] Testar filtro MTF: só operar se TF superior também der sinal")
    lines.append(
        "- [ ] Avaliar janela horária (ex: evitar abertura e fechamento)")
    lines.append("- [ ] Comparar desempenho em dias da semana (seg-sex)")
    lines.append(
        "- [ ] Avaliar stop por resultado diário (-3 ops perdidas = sem operar)")
    lines.append("")
    lines.append("---")
    lines.append(
        f"*Gerado automaticamente por `analisar_grupos.py` em {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

    return '\n'.join(lines)


# ---- MAIN ----
csv_files = [f for f in os.listdir(RESULT_DIR) if f.endswith('.csv')]
groups = group_files(csv_files)

print(f"Grupos identificados: {list(groups.keys())}")

for group_name, files in groups.items():
    print(f"\n=== {group_name} ({len(files)} arquivos) ===")
    files_data = []
    for fname in sorted(files):
        path = os.path.join(RESULT_DIR, fname)
        r = analyze_csv(path)
        status = f"✓ {r['total']} ops PnL={r['pnl_total']:+.0f}" if r else "✗ sem dados"
        print(f"  {fname}: {status}")
        files_data.append((fname, r))

    if not any(r for _, r in files_data):
        print(f"  [SKIP] Nenhum dado válido")
        continue

    md_content = generate_md(group_name, files_data)
    md_path = os.path.join(RESULT_DIR, f"ANALISE-{group_name}.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"  → {md_path}")

print("\nConcluído!")
