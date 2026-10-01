#!/usr/bin/env python3
"""Liga a atualização semanal do GitHub ao banco do site (Supabase).

Uso:
  python3 scripts/supabase_sync.py exportar PASTA
      Lê a tabela public.docs e grava um arquivo por documento em PASTA/<coleção>/<id>.json,
      no mesmo formato que o scripts/atualizar.py espera em --db.
  python3 scripts/supabase_sync.py marcar --resumo "..." [--commit HASH]
      Grava em sync/github a data desta atualização, para o Painel do site mostrar.

Variáveis de ambiente:
  SUPABASE_URL          endereço do projeto (https://xxxx.supabase.co)
  SUPABASE_SECRET_KEY   chave secreta do projeto (sb_secret_... ou a service_role antiga).
                        Fica só nos segredos do GitHub; nunca no código.
  SUPABASE_OWNER_ID     opcional: id do dono da trilha. Sem ela, o script exige que a tabela
                        tenha um único dono.
  GITHUB_REPOSITORY     preenchida pelo GitHub Actions (dono/repositório).

Só usa a biblioteca padrão do Python 3.9+.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

COLECOES = ("progress", "log", "settings", "accounts", "scores", "sync")
ID_OK = re.compile(r"^[A-Za-z0-9_.-]{1,200}$")
FUSO = timezone(timedelta(hours=-3))


def config():
    url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    chave = os.environ.get("SUPABASE_SECRET_KEY", "").strip()
    if not re.match(r"^https://[a-z0-9-]+\.supabase\.co$", url):
        raise SystemExit("SUPABASE_URL ausente ou inválida")
    if not chave:
        raise SystemExit("SUPABASE_SECRET_KEY ausente: crie o segredo no GitHub (Settings > Secrets and variables > Actions)")
    return url, chave


def cabecalhos(chave, extra=None):
    h = {"apikey": chave, "Accept": "application/json", "Content-Type": "application/json"}
    if chave.count(".") == 2:  # chave antiga em formato JWT (service_role)
        h["Authorization"] = "Bearer " + chave
    h.update(extra or {})
    return h


def pedir(metodo, url, chave, corpo=None, extra=None):
    dados = json.dumps(corpo).encode() if corpo is not None else None
    req = urllib.request.Request(url, data=dados, method=metodo, headers=cabecalhos(chave, extra))
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            txt = r.read().decode()
            return json.loads(txt) if txt else None
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="replace")[:300]
        raise SystemExit(f"Supabase respondeu {e.code} em {metodo} {url.split('?')[0]}: {msg}")


def dono(linhas):
    fixo = os.environ.get("SUPABASE_OWNER_ID", "").strip()
    if fixo:
        return fixo
    donos = sorted({l["owner"] for l in linhas})
    if len(donos) > 1:
        raise SystemExit("Há mais de uma conta com dados no banco. Defina o segredo SUPABASE_OWNER_ID com o id do dono da trilha.")
    return donos[0] if donos else None


def ler_tudo(url, chave):
    linhas, inicio, passo = [], 0, 1000
    while True:
        q = urllib.parse.urlencode({"select": "owner,collection,id,data", "order": "collection.asc,id.asc"})
        lote = pedir("GET", f"{url}/rest/v1/docs?{q}", chave, extra={"Range-Unit": "items", "Range": f"{inicio}-{inicio + passo - 1}"})
        lote = lote or []
        linhas += lote
        if len(lote) < passo:
            return linhas
        inicio += passo


def exportar(pasta):
    url, chave = config()
    linhas = ler_tudo(url, chave)
    quem = dono(linhas)
    pasta = Path(pasta)
    for c in COLECOES:
        (pasta / c).mkdir(parents=True, exist_ok=True)
    n = 0
    for l in linhas:
        if l.get("owner") != quem or l.get("collection") not in COLECOES or not ID_OK.match(str(l.get("id", ""))):
            continue
        if not isinstance(l.get("data"), dict):
            continue
        (pasta / l["collection"] / f"{l['id']}.json").write_text(json.dumps(l["data"], ensure_ascii=False), encoding="utf-8")
        n += 1
    (pasta / ".dono").write_text(quem or "", encoding="utf-8")
    print(f"Exportados {n} documentos do Supabase para {pasta}")


def marcar(resumo, commit, pasta):
    url, chave = config()
    quem = (Path(pasta) / ".dono").read_text(encoding="utf-8").strip() if pasta and (Path(pasta) / ".dono").exists() else ""
    if not quem:
        quem = dono(ler_tudo(url, chave))
    if not quem:
        print("Banco ainda sem dados: nada para marcar")
        return
    repo = os.environ.get("GITHUB_REPOSITORY", "ricardosiqueiraj/trilha-dados-ia")
    agora = datetime.now(FUSO).isoformat(timespec="seconds")
    dados = {"repo": repo, "updatedAt": agora, "summary": resumo[:200]}
    if commit and re.match(r"^[0-9a-f]{40}$", commit):
        dados["commitUrl"] = f"https://github.com/{repo}/commit/{commit}"
    linha = {"owner": quem, "collection": "sync", "id": "github", "data": dados, "updated_at": agora}
    pedir("POST", f"{url}/rest/v1/docs?on_conflict=owner,collection,id", chave, [linha],
          extra={"Prefer": "resolution=merge-duplicates,return=minimal"})
    print(f"Painel do site marcado: {agora}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("exportar")
    e.add_argument("pasta")
    m = sub.add_parser("marcar")
    m.add_argument("--resumo", default="")
    m.add_argument("--commit", default="")
    m.add_argument("--pasta", default="")
    a = ap.parse_args()
    if a.cmd == "exportar":
        exportar(a.pasta)
    else:
        marcar(a.resumo, a.commit, a.pasta)


if __name__ == "__main__":
    sys.exit(main())
