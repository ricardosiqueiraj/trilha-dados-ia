#!/usr/bin/env python3
"""Gera os trechos automáticos do README.md, o PLANO.md e o PROGRESSO.md a partir de dados/.

Uso:
  python3 scripts/atualizar.py              gera tudo a partir de dados/progresso.json
  python3 scripts/atualizar.py --db PASTA   antes, monta dados/progresso.json a partir da
                                            exportação da página de acompanhamento
                                            (PASTA/progress, PASTA/log, PASTA/settings, PASTA/accounts)

Só usa a biblioteca padrão do Python 3.9+.
"""
import argparse
import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
FUSO = timezone(timedelta(hours=-3))  # horário de Brasília, sem horário de verão desde 2019
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
USUARIO_GITHUB = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}$")
USUARIO = re.compile(r"^\w[\w.-]{0,99}$")
METAS = (4, 6, 8, 10, 12, 15)
PERFIS = {
    "github": ("GitHub", "https://github.com/{u}"),
    "kaggle": ("Kaggle", "https://www.kaggle.com/{u}"),
    "huggingface": ("Hugging Face", "https://huggingface.co/{u}"),
    "linkedin": ("LinkedIn", "https://www.linkedin.com/in/{u}/"),
}
SITUACAO = {"queued": "Na fila", "running": "Em andamento", "done": "Concluída", "late": "Atrasada"}
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
         "setembro", "outubro", "novembro", "dezembro"]


# ---------- utilidades ----------
def niveis_ingles(plano):
    """Os níveis da faixa de inglês no mesmo formato das fases (numero I1, I2...)."""
    ing = plano.get("ingles") or {}
    return [dict(n, numero=f"I{n['nivel']}") for n in ing.get("niveis", [])]


def ler_json(caminho):
    try:
        return json.loads(Path(caminho).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def gravar(caminho, texto):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    if not caminho.exists() or caminho.read_text(encoding="utf-8") != texto:
        caminho.write_text(texto, encoding="utf-8")


def data_br(iso):
    return f"{iso[8:10]}/{iso[5:7]}/{iso[0:4]}"


def dia_mes(d):
    return f"{d.day:02d}/{d.month:02d}"


def horas(h):
    txt = f"{h:.2f}".rstrip("0").rstrip(".")
    return txt.replace(".", ",") + " h"


def barra(p, n=20):
    cheio = round(max(0.0, min(1.0, p)) * n)
    return "█" * cheio + "░" * (n - cheio)


def celula(texto):
    """Texto seguro para uma célula de tabela Markdown."""
    t = " ".join(str(texto).split())
    return t.replace("\\", "\\\\").replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")


def inicio_semana(d):
    return d - timedelta(days=d.weekday())


# ---------- dados ----------
def montar_progresso(pasta, plano, agora):
    """Lê a exportação do banco da página e devolve o conteúdo de dados/progresso.json."""
    pasta = Path(pasta)
    ids = {e["id"] for f in plano["fases"] + niveis_ingles(plano) for e in f["etapas"]}

    concluidas = {}
    for arq in sorted((pasta / "progress").glob("*.json")):
        d = ler_json(arq)
        if arq.stem in ids and isinstance(d, dict) and isinstance(d.get("doneAt"), str) and ISO.match(d["doneAt"]):
            concluidas[arq.stem] = d["doneAt"]

    sessoes = []
    for arq in sorted((pasta / "log").glob("*.json")):
        d = ler_json(arq)
        if not isinstance(d, dict):
            continue
        try:
            h = float(d.get("hours"))
        except (TypeError, ValueError):
            continue
        dia = d.get("date")
        if not (isinstance(dia, str) and ISO.match(dia) and 0 < h <= 24):
            continue
        nota = d.get("note") if isinstance(d.get("note"), str) else ""
        criado = d.get("createdAt") if isinstance(d.get("createdAt"), str) else ""
        sessoes.append({"data": dia, "horas": round(h, 2), "nota": " ".join(nota.split())[:140], "_c": criado})
    sessoes.sort(key=lambda s: (s["data"], s["_c"]))
    for s in sessoes:
        del s["_c"]

    meta = 10
    ajustes = ler_json(pasta / "settings" / "plan.json")
    if isinstance(ajustes, dict) and ajustes.get("weeklyGoal") in METAS:
        meta = ajustes["weeklyGoal"]

    perfis = {k: "" for k in PERFIS}
    contas = {}
    for arq in sorted((pasta / "accounts").glob("*.json")):
        d = ler_json(arq)
        if not isinstance(d, dict):
            continue
        usuario = d.get("user") if isinstance(d.get("user"), str) else ""
        if arq.stem in perfis:
            regra = USUARIO_GITHUB if arq.stem == "github" else USUARIO
            perfis[arq.stem] = usuario if regra.match(usuario) else ""
        contas[arq.stem] = {"criada": d.get("created") is True, "ligada": d.get("linked") is True}

    return {
        "atualizado_em": agora.isoformat(timespec="minutes"),
        "meta_semanal_h": meta,
        "etapas_concluidas": dict(sorted(concluidas.items())),
        "sessoes": sessoes,
        "perfis": perfis,
        "contas": dict(sorted(contas.items())),
    }


def situacao_fase(fase, feitas, hoje):
    if feitas == len(fase["etapas"]):
        return "done"
    if hoje > fase["fim"]:
        return "late"
    if feitas > 0 or hoje >= fase["inicio"]:
        return "running"
    return "queued"


def resumo(plano, prog, hoje):
    concl = prog["etapas_concluidas"]
    etapas = [(f, e) for f in plano["fases"] for e in f["etapas"]]
    feitas = sum(1 for _, e in etapas if e["id"] in concl)
    proxima = next(((f, e) for f, e in etapas if e["id"] not in concl), None)
    por_semana = {}
    for s in prog["sessoes"]:
        k = inicio_semana(date.fromisoformat(s["data"]))
        por_semana[k] = por_semana.get(k, 0) + s["horas"]
    semana = inicio_semana(date.fromisoformat(hoje))
    return {
        "total": len(etapas), "feitas": feitas, "proxima": proxima,
        "por_semana": por_semana, "semana": semana,
        "nesta_semana": por_semana.get(semana, 0.0),
        "horas_total": sum(s["horas"] for s in prog["sessoes"]),
        "horas_plano": round(sum(e["horas"] for _, e in etapas) / 10) * 10,
    }


def quando(prog):
    agora = datetime.fromisoformat(prog["atualizado_em"]).astimezone(FUSO)
    return f"{agora.day:02d}/{agora.month:02d}/{agora.year} às {agora.hour:02d}h{agora.minute:02d}", agora.date().isoformat()


# ---------- README ----------
def bloco_progresso(plano, prog, r, hoje, texto_quando):
    pct = r["feitas"] / r["total"]
    linhas = ["## Progresso", "",
              f"`{barra(pct)}` **{round(pct * 100)}%** · {r['feitas']} de {r['total']} etapas concluídas", ""]
    if r["proxima"]:
        f, e = r["proxima"]
        linhas.append(f"- **Fase atual:** Fase {f['numero']} · {f['titulo']}")
        linhas.append(f"- **Próxima etapa:** {e['rotulo']} · {e['titulo']}")
    else:
        linhas.append("- **Plano concluído:** todas as etapas feitas.")
    linhas.append(f"- **Horas de estudo:** {horas(r['horas_total'])} no total, de ≈ {r['horas_plano']} h planejadas · "
                  f"{horas(r['nesta_semana'])} nesta semana, com meta de {prog['meta_semanal_h']} h")
    linhas.append(f"- **Atualizado em:** {texto_quando}")
    linhas += ["", "| Fase | Período | Etapas | Situação |", "|---|---|---|---|"]
    for f in plano["fases"]:
        n = sum(1 for e in f["etapas"] if e["id"] in prog["etapas_concluidas"])
        st = situacao_fase(f, n, hoje)
        linhas.append(f"| {f['numero']} · {celula(f['titulo'])} | {celula(f['periodo'])} | {n}/{len(f['etapas'])} | {SITUACAO[st]} |")
    niveis = niveis_ingles(plano)
    if niveis:
        concl = prog["etapas_concluidas"]
        etapas = [(f, e) for f in niveis for e in f["etapas"]]
        feitas = sum(1 for _, e in etapas if e["id"] in concl)
        prox = next(((f, e) for f, e in etapas if e["id"] not in concl), None)
        linhas += ["", "### Inglês, do básico ao avançado", "",
                   f"`{barra(feitas / len(etapas))}` **{round(feitas / len(etapas) * 100)}%** · {feitas} de {len(etapas)} etapas"
                   + (f" · nível atual: {prox[0]['titulo']} · próxima: {prox[1]['rotulo']} · {prox[1]['titulo']}" if prox else " · concluído")]
    linhas += ["", "O plano completo, com os cursos gratuitos de cada etapa, está em [PLANO.md](PLANO.md). "
               "As horas e as etapas concluídas, semana a semana, estão em [PROGRESSO.md](PROGRESSO.md)."]
    return "\n".join(linhas)


def bloco_projetos(plano, prog, hoje):
    linhas = ["## Projetos do portfólio", "",
              "Cada projeto terá um repositório próprio, com README explicando o problema, a arquitetura e como rodar.", "",
              "| Projeto | Fase | Situação |", "|---|---|---|"]
    for f in plano["fases"]:
        n = sum(1 for e in f["etapas"] if e["id"] in prog["etapas_concluidas"])
        st = situacao_fase(f, n, hoje)
        for e in f["etapas"]:
            if e["tipo"] != "Projeto":
                continue
            if e["id"] in prog["etapas_concluidas"]:
                sit = "Concluído em " + data_br(prog["etapas_concluidas"][e["id"]])
            elif st in ("running", "late"):
                sit = "Nesta fase"
            else:
                sit = "Na fila"
            linhas.append(f"| {celula(e['titulo'])} | {f['numero']} | {sit} |")
    return "\n".join(linhas)


def bloco_perfis(prog):
    itens = [f"- {nome}: [{u}]({modelo.format(u=quote(u))})"
             for chave, (nome, modelo) in PERFIS.items() if (u := prog["perfis"].get(chave))]
    return "\n".join(["## Onde me encontrar", ""] + (itens or ["- Em breve."]))


def trocar_bloco(texto, nome, conteudo):
    padrao = re.compile(rf"(<!-- AUTO:{nome} -->)(.*?)(<!-- /AUTO:{nome} -->)", re.S)
    if not padrao.search(texto):
        raise SystemExit(f"README.md sem o marcador AUTO:{nome}")
    return padrao.sub(lambda m: f"{m.group(1)}\n{conteudo}\n{m.group(3)}", texto, count=1)


# ---------- PLANO.md ----------
def gerar_plano(plano, prog, hoje):
    concl = prog["etapas_concluidas"]
    total = sum(len(f["etapas"]) for f in plano["fases"])
    linhas = [f"# Plano de estudos: {plano['titulo']}", "",
              f"{plano['resumo']} São {total} etapas em {len(plano['fases'])} fases, de {plano['periodo']}, "
              "só com cursos gratuitos. As etapas marcadas já foram concluídas.", ""]
    trilha = None
    for f in plano["fases"]:
        if f["trilha"] != trilha:
            trilha = f["trilha"]
            t = plano["trilhas"][str(trilha)]
            linhas += [f"## {t['titulo']} ({t['rotulo']})", "", t["descricao"], ""]
        n = sum(1 for e in f["etapas"] if e["id"] in concl)
        h = sum(e["horas"] for e in f["etapas"])
        st = SITUACAO[situacao_fase(f, n, hoje)]
        linhas += [f"### Fase {f['numero']} · {f['titulo']}", "",
                   f"**Período:** {f['periodo']} · ≈ {horas(h)} de estudo · **Situação:** {st} ({n}/{len(f['etapas'])})", "",
                   f"**Objetivo:** {f['objetivo']}", ""]
        if f.get("nota"):
            linhas += [f"_{f['nota']}_", ""]
        for e in f["etapas"]:
            feito = e["id"] in concl
            carga = f"≈ {horas(e['horas'])}" if e["horas"] else ("no trabalho" if e["tipo"] == "Trabalho" else "contínuo")
            topo = f"- [{'x' if feito else ' '}] **{e['rotulo']} · {e['titulo']}** ({carga})"
            if feito:
                topo += f" · concluída em {data_br(concl[e['id']])}"
            linhas.append(topo + "\\")
            if e["links"]:
                links = " · ".join(f"[{l['titulo']}]({l['url']}) ({l['idioma']})" for l in e["links"])
                linhas.append(f"  {e['detalhe']}\\")
                linhas.append(f"  Links: {links}")
            else:
                linhas.append(f"  {e['detalhe']}")
        linhas.append("")
    ing = plano.get("ingles")
    if ing:
        linhas += [f"## {ing['titulo']} ({ing['rotulo']})", "", ing["descricao"], ""]
        for f in niveis_ingles(plano):
            n = sum(1 for e in f["etapas"] if e["id"] in concl)
            h = sum(e["horas"] for e in f["etapas"])
            st = SITUACAO[situacao_fase(f, n, hoje)]
            linhas += [f"### Nível {f['nivel']} · {f['titulo']}", "",
                       f"**Período:** {f['periodo']} · ≈ {horas(h)} de estudo · **Situação:** {st} ({n}/{len(f['etapas'])})", "",
                       f"**Objetivo:** {f['objetivo']}", ""]
            if f.get("nota"):
                linhas += [f"_{f['nota']}_", ""]
            for e in f["etapas"]:
                feito = e["id"] in concl
                topo = f"- [{'x' if feito else ' '}] **{e['rotulo']} · {e['titulo']}** (≈ {horas(e['horas'])})"
                if feito:
                    topo += f" · concluída em {data_br(concl[e['id']])}"
                linhas.append(topo + "\\")
                if e["links"]:
                    links = " · ".join(f"[{l['titulo']}]({l['url']}) ({l['idioma']})" for l in e["links"])
                    linhas.append(f"  {e['detalhe']}\\")
                    linhas.append(f"  Links: {links}")
                else:
                    linhas.append(f"  {e['detalhe']}")
            linhas.append("")
    linhas += ["## Certificações", "", "| Certificação | Prova | Quando | Observação |", "|---|---|---|---|"]
    for c in plano["certificacoes"]:
        nome = f"[{c['nome']}]({c['url']})" if c.get("url") else c["nome"]
        linhas.append(f"| {nome} | {c['codigo']} | {celula(c['quando'])} | {celula(c['nota'])} |")
    return "\n".join(linhas) + "\n"


# ---------- PROGRESSO.md ----------
def gerar_progresso(plano, prog, r, texto_quando):
    concl = prog["etapas_concluidas"]
    nomes = {e["id"]: (f, e) for f in plano["fases"] + niveis_ingles(plano) for e in f["etapas"]}
    linhas = ["# Diário de estudos", "",
              f"Atualizado em {texto_quando}. Meta semanal: {prog['meta_semanal_h']} h. "
              f"Total registrado: {horas(r['horas_total'])}.", "", "## Horas por semana", ""]
    semanas = sorted(r["por_semana"])
    if semanas:
        primeira = min(semanas[0], r["semana"])
        linhas += ["| Semana | Horas | Da meta |", "|---|---|---|"]
        s = r["semana"]
        while s >= primeira:
            h = r["por_semana"].get(s, 0.0)
            fim = s + timedelta(days=6)
            pct = h / prog["meta_semanal_h"]
            linhas.append(f"| {dia_mes(s)} a {dia_mes(fim)}/{fim.year} | {horas(h)} | `{barra(pct, 10)}` {round(min(pct, 9.99) * 100)}% |")
            s -= timedelta(days=7)
    else:
        linhas.append("Nenhuma sessão registrada ainda.")
    linhas += ["", "## Etapas concluídas", ""]
    if concl:
        linhas += ["| Data | Etapa | Fase |", "|---|---|---|"]
        for sid, dia in sorted(concl.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
            f, e = nomes[sid]
            linhas.append(f"| {data_br(dia)} | {e['rotulo']} · {celula(e['titulo'])} | {f['numero']} |")
    else:
        linhas.append("Nenhuma etapa concluída ainda.")
    linhas += ["", "## Sessões de estudo", ""]
    if prog["sessoes"]:
        linhas += ["| Data | Horas | O que estudei |", "|---|---|---|"]
        for s in reversed(prog["sessoes"]):
            linhas.append(f"| {data_br(s['data'])} | {horas(s['horas'])} | {celula(s['nota']) or '—'} |")
    else:
        linhas.append("Nenhuma sessão registrada ainda.")
    return "\n".join(linhas) + "\n"


def sem_data(texto):
    """Tira a data da atualização, para comparar só o conteúdo."""
    texto = re.sub(r"Atualizado em(:\*\*)? \d{2}/\d{2}/\d{4} às \d{2}h\d{2}", "Atualizado em —", texto)
    return re.sub(r'"atualizado_em": "[^"]*"', '"atualizado_em": ""', texto)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", help="pasta com a exportação da página (progress/, log/, settings/, accounts/)")
    ap.add_argument("--agora", help="data e hora da atualização em ISO 8601 (padrão: agora, horário de Brasília)")
    ap.add_argument("--forcar", action="store_true", help="grava os arquivos mesmo sem mudança de conteúdo")
    args = ap.parse_args()

    plano = ler_json(DADOS / "plano.json")
    if not plano:
        raise SystemExit("dados/plano.json não encontrado ou inválido")
    agora = datetime.fromisoformat(args.agora).astimezone(FUSO) if args.agora else datetime.now(FUSO)
    if args.db:
        prog = montar_progresso(args.db, plano, agora)
    else:
        prog = ler_json(DADOS / "progresso.json")
        if not prog:
            raise SystemExit("dados/progresso.json não encontrado: rode com --db PASTA")

    texto_quando, hoje = quando(prog)
    r = resumo(plano, prog, hoje)
    readme = (RAIZ / "README.md").read_text(encoding="utf-8")
    readme = trocar_bloco(readme, "PROGRESSO", bloco_progresso(plano, prog, r, hoje, texto_quando))
    readme = trocar_bloco(readme, "PROJETOS", bloco_projetos(plano, prog, hoje))
    readme = trocar_bloco(readme, "PERFIS", bloco_perfis(prog))
    saidas = {
        DADOS / "progresso.json": json.dumps(prog, ensure_ascii=False, indent=2) + "\n",
        RAIZ / "README.md": readme,
        RAIZ / "PLANO.md": gerar_plano(plano, prog, hoje),
        RAIZ / "PROGRESSO.md": gerar_progresso(plano, prog, r, texto_quando),
    }
    mudou = any(not caminho.exists() or sem_data(caminho.read_text(encoding="utf-8")) != sem_data(texto)
                for caminho, texto in saidas.items())
    resumo_txt = f"{r['feitas']}/{r['total']} etapas · {horas(r['horas_total'])} · {horas(r['nesta_semana'])} nesta semana"
    if not mudou and not args.forcar:
        print("Sem mudanças: " + resumo_txt)
        return
    for caminho, texto in saidas.items():
        gravar(caminho, texto)
    print("Atualizado: " + resumo_txt)


if __name__ == "__main__":
    main()
