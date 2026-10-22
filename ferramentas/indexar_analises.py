"""Gera ``docs/04_REGISTRO_ANALISES.md`` a partir de ``docs/registro/analises.csv``.

Uso: python ferramentas/indexar_analises.py
"""

from __future__ import annotations

import csv
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FONTE = RAIZ / "docs" / "registro" / "analises.csv"
SAIDA = RAIZ / "docs" / "04_REGISTRO_ANALISES.md"
CLASSES = {"direcao", "volatilidade", "geometria", "execucao", "descritiva", "econofisica", "legado"}
DECISOES = {"USAR", "NAO_USAR", "CONDICIONAL", "PENDENTE", "FORA_DO_PROTOCOLO"}
ORDEM = ["USAR", "CONDICIONAL", "PENDENTE", "NAO_USAR", "FORA_DO_PROTOCOLO"]
ROTULO = {
    "USAR": "Entra no robô",
    "CONDICIONAL": "Só entra com a ressalva registrada",
    "PENDENTE": "Ainda não decide parâmetro",
    "NAO_USAR": "Fica fora do robô",
    "FORA_DO_PROTOCOLO": "Fora do protocolo (não usar como evidência)",
}


def main() -> None:
    with FONTE.open(encoding="utf-8") as f:
        linhas = list(csv.DictReader(f, delimiter=";"))
    erros = []
    for r in linhas:
        if r["classe"] not in CLASSES:
            erros.append(f"{r['id']}: classe {r['classe']}")
        if r["decisao"] not in DECISOES:
            erros.append(f"{r['id']}: decisao {r['decisao']}")
        if r["arquivo"] != "—" and not (RAIZ / r["arquivo"]).exists():
            erros.append(f"{r['id']}: arquivo ausente {r['arquivo']}")
    if erros:
        raise SystemExit("registro inválido:\n" + "\n".join(erros))

    md = ["# Registro de análises\n",
          "> Gerado por `ferramentas/indexar_analises.py` a partir de `docs/registro/analises.csv`. "
          "Para incluir uma análise, acrescente uma linha no CSV e rode o script. "
          "Vocabulário e regras: `docs/01_CONVENCOES.md` §8. A decisão de cada peça no robô está em `docs/05_TRILHA_ROBO.md`.\n",
          "## Contagem\n",
          "| decisão | quantas |", "|---|---|"]
    for d in ORDEM:
        md.append(f"| {ROTULO[d]} | {sum(r['decisao'] == d for r in linhas)} |")
    md.append("\n## Por decisão\n")
    for d in ORDEM:
        grupo = [r for r in linhas if r["decisao"] == d]
        if not grupo:
            continue
        md.append(f"### {ROTULO[d]}\n")
        md.append("| id | classe | análise | período | nota |")
        md.append("|---|---|---|---|---|")
        for r in grupo:
            link = f"[`{r['titulo']}`](../{r['arquivo']})" if r["arquivo"] != "—" else r["titulo"]
            md.append(f"| {r['id']} | {r['classe']} | {link} | {r['periodo']} | {r['nota']} |")
        md.append("")
    md.append("Hipóteses ligadas a cada análise estão na coluna `hipoteses` do CSV e no [`INDICE_HIPOTESES.md`](INDICE_HIPOTESES.md).\n")
    SAIDA.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("gravado", SAIDA.relative_to(RAIZ), len(linhas), "análises")


if __name__ == "__main__":
    main()
