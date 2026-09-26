"""Elementos visuais sem lógica de navegação ou alterações de dados."""
from base64 import b64encode
from functools import lru_cache
from html import escape

import streamlit as st

from data_access import ROOT, as_bool


@lru_cache
def asset(name):
    path = ROOT / "identidade visual" / name
    return "data:image/png;base64," + b64encode(path.read_bytes()).decode()


def html(markup):
    st.markdown(markup, unsafe_allow_html=True)


def style(large=False, contrast=False):
    css = (ROOT / "app" / "src" / "style.css").read_text(encoding="utf-8")
    html(f"<style>{css}</style>")
    size = "19px" if large else "17px"
    html(f"<style>html {{ font-size: {size}; }} .stApp {{ --reading-size: {size}; }}</style>")
    if contrast:
        html("""<style>
        .stApp { --paper:#fff; --ink:#111; --muted:#303030; --border:#575757; }
        .stApp [data-testid="stAppViewContainer"] {background:#fff;}
        .stApp [data-baseweb="select"]>div, .stApp [data-baseweb="input"] {background:#fff;border-color:#575757;}
        .stApp .note, .stApp .resource, .stApp .step {border-color:#575757;}
        .stApp button:focus-visible, .stApp input:focus-visible {outline:3px solid #111!important;}
        </style>""")


def brand_header(logged_in=False):
    html(f"""<header class="brandbar">
      <img class="brand-logo" src="{asset('embarque-inclusivo-logo-horizontal.png')}" alt="Embarque Inclusivo">
      <div class="brand-meta"><span class="line-tag">7 · RUBI</span>
      <span class="demo-tag">Protótipo · simulação</span></div>
    </header>""")


def heading(eyebrow, title, subtitle=""):
    html(f"<div class='page-heading'><p class='eyebrow'>{escape(eyebrow)}</p>"
         f"<h1>{escape(title)}</h1><p class='muted'>{escape(subtitle)}</p></div>")


def section_label(text, eyebrow=""):
    html(f"<div class='section-title'><span class='eyebrow'>{escape(eyebrow)}</span>"
         f"<h2>{escape(text)}</h2></div>")


def note(title, text, tone="info"):
    icon = {"info": "i", "warning": "!", "error": "!", "success": "✓"}.get(tone, "i")
    html(f"<aside class='note note-{tone}'><span class='note-icon' aria-hidden='true'>{icon}</span>"
         f"<div><h3>{escape(title)}</h3><p>{escape(text)}</p></div></aside>")


def persona(user, subtitle):
    name = user["nome"]
    initials = "".join(part[0] for part in name.split()[:2])
    html(f"<div class='person'><div class='avatar' aria-hidden='true'>{escape(initials)}</div>"
         f"<div><h3>{escape(name)}</h3><p>{escape(subtitle)}</p></div></div>")


def landing_story():
    html("""<section class="welcome-story">
      <span class="story-tag">MOBILIDADE QUE CONECTA PESSOAS</span>
      <h1>Seu caminho,<br>com mais confiança.</h1>
      <p>Planeje sua viagem, conheça as estações e encontre o apoio de que você precisa.</p>
      <ol class="story-stops">
        <li><span>ANTES DE SAIR</span><strong>Uma viagem pensada para você</strong></li>
        <li><span>NO PERCURSO</span><strong>Informação que faz diferença</strong></li>
        <li><span>NA ESTAÇÃO</span><strong>Mais clareza para pedir apoio</strong></li>
      </ol>
      <div class="story-footer"><span>LINHA 7–RUBI</span><span>Jundiaí ↔ Barra Funda</span></div>
    </section>""")


def trip_ticket(origin, destination, scenario, count):
    status = "Sem operação" if scenario["closed"] else "Atenção na linha" if scenario["incident"] else "Operação normal"
    if scenario["status_operacao"] == "operacao_inicial":
        status = "Início da operação"
    movement = {"baixo": "Baixo", "moderado": "Moderado", "alto": "Alto", "sem_servico": "Sem serviço"}[scenario["movimento"]]
    html(f"""<section class="journey-ticket">
      <div class="ticket-top"><span class="ticket-line">7 · Linha Rubi</span><span class="ticket-status">{escape(status)} · simulado</span></div>
      <div class="ticket-route"><div><small>EMBARQUE</small><h2>{escape(origin)}</h2></div>
      <span class="route-connector" aria-hidden="true">↓</span>
      <div><small>DESEMBARQUE</small><h2>{escape(destination)}</h2></div></div>
      <dl class="ticket-stats"><div><dt>Horário simulado</dt><dd>{escape(scenario['horario'])}</dd></div>
      <div><dt>No percurso</dt><dd>{count} estações</dd></div>
      <div><dt>Movimento</dt><dd>{movement}</dd></div></dl>
    </section>""")


def route_map(stations, affected=(), current=()):
    bad = {s["estacao_id"] for s in affected}
    selected = {s["estacao_id"] for s in current}
    rows = []
    for index, station in enumerate(stations):
        sid = station["estacao_id"]
        if current:
            label = ("Sua origem" if sid == current[0]["estacao_id"] else
                     "Seu destino" if sid == current[-1]["estacao_id"] else
                     "No seu percurso" if sid in selected else "")
        else:
            label = "Origem" if index == 0 else "Destino" if index == len(stations)-1 else ""
        if sid in bad:
            label = f"{label} · Ocorrência simulada" if label else "Ocorrência simulada"
        cls = "route-alert" if sid in bad else "route-selected" if sid in selected else ""
        rows.append(f"<li class='{cls}'><span class='station-dot' aria-hidden='true'></span>"
                    f"<div><strong>{escape(station['nome_estacao'])}</strong>"
                    f"<small>{escape(label)}</small></div></li>")
    html("<ol class='line-map' aria-label='Estações na ordem do percurso'>" + "".join(rows) + "</ol>")


def resource_grid(station):
    resources = station["recursos"]
    toilet = any(as_bool(resources.get(k)) for k in (
        "banheiro_acessivel_feminino", "banheiro_acessivel_masculino", "banheiro_acessivel_unissex"))
    features = [("Rampa", as_bool(resources.get("rampa"))),
                ("Piso tátil", as_bool(resources.get("piso_tatil"))),
                ("Elevador", as_bool(resources.get("elevador"))),
                ("Banheiro acessível", toilet),
                ("Transposição de plataformas", as_bool(resources.get("transposicao_de_plataformas"))),
                ("Escada rolante", as_bool(resources.get("escada_rolante")))]
    rows = []
    for label, published in features:
        state = "Publicado no cadastro" if published else "Não informado no cadastro"
        icon = "✓" if published else "?"
        cls = "resource-published" if published else "resource-unknown"
        rows.append(f"<div class='resource {cls}'><span aria-hidden='true'>{icon}</span>"
                    f"<div><strong>{escape(label)}</strong><small>{state}</small></div></div>")
    html("<div class='resource-grid'>" + "".join(rows) + "</div>")


def support_steps(status):
    progress = {"pendente": 1, "confirmado": 2, "concluido": 3, "cancelado": 0}.get(status, 0)
    steps = []
    for idx, label in enumerate(("Pedido enviado", "Equipe designada", "Atendimento concluído"), 1):
        cls = "step-done" if idx <= progress else ""
        steps.append(f"<li class='step {cls}'><span aria-hidden='true'>{'✓' if idx <= progress else idx}</span>"
                     f"<strong>{label}</strong></li>")
    html("<ol class='support-steps' aria-label='Etapas da assistência simulada'>" + "".join(steps) + "</ol>")


def footer():
    html("<footer class='app-footer'>Embarque Inclusivo · Linha 7–Rubi<br>"
         "Cadastro de estações + cenários fictícios. Nenhum pedido é enviado à operadora.</footer>")
