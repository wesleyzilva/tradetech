"""Gera ``docs/INDICE_HIPOTESES.md``: índice único de todas as hipóteses dos motores.

Lê as tabelas de ``HIPOTESES.md`` de cada motor/tese (sem alterá-las) e consolida id, grupo, enunciado e veredito.

Uso (a partir da raiz do repositório):
    python ferramentas/indexar_hipoteses.py
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "docs" / "INDICE_HIPOTESES.md"

FONTES = [
    ("M01 · cores", "motores/M01_fma_forca/teses/cores/HIPOTESES.md", r"H\d+"),
    ("M01 · áreas", "motores/M01_fma_forca/teses/areas/HIPOTESES.md", r"A\d+"),
    ("M01 · reversão", "motores/M01_fma_forca/teses/reversao/HIPOTESES.md", r"R\d+"),
    ("M02 · microestrutura", "motores/M02_microestrutura_barreiras/HIPOTESES.md", r"MB-H\d+"),
    ("M16 · confluência multi-TF", "motores/M16_confluencia_multitf/HIPOTESES.md", r"CF-H\d+"),
]
VEREDITOS = ["CONFIRMADA", "PARCIAL", "INCONCLUSIVA", "NÃO SUPORTADA", "REFUTADA", "PENDENTE"]


def celulas(linha: str) -> list[str]:
    partes = re.split(r"(?:^|(?<=\s))\|(?=\s|$)", linha.strip())
    return [p.strip().replace("\\|", "|") for p in partes if p.strip() != ""]


def limpar(txt: str, n: int = 140) -> str:
    txt = re.sub(r"\*\*|`", "", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    txt = txt if len(txt) <= n else txt[: n - 1].rstrip() + "…"
    return txt.replace("|", "\\|")


def veredito(txt: str) -> str:
    t = re.sub(r"\*\*|`", "", txt).upper()
    for v in VEREDITOS:
        if v in t:
            return v
    return "PENDENTE"


def extrair(caminho: Path, padrao: str) -> list[dict]:
    """Prioridade por id: painel (≥ 7 colunas) > linha com veredito em negrito (fichas) > demais (backlog/pendente)."""
    out: dict[str, tuple[int, dict]] = {}
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if not linha.startswith("|"):
            continue
        c = celulas(linha)
        if not c or not re.fullmatch(padrao, c[0]) or len(c) < 2:
            continue
        id_, n = c[0], len(c)
        em_negrito = re.search(r"\*\*(CONFIRMADA|PARCIAL|INCONCLUSIVA|NÃO SUPORTADA|REFUTADA)\*\*", linha)
        if n >= 7 and "cores" in str(caminho):
            prio, reg = 2, {"id": id_, "grupo": c[1], "texto": c[2], "veredito": veredito(c[5])}
        elif n == 6:
            prio, reg = 2, {"id": id_, "grupo": "", "texto": c[1], "veredito": veredito(c[5]) if c[5] not in ("—", "") else veredito(c[4])}
        elif n == 4 and "cores" not in str(caminho):
            prio, reg = 2, {"id": id_, "grupo": "", "texto": c[1], "veredito": veredito(c[3])}
        elif n == 5 and "reversao" in str(caminho):
            prio, reg = 2, {"id": id_, "grupo": "", "texto": c[1], "veredito": veredito(c[4])}
        elif em_negrito:
            prio, reg = 1, {"id": id_, "grupo": "", "texto": c[1], "veredito": em_negrito.group(1)}
        else:
            prio, reg = 0, {"id": id_, "grupo": "", "texto": c[1], "veredito": "PENDENTE"}
        if id_ not in out or prio > out[id_][0]:
            out[id_] = (prio, reg)
    return sorted((v[1] for v in out.values()), key=lambda r: int(re.sub(r"\D", "", r["id"])))


def main() -> None:
    md = ["# Índice único de hipóteses", "",
          "> **Gerado por** `ferramentas/indexar_hipoteses.py` — não editar à mão. A fonte de cada veredito é o `HIPOTESES.md` do motor/tese (coluna *Fonte*). "
          "Para criar uma hipótese nova, ver `docs/01_CONVENCOES.md` §2 e `docs/templates/HIPOTESE.md`.", ""]
    resumo = []
    corpo = []
    for nome, rel, padrao in FONTES:
        p = RAIZ / rel
        if not p.exists():
            continue
        regs = extrair(p, padrao)
        cont = Counter(r["veredito"] for r in regs)
        resumo.append((nome, len(regs), cont))
        corpo.append(f"## {nome}\n\nFonte: [`{rel}`](../{rel})\n")
        corpo.append("| id | grupo | hipótese | veredito |")
        corpo.append("|---|---|---|---|")
        for r in regs:
            corpo.append(f"| {r['id']} | {r['grupo']} | {limpar(r['texto'])} | {r['veredito']} |")
        corpo.append("")
    md.append("## Resumo\n")
    md.append("| motor / tese | hipóteses | " + " | ".join(VEREDITOS) + " |")
    md.append("|---|---|" + "|".join("---" for _ in VEREDITOS) + "|")
    for nome, n, cont in resumo:
        md.append(f"| {nome} | {n} | " + " | ".join(str(cont.get(v, 0)) for v in VEREDITOS) + " |")
    md.append("")
    md.extend(corpo)
    SAIDA.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"gravado {SAIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
