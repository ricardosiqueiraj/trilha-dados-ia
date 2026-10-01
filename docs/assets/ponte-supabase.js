/* Ponte entre a página da trilha e o Supabase.
 * A página foi escrita para um armazenamento com a interface claude.use("db") / claude.use("user").
 * Este arquivo oferece a mesma interface, guardando tudo na tabela public.docs do Supabase,
 * e cuida do login (GitHub ou link por e-mail). */
(function () {
  "use strict";
  var cfg = window.TRILHA_CONFIG || {};
  var sb = null, uid = null, sessao = null, carregado = false, canal = null;
  var cache = new Map();          // "colecao/id" -> dados
  var ouvintes = new Set();

  function cliente() {
    if (!sb && window.supabase && /^https:\/\//.test(cfg.supabaseUrl || "") && cfg.supabaseKey && !/COLE_AQUI/.test(cfg.supabaseKey)) {
      sb = window.supabase.createClient(cfg.supabaseUrl, cfg.supabaseKey);
    }
    return sb;
  }
  function erro(e) {
    var x = new Error((e && e.message) || "erro");
    var msg = String((e && e.message) || "");
    x.code = (e && e.code === "42501") || /permission|policy|JWT/i.test(msg) ? "not_granted" : "unavailable";
    return x;
  }
  function copia(v) { return v === undefined ? undefined : JSON.parse(JSON.stringify(v)); }
  function avisar() { ouvintes.forEach(function (o) { try { o.disparar(); } catch (e) {} }); }

  function fotoDoc(col, id) {
    var d = cache.get(col + "/" + id);
    return { id: id, exists: d !== undefined, data: function () { return copia(d); } };
  }
  function fotoColecao(col, q) {
    var docs = [];
    cache.forEach(function (v, k) {
      var i = k.indexOf("/");
      if (k.slice(0, i) === col) docs.push(fotoDoc(col, k.slice(i + 1)));
    });
    if (q.orderBy) {
      var campo = q.orderBy[0], desc = q.orderBy[1] === "desc";
      docs.sort(function (a, b) {
        var x = (a.data() || {})[campo], y = (b.data() || {})[campo];
        return (x < y ? -1 : x > y ? 1 : 0) * (desc ? -1 : 1);
      });
    }
    if (q.limit) docs = docs.slice(0, q.limit);
    return { docs: docs, size: docs.length, empty: !docs.length };
  }

  function carregarTudo() {
    return cliente().from("docs").select("collection,id,data").then(function (r) {
      if (r.error) throw erro(r.error);
      cache.clear();
      (r.data || []).forEach(function (l) { cache.set(l.collection + "/" + l.id, l.data); });
      carregado = true;
    });
  }
  function gravar(col, id, dados) {
    return cliente().from("docs")
      .upsert({ owner: uid, collection: col, id: id, data: dados, updated_at: new Date().toISOString() }, { onConflict: "owner,collection,id" })
      .then(function (r) { if (r.error) throw erro(r.error); cache.set(col + "/" + id, copia(dados)); avisar(); });
  }
  function apagar(col, id) {
    return cliente().from("docs").delete().match({ owner: uid, collection: col, id: id })
      .then(function (r) { if (r.error) throw erro(r.error); cache.delete(col + "/" + id); avisar(); });
  }
  function refDoc(col, id) {
    return {
      id: id,
      set: function (d) { return gravar(col, id, d); },
      delete: function () { return apagar(col, id); },
      onSnapshot: function (prox) {
        var o = { disparar: function () { prox(fotoDoc(col, id)); } };
        ouvintes.add(o); setTimeout(o.disparar, 0);
        return function () { ouvintes.delete(o); };
      }
    };
  }
  function consulta(col, q) {
    return {
      orderBy: function (f, dir) { return consulta(col, Object.assign({}, q, { orderBy: [f, dir || "asc"] })); },
      limit: function (n) { return consulta(col, Object.assign({}, q, { limit: n })); },
      onSnapshot: function (prox) {
        var o = { disparar: function () { prox(fotoColecao(col, q)); } };
        ouvintes.add(o); setTimeout(o.disparar, 0);
        return function () { ouvintes.delete(o); };
      }
    };
  }
  function novoId() { return "a" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }
  var db = Object.freeze({
    collection: function (col) { return Object.assign(consulta(col, {}), { doc: function (id) { return refDoc(col, id || novoId()); } }); },
    doc: function (caminho) { var i = caminho.indexOf("/"); return refDoc(caminho.slice(0, i), caminho.slice(i + 1)); }
  });

  function tempoReal() {
    var c = cliente();
    if (canal || !c.channel) return;
    canal = c.channel("docs-" + uid)
      .on("postgres_changes", { event: "*", schema: "public", table: "docs", filter: "owner=eq." + uid }, function (p) {
        if (p.eventType === "DELETE") { if (p.old) cache.delete(p.old.collection + "/" + p.old.id); }
        else if (p.new) cache.set(p.new.collection + "/" + p.new.id, p.new.data);
        avisar();
      })
      .subscribe();
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "visible") carregarTudo().then(avisar).catch(function () {});
    });
  }

  // Na primeira entrada, oferece trazer o progresso salvo na versão anterior da trilha.
  function talvezImportar() {
    if (cache.size > 0 || !cfg.dadosIniciais) return Promise.resolve();
    return fetch(cfg.dadosIniciais, { cache: "no-store" }).then(function (r) { return r.ok ? r.json() : null; }).then(function (snap) {
      if (!snap || !Array.isArray(snap.linhas) || !snap.linhas.length) return;
      var ok = true;
      try { ok = window.confirm("Encontrei o progresso que você já tinha marcado (" + snap.resumo + "). Quer trazer para esta conta?"); } catch (e) {}
      if (!ok) return;
      var linhas = snap.linhas.map(function (l) { return { owner: uid, collection: l.collection, id: l.id, data: l.data, updated_at: new Date().toISOString() }; });
      return cliente().from("docs").upsert(linhas, { onConflict: "owner,collection,id" }).then(function (r) {
        if (r.error) throw erro(r.error);
        linhas.forEach(function (l) { cache.set(l.collection + "/" + l.id, l.data); });
      });
    }).catch(function () {});
  }

  function iniciais(nome) {
    var p = String(nome || "?").trim().split(/\s+/);
    var t = ((p[0] || "?")[0] + (p.length > 1 ? p[p.length - 1][0] : "")).toUpperCase();
    return "data:image/svg+xml," + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64"><rect width="64" height="64" rx="32" fill="#0A3BD8"/><text x="32" y="41" font-family="Arial" font-size="24" fill="#fff" text-anchor="middle">' + t.replace(/[<&>"]/g, "") + "</text></svg>");
  }
  function eu() {
    var u = sessao && sessao.user;
    if (!u) return { id: null, name: "", avatarUrl: iniciais("?"), color: "#0A3BD8", email: null, isOwner: false, canEdit: false };
    var m = u.user_metadata || {};
    var nome = m.full_name || m.name || m.user_name || (u.email || "").split("@")[0] || "";
    return { id: u.id, name: nome, avatarUrl: m.avatar_url || iniciais(nome), color: "#0A3BD8", email: u.email || null, isOwner: true, canEdit: true };
  }

  function obterSessao() {
    var c = cliente();
    if (!c) return Promise.resolve(null);
    return c.auth.getSession().then(function (r) { sessao = r && r.data ? r.data.session : null; return sessao; }).catch(function () { return null; });
  }

  window.claude = {
    use: function (nome) {
      if (nome === "db") {
        return obterSessao().then(function (s) {
          if (!s) return null;
          uid = s.user.id;
          if (carregado) return db;
          return carregarTudo().then(talvezImportar).then(function () { tempoReal(); return db; });
        });
      }
      if (nome === "user") {
        return obterSessao().then(function () {
          return Object.freeze({
            me: function () { return Promise.resolve(eu()); },
            id: function () { return Promise.resolve(uid); },
            isOwner: function () { return Promise.resolve(!!sessao); },
            canEdit: function () { return Promise.resolve(!!sessao); },
            can: function () { return Promise.resolve(!!sessao); }
          });
        });
      }
      return Promise.resolve(null);
    }
  };

  // Botões da tela de entrada e de saída.
  function msg(t, tipo) { var m = document.getElementById("login-msg"); if (m) { m.textContent = t; m.setAttribute("data-kind", tipo || ""); } }
  function destino() { return location.origin + location.pathname; }
  document.addEventListener("DOMContentLoaded", ligarBotoes);
  if (document.readyState !== "loading") ligarBotoes();
  var ligado = false;
  function ligarBotoes() {
    if (ligado) return; ligado = true;
    var gh = document.getElementById("login-github");
    var form = document.getElementById("login-email");
    var sair = document.getElementById("logout");
    if (gh) gh.addEventListener("click", function () {
      var c = cliente(); if (!c) return msg("O site ainda não foi ligado ao banco. Confira o arquivo config.js.", "error");
      msg("Abrindo o GitHub…");
      fetch(cfg.supabaseUrl + "/auth/v1/settings", { headers: { apikey: cfg.supabaseKey } })
        .then(function (r) { return r.json(); })
        .then(function (s) { return !!(s && s.external && s.external.github); }, function () { return true; })
        .then(function (ativo) {
          if (!ativo) return msg("O login com GitHub ainda não foi ativado no Supabase. Por enquanto, entre pelo link no e-mail.", "error");
          return c.auth.signInWithOAuth({ provider: "github", options: { redirectTo: destino() } }).then(function (r) {
        if (r && r.error) msg(/not enabled|provider/i.test(r.error.message) ? "O login com GitHub ainda não foi ativado no Supabase. Use o e-mail por enquanto." : "Não deu para entrar com o GitHub: " + r.error.message, "error");
      });
        });
    });
    if (form) form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var c = cliente(); if (!c) return msg("O site ainda não foi ligado ao banco. Confira o arquivo config.js.", "error");
      var email = (document.getElementById("login-email-input") || {}).value || "";
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return msg("Digite um e-mail válido.", "error");
      msg("Enviando…");
      c.auth.signInWithOtp({ email: email, options: { emailRedirectTo: destino() } }).then(function (r) {
        if (r && r.error) msg("Não deu para enviar o link: " + r.error.message, "error");
        else msg("Pronto! Abra o e-mail que enviamos e toque no link para entrar.", "ok");
      });
    });
    [sair, document.getElementById("logout2")].forEach(function (bt) {
      if (bt) bt.addEventListener("click", function () {
        var c = cliente(); if (!c) return;
        c.auth.signOut().then(function () { location.reload(); });
      });
    });
    var c = cliente();
    if (c) c.auth.onAuthStateChange(function (evento) {
      if (evento === "SIGNED_IN" && !uid) { var b = document.getElementById("gate-retry"); if (b) b.click(); }
    });
  }
})();
