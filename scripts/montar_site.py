#!/usr/bin/env python3
"""Monta o site (docs/index.html) a partir da página fonte (fonte/trilha.html).

A página fonte é a mesma usada no Claude. Aqui ela ganha:
- o esqueleto HTML completo (idioma, meta tags, ícone);
- o cliente do Supabase, o config.js e a ponte que guarda os dados no banco;
- uma tela de entrada com GitHub e link por e-mail, e um botão de sair.

Uso: python3 scripts/montar_site.py
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "fonte" / "trilha.html"
SAIDA = RAIZ / "docs" / "index.html"

ICONE = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
         "%3Crect width='64' height='64' rx='14' fill='%230A3BD8'/%3E"
         "%3Cg fill='none' stroke='%23fff' stroke-width='4'%3E%3Ccircle cx='18' cy='32' r='7'/%3E"
         "%3Ccircle cx='46' cy='18' r='7'/%3E%3Ccircle cx='46' cy='46' r='7'/%3E"
         "%3Cpath d='M24 29l16-8M24 35l16 8'/%3E%3C/g%3E%3C/svg%3E")

CABECA = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Trilha de estudos de José Ricardo para Engenharia de Dados e IA: 39 etapas, 6 fases e cursos gratuitos.">
<meta name="theme-color" content="#031626">
<link rel="icon" href="{ICONE}">
<link rel="apple-touch-icon" href="{ICONE}">
<style>[hidden]{{display:none!important}}img{{max-width:100%}}</style>
"""

ENTRADA = """      <h1 id="gate-title">Entre para acessar sua trilha</h1>
      <p id="gate-msg">Seu progresso, suas horas e suas contas ficam salvos na sua conta e aparecem no celular e no computador.</p>
      <button class="gate-btn primary" type="button" id="login-github"><i data-icon="git"></i>Entrar com GitHub</button>
      <div class="gate-or"><span>ou receba um link por e-mail</span></div>
      <form class="gate-form" id="login-email" novalidate>
        <label class="sr-only" for="login-email-input">Seu e-mail</label>
        <input class="inp" id="login-email-input" type="email" autocomplete="email" inputmode="email" placeholder="seu@email.com" required>
        <button class="gate-btn" type="submit"><i data-icon="right"></i>Receber link de acesso</button>
      </form>
      <p class="gate-note" id="login-msg" role="status"></p>
      <button class="gate-btn" type="button" id="gate-skip"><i data-icon="right"></i>Só olhar, sem salvar</button>
      <a id="gate-login" href="#" hidden></a><button type="button" id="gate-retry" hidden></button>
      <p class="gate-note">Sem senha para decorar: entre com o GitHub ou com o link que chega no seu e-mail.</p>
"""

ESTILO_EXTRA = """
.gate-or{display:flex;align-items:center;gap:10px;color:var(--dim);font-size:.78rem}
.gate-or::before,.gate-or::after{content:"";flex:1;height:1px;background:var(--line)}
.gate-form{display:grid;gap:10px}
#login-msg[data-kind="error"]{color:var(--warn)!important}
#login-msg[data-kind="ok"]{color:var(--green)!important}
.logout-btn{width:40px;height:40px;border-radius:50%;border:1px solid var(--line-2);background:var(--surface);color:var(--text);display:grid;place-items:center;cursor:pointer;transition:border-color .18s ease,color .18s ease,transform .18s ease}
.logout-btn:hover{border-color:var(--warn);color:var(--warn);transform:translateY(-2px)}
@media (max-width:520px){#logout{display:none}}
.logout-row{display:flex;justify-content:flex-end}
"""

def versao(arquivo):
    """Código curto do conteúdo do arquivo, para o navegador não usar uma cópia antiga."""
    import hashlib
    return hashlib.sha1((RAIZ / "docs" / arquivo).read_bytes()).hexdigest()[:8]


def scripts():
    return ('<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js"></script>\n'
            f'<script src="config.js?v={versao("config.js")}"></script>\n'
            f'<script src="assets/ponte-supabase.js?v={versao("assets/ponte-supabase.js")}"></script>\n')


def main():
    html = FONTE.read_text(encoding="utf-8")
    # tela de entrada própria do site
    html, n = re.subn(r"<!-- GATE:INICIO -->.*?<!-- GATE:FIM -->", "<!-- GATE:INICIO -->\n" + ENTRADA + "      <!-- GATE:FIM -->", html, flags=re.S)
    assert n == 1, "marcadores GATE não encontrados"
    # botão de sair ao lado do usuário
    alvo = '<button class="me" type="button" data-nav="inicio"'
    assert alvo in html
    html = html.replace(alvo, '<button class="logout-btn" type="button" id="logout" aria-label="Sair da conta" title="Sair da conta"><i data-icon="left"></i></button>\n      ' + alvo, 1)
    # botão de sair também no fim da aba Contas (no celular o do topo some)
    fim_contas = '<div class="tools" id="tools"></div>'
    assert fim_contas in html
    html = html.replace(fim_contas, fim_contas + '\n      <div class="logout-row"><button class="btn-outline" type="button" id="logout2">Sair da conta</button></div>', 1)
    # ícones novos usados acima e estilos extras
    html = html.replace("</style>", ESTILO_EXTRA + "</style>", 1)
    # textos que falavam do Claude
    html = html.replace("Abra a página pelo Claude, com sua conta, para salvar.", "Entre com sua conta para salvar.")
    # no site, quem atualiza o GitHub é o GitHub Actions, lendo o banco do Supabase
    for velho, novo in [
        ("Depois de ligado, o Claude atualiza toda semana o repositório trilha-dados-ia com o que você marca nesta página:",
         "Todo domingo à noite, uma automação do próprio GitHub (GitHub Actions) lê o que você marca neste site e atualiza o repositório trilha-dados-ia:"),
        ("<strong>Conecte o GitHub ao Claude</strong><span class=\"s\">No claude.ai, abra Configurações, depois Conectores, conecte sua conta do GitHub e libere o acesso ao repositório trilha-dados-ia.</span>",
         "<strong>Guarde a chave secreta do Supabase no GitHub</strong><span class=\"s\">No repositório, Settings, Secrets and variables, Actions: crie o segredo SUPABASE_SECRET_KEY. É ele que deixa a automação ler o seu progresso.</span>"),
        ("<strong>Avise o Claude no chat</strong><span class=\"s\">Ele envia o plano para o repositório e liga a atualização de toda semana. Quando ela rodar, a data aparece aqui em cima.</span>",
         "<strong>Rode a automação uma vez</strong><span class=\"s\">Na aba Actions do repositório, abra Atualizar progresso e clique em Run workflow. Depois ela roda sozinha todo domingo, e a data aparece aqui em cima.</span>"),
        ("Passos 1 e 2 feitos. Falta avisar o Claude no chat para ligar a atualização automática.",
         "Passos 1 e 2 feitos. Falta rodar a automação uma vez na aba Actions do GitHub."),
    ]:
        assert velho in html, velho[:50]
        html = html.replace(velho, novo)
    # scripts do site antes do script principal
    pos = html.rfind("<script>")
    assert pos > 0
    html = html[:pos] + scripts() + html[pos:]
    titulo_fim = html.index("</title>") + len("</title>")
    titulo = html[:titulo_fim]
    resto = html[titulo_fim:]
    pagina = CABECA + titulo + "\n" + resto.split("<style>", 1)[0] + "<style>" + resto.split("<style>", 1)[1].split("</style>", 1)[0] + "</style>\n</head>\n<body>\n" + resto.split("</style>", 1)[1] + "\n</body>\n</html>\n"
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(pagina, encoding="utf-8")
    print(f"site montado em {SAIDA.relative_to(RAIZ)} ({len(pagina) // 1024} KB)")


if __name__ == "__main__":
    main()
