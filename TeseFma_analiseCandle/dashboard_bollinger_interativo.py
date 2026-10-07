"""Gera um dashboard interativo descritivo de ignição e saturação Bollinger no WIN."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from plotly.offline import get_plotlyjs

BASE = Path(__file__).resolve().parent
OUT = BASE / "graficos_motor" / "bollinger_ignicao_saturacao_win.html"
TIMEFRAMES = ["5min", "15min", "30min", "60min"]
ROOT = BASE.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from gerar_graficos_motor import series_por_tf


def carregar_dados() -> dict:
    """Serializa apenas os campos necessários à exploração no navegador."""
    saida = {}
    for tf in TIMEFRAMES:
        d = series_por_tf(tf)
        if d.empty:
            continue
        d = d.sort_values("dt", kind="stable").reset_index(drop=True)
        rng_atr = d["rng"] / d["atr"].where(d["atr"] > 0)
        saida[tf] = {
            "dt": d["dt"].dt.strftime("%Y-%m-%dT%H:%M:%S").tolist(),
            "dia": d["dia"].dt.strftime("%Y-%m-%d").tolist(),
            "close": d["c"].round(4).fillna(0).tolist(),
            "m": d["m"].round(6).fillna(0).tolist(),
            "a": d["a"].round(6).fillna(0).tolist(),
            "F": d["F"].round(6).fillna(0).tolist(),
            "z": d["z"].round(6).fillna(0).tolist(),
            "rng_atr": rng_atr.round(6).fillna(0).tolist(),
        }
        saida[tf]["data_start"] = str(d["dt"].min().date())
        saida[tf]["data_end"] = str(d["dt"].max().date())
        saida[tf]["symbols"] = sorted(d["simbolo"].dropna().unique().tolist()) if "simbolo" in d else []
    return saida


def build_html() -> str:
    payload = json.dumps(carregar_dados(), separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    plotly_js = get_plotlyjs()
    return """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WIN | Ignição e Saturação Bollinger</title>
<script>""" + plotly_js + """</script>
<style>
:root{color-scheme:light;--ink:#142033;--muted:#617087;--line:#dce4ef;--blue:#3157d5;--green:#09866b;--red:#d34b55;--bg:#f3f6fb}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 Inter,Segoe UI,Arial,sans-serif}
main{max-width:1500px;margin:auto;padding:24px}.hero,.panel,.metric{background:#fff;border:1px solid var(--line);border-radius:16px;box-shadow:0 5px 20px #1420330a}
.hero{padding:24px;margin-bottom:16px}.hero h1{margin:0 0 5px;font-size:27px}.hero p{margin:5px 0;color:var(--muted)}
.controls{display:grid;grid-template-columns:repeat(5,minmax(120px,1fr));gap:12px;margin:16px 0}.field{background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px 12px}.field label{display:block;font-size:11px;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.05em}.field select,.field input{width:100%;margin-top:5px;border:0;background:transparent;color:var(--ink);font:inherit;outline:none}
.metrics{display:grid;grid-template-columns:repeat(4,minmax(150px,1fr));gap:12px;margin:12px 0}.metric{padding:14px 16px}.metric small{color:var(--muted);display:block}.metric strong{font-size:22px;display:block;margin-top:4px}
.panel{padding:14px 16px;margin:12px 0}.panel h2{font-size:17px;margin:3px 0}.plot{height:390px}.split{display:grid;grid-template-columns:1.15fr .85fr;gap:12px}.tablewrap{overflow:auto}table{width:100%;border-collapse:collapse;margin-top:10px}th,td{padding:10px 9px;text-align:right;border-bottom:1px solid var(--line);white-space:nowrap}th:first-child,td:first-child{text-align:left}th{font-size:11px;color:var(--muted);text-transform:uppercase}.pill{display:inline-block;border-radius:99px;padding:3px 9px;font-size:12px;font-weight:700}.ign{background:#eaf0ff;color:#3157d5}.sat{background:#fff0e8;color:#ba5424}.note{color:var(--muted);font-size:12px}.warning{border-left:4px solid #e5a83b;background:#fff9eb;padding:12px 14px;border-radius:8px;margin-top:12px}
.parity{border-left:4px solid #c78222;background:#fff8e9;padding:14px 16px;border-radius:10px;margin:12px 0}.parity strong{color:#8a5511}.parity ul{margin:7px 0 0;padding-left:20px}.parity li{margin:3px 0}
@media(max-width:900px){.controls{grid-template-columns:repeat(2,1fr)}.metrics{grid-template-columns:repeat(2,1fr)}.split{grid-template-columns:1fr}.plot{height:330px}}@media(max-width:520px){main{padding:12px}.controls{grid-template-columns:1fr 1fr}.hero h1{font-size:22px}}
</style></head><body><main>
<section class="hero"><h1>WIN · Ignição e saturação Bollinger</h1>
<p>Exploração descritiva do escore F normalizado pela média e desvio-padrão móveis do próprio motor.</p>
<div class="warning"><b>Leitura das zonas:</b> ignição = escore direcional de k₁σ até abaixo de k₂σ; saturação = escore direcional ≥ k₂σ. A saturação é o nível mais extremo dentro do mesmo sistema, não uma previsão de reversão.</div></section>
<section class="parity"><strong>PARIDADE NTSL × PYTHON: NÃO VALIDADA NESTE DASHBOARD</strong>
<ul><li>Os pontos e estatísticas abaixo vêm da série Python; não estão casados com casos Profit por timestamp.</li>
<li>O repositório tem documentação metodológica, mas não contém atualmente o gerador nem os CSVs de casos/histórico/observações citados nela.</li>
<li>Antes de interpretar cores do Profit como o mesmo estado, compare timestamp, OHLC, volume, m, a, F, μ, σ, z, família e estado.</li></ul></section>
<section class="controls">
<div class="field"><label>Timeframe</label><select id="tf"></select></div>
<div class="field"><label>Data inicial</label><input id="from" type="date"></div><div class="field"><label>Data final</label><input id="to" type="date"></div>
<div class="field"><label>Ignição k₁ (σ)</label><input id="k1" type="number" min="0.1" max="5" step="0.1" value="1.5"></div>
<div class="field"><label>Saturação k₂ (σ)</label><input id="k2" type="number" min="0.2" max="6" step="0.1" value="2.5"></div>
</section>
<section class="metrics"><div class="metric"><small>Candles na seleção</small><strong id="n-bars">—</strong></div><div class="metric"><small>Ign. · ocorrências / taxa</small><strong id="ign-count">—</strong></div><div class="metric"><small>Sat. · ocorrências / taxa</small><strong id="sat-count">—</strong></div><div class="metric"><small>Maior |z| observado</small><strong id="max-z">—</strong></div></section>
<p class="note" id="data-source"></p>
<section class="panel"><h2>Preço e eventos coloridos por zona</h2><div id="price" class="plot"></div><p class="note">Pontos sobrepostos indicam candles classificados. Use zoom e hover para inspecionar os timestamps.</p></section>
<section class="split"><div class="panel"><h2>Escore direcional z · faixas ajustáveis</h2><div id="zplot" class="plot"></div></div><div class="panel"><h2>Decomposição do candle · massa × aceleração</h2><div id="scatter" class="plot"></div><p class="note">m = corpo/range; a = volume/média dos 20 candles anteriores. F = m × a × 100. O escore Bollinger é aplicado sobre F.</p></div></section>
<section class="panel"><h2>Resumo descritivo por classe</h2><div class="tablewrap"><table><thead><tr><th>Classe</th><th>Eventos</th><th>Frequência</th><th>Range seguinte / ATR</th><th>Retorno alinhado h1</th><th>Retorno alinhado h3</th></tr></thead><tbody id="summary"></tbody></table></div>
<p class="note">Retorno alinhado é sinal(F) × variação do fechamento, em pontos. Range/ATR é o do candle futuro. Horizontes são candles do mesmo dia; métricas são descritivas, não estimativas de lucro nem teste de significância.</p></section>
<p class="note">Dados históricos WIN contínuos do repositório; o agregador seleciona o contrato de maior volume por dia entre os arquivos encontrados. Cálculo usa a definição Python atual, inclusive a janela móvel que inclui o candle classificado. Continuidade de contrato e cobertura variam. Isto não substitui o lote de paridade WINQ26 Jun–Jul/2026.</p>
</main><script>
const DATA = __DATA__;
const $=id=>document.getElementById(id), COLORS={ign:'#3157d5',sat:'#ef7a3a',bull:'#09866b',bear:'#d34b55'};
const tfs=Object.keys(DATA); for(const tf of tfs){const o=document.createElement('option');o.value=tf;o.textContent=tf;$('tf').appendChild(o)}
if(tfs.includes('5min')) $('tf').value='5min';
const dateBounds=()=>{const d=DATA[$('tf').value];$('from').value=d.data_start;$('to').value=d.data_end;$('from').min=d.data_start;$('from').max=d.data_end;$('to').min=d.data_start;$('to').max=d.data_end};
function fixed(n,d=2){return Number.isFinite(n)?n.toFixed(d):'—'}
function avg(vals){return vals.length?vals.reduce((a,b)=>a+b,0)/vals.length:NaN}
function update(){
 const d=DATA[$('tf').value]; if(!d)return;
 let from=$('from').value||d.dia[0],to=$('to').value||d.dia[d.dia.length-1];
 let k1=Number($('k1').value),k2=Number($('k2').value); if(!Number.isFinite(k1)||!Number.isFinite(k2)||k1<=0||k2<=k1){$('summary').innerHTML='<tr><td colspan="6">Ajuste k₂ para ficar maior que k₁ e ambos acima de zero.</td></tr>';return}
 const ix=[];for(let i=0;i<d.dt.length;i++)if(d.dia[i]>=from&&d.dia[i]<=to)ix.push(i);
 if(!ix.length){$('summary').innerHTML='<tr><td colspan="6">Sem barras no intervalo escolhido.</td></tr>';return}
 $('data-source').textContent=`Série ${$('tf').value}: ${d.data_start} a ${d.data_end} · contratos agregados: ${d.symbols.join(', ')||'não identificado'}. A seleção do arquivo contínuo segue o critério de maior volume diário do agregador.`;
 const cats={Ignicao:[],Saturacao:[],Neutro:[]};let maxz=0;
 for(const i of ix){const score=d.z[i]*Math.sign(d.F[i]);maxz=Math.max(maxz,Math.abs(d.z[i]));if(score>=k2)cats.Saturacao.push(i);else if(score>=k1)cats.Ignicao.push(i);else cats.Neutro.push(i)}
 $('n-bars').textContent=ix.length.toLocaleString('pt-BR');$('ign-count').textContent=`${cats.Ignicao.length.toLocaleString('pt-BR')} · ${fixed(100*cats.Ignicao.length/ix.length,1)}%`;$('sat-count').textContent=`${cats.Saturacao.length.toLocaleString('pt-BR')} · ${fixed(100*cats.Saturacao.length/ix.length,1)}%`;$('max-z').textContent=fixed(maxz,2)+'σ';
 const x=ix.map(i=>d.dt[i]), close=ix.map(i=>d.close[i]), zd=ix.map(i=>d.z[i]*Math.sign(d.F[i]));
 const priceTr=[{x,y:close,type:'scattergl',mode:'lines',name:'Fechamento',line:{color:'#8995a8',width:1}}];
 for(const [name,color] of [['Ignicao',COLORS.ign],['Saturacao',COLORS.sat]]){const ids=cats[name];priceTr.push({x:ids.map(i=>d.dt[i]),y:ids.map(i=>d.close[i]),type:'scattergl',mode:'markers',name:name==='Ignicao'?'Ignição':'Saturação',marker:{color,size:6,opacity:.8},customdata:ids.map(i=>[d.z[i],d.F[i],d.m[i],d.a[i]]),hovertemplate:'%{x}<br>Close=%{y:.0f}<br>z=%{customdata[0]:.2f}<br>F=%{customdata[1]:.1f}<br>m=%{customdata[2]:.3f}<br>a=%{customdata[3]:.2f}<extra></extra>'})}
 Plotly.react('price',priceTr,{margin:{l:55,r:20,t:18,b:45},xaxis:{rangeslider:{visible:false}},yaxis:{title:'WIN · pontos'},legend:{orientation:'h',y:1.12},paper_bgcolor:'white',plot_bgcolor:'white'}, {responsive:true,displaylogo:false});
 Plotly.react('zplot',[{x,y:zd,type:'scattergl',mode:'lines',name:'z direcional',line:{color:'#64748b',width:1}},{x,y:zd.map(v=>v>=k1?v:null),type:'scattergl',mode:'markers',name:'Ignição+',marker:{color:COLORS.ign,size:5}},{x,y:zd.map(v=>v>=k2?v:null),type:'scattergl',mode:'markers',name:'Saturação+',marker:{color:COLORS.sat,size:6}}],{margin:{l:55,r:15,t:18,b:45},xaxis:{},yaxis:{title:'sign(F) × z',zeroline:true},shapes:[{type:'line',xref:'paper',x0:0,x1:1,y0:k1,y1:k1,line:{color:COLORS.ign,dash:'dot'}},{type:'line',xref:'paper',x0:0,x1:1,y0:k2,y1:k2,line:{color:COLORS.sat,dash:'dot'}}],legend:{orientation:'h',y:1.12},paper_bgcolor:'white',plot_bgcolor:'white'},{responsive:true,displaylogo:false});
 const sc=[];for(const [name,color] of [['Neutro','#aab4c3'],['Ignicao',COLORS.ign],['Saturacao',COLORS.sat]]){const ids=cats[name];sc.push({x:ids.map(i=>d.m[i]),y:ids.map(i=>d.a[i]),type:'scattergl',mode:'markers',name:name==='Neutro'?'Demais':name==='Ignicao'?'Ignição':'Saturação',marker:{color,size:name==='Neutro'?4:7,opacity:.55},customdata:ids.map(i=>[d.F[i],d.z[i]]),hovertemplate:'m=%{x:.3f}<br>a=%{y:.2f}<br>F=%{customdata[0]:.1f}<br>z=%{customdata[1]:.2f}<extra></extra>'})}
 Plotly.react('scatter',sc,{margin:{l:55,r:12,t:18,b:50},xaxis:{title:'m · corpo/range'},yaxis:{title:'a · volume/média anterior',rangemode:'tozero'},legend:{orientation:'h',y:1.12},paper_bgcolor:'white',plot_bgcolor:'white'},{responsive:true,displaylogo:false});
 const groups=[['Ignição',cats.Ignicao],['Saturação',cats.Saturacao],['Demais candles',cats.Neutro]];
 $('summary').innerHTML=groups.map(([name,ids])=>{const r1=[],r3=[],rng=[];for(const i of ids){if(i+1<d.dt.length&&d.dia[i+1]===d.dia[i]){const s=Math.sign(d.F[i]);r1.push(s*(d.close[i+1]-d.close[i]));rng.push(d.rng_atr[i+1])}if(i+3<d.dt.length&&d.dia[i+3]===d.dia[i])r3.push(Math.sign(d.F[i])*(d.close[i+3]-d.close[i]))}const pct=100*ids.length/ix.length;return `<tr><td>${name}</td><td>${ids.length.toLocaleString('pt-BR')}</td><td>${fixed(pct,2)}%</td><td>${fixed(avg(rng),3)}</td><td>${fixed(avg(r1),1)} pts</td><td>${fixed(avg(r3),1)} pts</td></tr>`}).join('');
}
$('tf').addEventListener('change',()=>{dateBounds();update()});for(const id of ['from','to','k1','k2'])$(id).addEventListener('change',update);dateBounds();update();
</script></body></html>""".replace("__DATA__", payload)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_html(), encoding="utf-8")
    print(f"Dashboard criado: {OUT}")
    print(f"Tamanho: {OUT.stat().st_size / (1024 * 1024):.1f} MiB")


if __name__ == "__main__":
    main()