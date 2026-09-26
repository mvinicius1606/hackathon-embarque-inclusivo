"""Embarque Inclusivo: experiência de passageiro com operação e apoio simulados.

Executar na raiz: python -m streamlit run app/src/streamlit_app.py
"""
from copy import deepcopy
from datetime import time
from pathlib import Path
import sys

# Também funciona quando o arquivo é executado pelo AppTest do Streamlit.
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import streamlit as st

from data_access import ROOT, load_data, user_routines, normalize
from journey import (SCENARIOS, SUPPORT_OPTIONS, route_stations, scenario_for,
                     affected_on_route, route_insights, preferred_support,
                     create_request, transition_request)
import ui


@st.cache_data
def get_data():
    return load_data()


def station_name(data, station_id):
    return next(s["nome_estacao"] for s in data["stations"] if s["estacao_id"] == station_id)


def current_routines(data):
    routines = user_routines(data, st.session_state["user"]["usuario_id"])
    custom = st.session_state.get("session_routine")
    return routines + ([custom] if custom else [])


def invalidate_request(message=None):
    if st.session_state.get("request"):
        st.session_state["notice"] = "A viagem ou as preferências mudaram. O pedido anterior foi encerrado nesta simulação; solicite apoio novamente."
    elif message:
        st.session_state["notice"] = message
    st.session_state["request"] = None
    st.session_state.pop("support_error", None)


def start_user(user, data):
    preferences = {k: st.session_state.get(k, False) for k in ("large_text", "high_contrast")}
    st.session_state.clear()
    st.session_state.update(preferences)
    routines = user_routines(data, user["usuario_id"])
    trip = deepcopy(routines[0]["legs"]["ida"]) if routines else {
        "origin": data["stations"][0]["estacao_id"],
        "destination": data["stations"][2]["estacao_id"], "departure": "10:00",
        "name": "Viagem avulsa", "direction": "ida", "routine_id": None,
    }
    st.session_state.update(user=deepcopy(user), initial_user=deepcopy(user), trip=trip, page="Viagem",
                            scenario_mode="horario", manual_hour=int(trip["departure"][:2]),
                            request=None, request_sequence=0, trip_editor=False)


def reset_profile(data):
    original = next((u for u in data["users"] if u["usuario_id"] == st.session_state["user"]["usuario_id"]),
                    st.session_state["initial_user"])
    start_user(original, data)
    st.session_state["notice"] = "Demonstração reiniciada para este perfil."


def logout():
    visual = {k: st.session_state.get(k, False) for k in ("large_text", "high_contrast")}
    st.session_state.clear()
    st.session_state.update(visual)


def go(page):
    st.session_state["page"] = page


def apply_trip(trip):
    invalidate_request("Viagem atualizada.")
    st.session_state["trip"] = deepcopy(trip)
    st.session_state["scenario_mode"] = "horario"
    st.session_state["manual_hour"] = int(trip["departure"][:2])
    st.session_state["trip_editor"] = False
    st.session_state["page"] = "Viagem"


def save_trip(data):
    state = st.session_state
    try:
        route_stations(data["stations"], state["edit_origin"], state["edit_destination"])
    except ValueError as error:
        state["trip_error"] = str(error)
        return
    apply_trip({"origin": state["edit_origin"], "destination": state["edit_destination"],
                "departure": f"{state['edit_hour']:02d}:00", "name": "Viagem avulsa",
                "direction": "ida", "routine_id": None})
    state.pop("trip_error", None)


def choose_routine(data):
    routines = current_routines(data)
    selected = next(r for r in routines if r["rotina_id"] == st.session_state["chosen_routine"])
    direction = "ida" if st.session_state["chosen_direction"] == "Ida" else "volta"
    apply_trip(selected["legs"][direction])


def create_profile(data):
    state = st.session_state
    name = state.get("new_name", "").strip()
    if not name:
        state["signup_error"] = "Digite um nome fictício para continuar."
        return
    support = state.get("new_support", [])
    user = {"usuario_id": "USR-DEMO", "nome": name, "deficiencia_informada": "não informada",
            "usa_cadeira_rodas": False, "preferencia_comunicacao": "app",
            "necessita_percurso_sem_escadas": SUPPORT_OPTIONS[2] in support,
            "prefere_orientacao_embarque": bool(set(SUPPORT_OPTIONS[:2]) & set(support)),
            "solicita_acompanhamento": SUPPORT_OPTIONS[3] in support, "dados_sinteticos": True}
    start_user(user, data)


def save_profile():
    state = st.session_state
    if not state["profile_name"].strip():
        state["profile_error"] = "Informe um nome fictício."
        return
    user = deepcopy(state["user"])
    user.update(nome=state["profile_name"].strip(),
                necessita_percurso_sem_escadas=state["pref_stairs"],
                prefere_orientacao_embarque=state["pref_orientation"],
                solicita_acompanhamento=state["pref_accompany"],
                usa_cadeira_rodas=state["pref_wheelchair"],
                preferencia_comunicacao=state["pref_communication"])
    invalidate_request("Preferências atualizadas nesta sessão.")
    state["user"] = user
    state.pop("profile_error", None)


def save_routine(data):
    state = st.session_state
    try:
        route_stations(data["stations"], state["routine_origin"], state["routine_destination"])
        if not state["routine_days"]:
            raise ValueError("Selecione pelo menos um dia da semana.")
        if state["routine_return"] <= state["routine_departure"]:
            raise ValueError("O retorno deve ser após a saída. Esta demonstração considera ida e volta no mesmo dia.")
    except ValueError as error:
        state["routine_error"] = str(error)
        return
    name = state["routine_purpose"]
    base = {"name": name, "routine_id": "ROT-SESSAO", "arrival": ""}
    outbound = {**base, "origin": state["routine_origin"], "destination": state["routine_destination"],
                "departure": state["routine_departure"].strftime("%H:%M"), "direction": "ida"}
    inbound = {**base, "origin": state["routine_destination"], "destination": state["routine_origin"],
               "departure": state["routine_return"].strftime("%H:%M"), "direction": "volta"}
    state["session_routine"] = {"rotina_id": "ROT-SESSAO", "nome_rotina": name,
                                "days": state["routine_days"], "legs": {"ida": outbound, "volta": inbound}}
    state.pop("routine_error", None)
    apply_trip(outbound)
    state["notice"] = "Rotina salva nesta sessão, com retorno no sentido inverso."


def send_request(data):
    state = st.session_state
    scenario = scenario_for(data["occurrences"], state["scenario_mode"], state.get("manual_hour", 10))
    previous = state.get("request")
    try:
        request = create_request(state["user"], state["trip"], scenario, state["support_types"],
                                 state["request_sequence"] + 1, previous, state.get("support_note", ""))
    except ValueError as error:
        state["support_error"] = str(error)
        return
    if not previous or previous["id"] != request["id"]:
        state["request_sequence"] += 1
    state["request"] = request
    state.pop("support_error", None)


def advance_support(action):
    try:
        st.session_state["request"] = transition_request(st.session_state.get("request"), action)
    except ValueError as error:
        st.session_state["support_error"] = str(error)


def login_screen(data):
    left, right = st.columns([1.08, 1], gap="large")
    with left:
        ui.landing_story()
    with right:
        ui.section_label("Comece por uma pessoa", "EXPLORE A DEMONSTRAÇÃO")
        st.write("Escolha um perfil fictício e veja como o app acompanha diferentes necessidades.")
        subtitles = ["Orientação na estação · deficiência visual", "Percurso sem escadas · usa cadeira de rodas",
                     "Viagens do dia a dia · sem deficiência informada"]
        for index, user in enumerate(data["users"][:3]):
            with st.container(key=f"persona_{index}"):
                ui.persona(user, subtitles[index])
                st.button(f"Viajar com {user['nome'].split()[0]}", key=f"login_{user['usuario_id']}",
                          icon=":material/arrow_forward:", width="stretch",
                          on_click=start_user, args=(user, data))
        with st.expander("Outros perfis de demonstração"):
            profiles = {u["usuario_id"]: u for u in data["users"][3:]}
            selected = st.selectbox("Escolha uma pessoa", list(profiles),
                                    format_func=lambda uid: profiles[uid]["nome"], key="extra_person")
            st.button("Explorar este perfil", on_click=start_user, args=(profiles[selected], data), width="stretch")
        with st.expander("Criar outro perfil fictício"):
            st.caption("Use um nome de teste. Este perfil existe somente durante a sessão.")
            with st.form("signup"):
                st.text_input("Nome fictício", key="new_name", max_chars=60)
                st.multiselect("Qual apoio ajudaria nesta viagem?", SUPPORT_OPTIONS, key="new_support")
                st.form_submit_button("Começar minha simulação", on_click=create_profile, args=(data,),
                                      type="primary", width="stretch")
            if st.session_state.get("signup_error"):
                st.error(st.session_state["signup_error"])


def demo_controls(data, scenario):
    with st.expander(f"Controles da apresentação · {scenario['horario']} · cenário simulado"):
        st.caption("Use estes controles para mostrar como a mesma viagem muda ao longo do dia.")
        st.selectbox("Cenário", list(SCENARIOS), key="scenario_mode",
                     format_func=lambda key: f"{SCENARIOS[key]['label']} · {SCENARIOS[key]['note']}",
                     on_change=invalidate_request)
        if st.session_state["scenario_mode"] == "horario":
            st.session_state.setdefault("manual_hour", 10)
            st.slider("Hora da simulação", 0, 23, key="manual_hour", format="%02dh", on_change=invalidate_request)
        if st.session_state["scenario_mode"] == "ocorrencia":
            st.caption("Cena programada: a restrição de Vila Aurora, Perus e Caieiras é combinada com o pico das 7h.")
        c1, c2 = st.columns(2)
        c1.button("Reiniciar este perfil", icon=":material/restart_alt:", on_click=reset_profile,
                  args=(data,), width="stretch")
        c2.button("Trocar pessoa", icon=":material/switch_account:", on_click=logout, width="stretch")


def navigation():
    labels = [("Viagem", "route"), ("Estações", "train"), ("Apoio", "support_agent"), ("Perfil", "person")]
    with st.container(key="navigation"):
        columns = st.columns(4)
        for column, (label, icon) in zip(columns, labels):
            column.button(label, icon=f":material/{icon}:", key=f"nav_{label}",
                          type="primary" if st.session_state["page"] == label else "secondary",
                          on_click=go, args=(label,), width="stretch")


def trip_editor(data, scenario):
    trip = st.session_state["trip"]
    ids = [s["estacao_id"] for s in data["stations"]]
    with st.form("trip_form"):
        ui.section_label("Para onde você vai?")
        st.selectbox("Estação de origem", ids, index=ids.index(trip["origin"]), key="edit_origin",
                     format_func=lambda sid: station_name(data, sid))
        st.selectbox("Estação de destino", ids, index=ids.index(trip["destination"]), key="edit_destination",
                     format_func=lambda sid: station_name(data, sid))
        st.selectbox("Horário da viagem simulada", list(range(24)), index=scenario["hora"],
                     format_func=lambda hour: f"{hour:02d}:00", key="edit_hour")
        st.form_submit_button("Consultar viagem", type="primary", width="stretch", on_click=save_trip, args=(data,))
    if st.session_state.get("trip_error"):
        st.error(st.session_state["trip_error"])
    st.button("Manter viagem atual", on_click=lambda: st.session_state.update(trip_editor=False), width="stretch")


def routine_picker(data):
    routines = current_routines(data)
    with st.expander("Usar uma rotina de viagem"):
        if not routines:
            st.write("Você pode criar uma rotina na aba Perfil.")
            st.button("Criar minha rotina", on_click=go, args=("Perfil",))
            return
        lookup = {r["rotina_id"]: r for r in routines}
        with st.form("routine_picker"):
            st.selectbox("Rotina", list(lookup), key="chosen_routine",
                         format_func=lambda rid: lookup[rid]["nome_rotina"])
            st.radio("Sentido da rotina", ["Ida", "Volta"], horizontal=True, key="chosen_direction")
            st.form_submit_button("Usar esta viagem", on_click=choose_routine, args=(data,), width="stretch")


def trip_screen(data, scenario):
    user, trip = st.session_state["user"], st.session_state["trip"]
    route = route_stations(data["stations"], trip["origin"], trip["destination"])
    ui.heading("SUA VIAGEM, DO SEU JEITO", f"Olá, {user['nome'].split()[0]}.", "Vamos cuidar do próximo percurso?")
    if st.session_state.get("trip_editor"):
        trip_editor(data, scenario)
        return
    main, side = st.columns([1.55, 1], gap="medium")
    with main:
        ui.trip_ticket(route[0]["nome_estacao"], route[-1]["nome_estacao"], scenario, len(route))
        st.button("Alterar viagem", icon=":material/edit_road:", key="edit_trip", width="stretch",
                  on_click=lambda: st.session_state.update(trip_editor=True))
        routine_picker(data)
    with side:
        with st.container(key="support_summary"):
            ui.section_label("Apoio para o seu caminho", "VOCÊ ESCOLHE O QUE PRECISA")
            request = st.session_state.get("request")
            if request:
                status = {"pendente": "Pedido enviado", "confirmado": "Equipe designada",
                          "concluido": "Atendimento concluído", "cancelado": "Pedido cancelado"}[request["status"]]
                st.write(f"**{status}**")
                st.caption(f"{request['id']} · atendimento simulado")
                label = "Acompanhar meu pedido"
            else:
                st.write("Orientação, embarque ou acompanhamento: conte qual apoio facilita a sua viagem.")
                st.caption("Não é necessário informar um diagnóstico.")
                label = "Solicitar apoio"
            st.button(label, icon=":material/support_agent:", type="primary", width="stretch",
                      on_click=go, args=("Apoio",))
        with st.container(key="trip_actions"):
            ui.section_label("Antes de sair")
            st.write("Confira os recursos publicados para as estações de embarque e desembarque.")
            st.button("Explorar estações", icon=":material/train:", width="stretch", on_click=go, args=("Estações",))
    ui.section_label("O que considerar nesta viagem")
    insights = route_insights(user, route, scenario)
    if not insights:
        ui.note("Sem ocorrência programada neste cenário",
                "Confira a acessibilidade das estações e, se precisar, solicite orientação para o embarque.", "success")
    for tone, title, description in insights:
        ui.note(title, description, tone)
    with st.expander(f"Ver percurso · {len(route)} estações"):
        st.caption("Diagrama da ordem das estações. Não representa distâncias nem tempo de viagem.")
        ui.route_map(route, affected_on_route(route, scenario))


def stations_screen(data, scenario):
    ui.heading("LINHA 7–RUBI", "Conheça sua estação", "Acessibilidade e informações úteis em um só lugar.")
    search = st.text_input("Buscar estação", placeholder="Digite o nome de uma estação", key="station_search")
    filtered = [s for s in data["stations"] if normalize(search) in normalize(s["nome_estacao"])]
    if not filtered:
        st.info("Nenhuma estação encontrada. Tente outra parte do nome.")
        return
    choices = [s["estacao_id"] for s in filtered]
    current = st.session_state.get("station_choice", st.session_state["trip"]["origin"])
    if current not in choices:
        st.session_state["station_choice"] = choices[0]
    elif "station_choice" not in st.session_state:
        st.session_state["station_choice"] = current
    selected = st.selectbox("Estação", choices, key="station_choice", format_func=lambda sid: station_name(data, sid))
    station = next(s for s in filtered if s["estacao_id"] == selected)
    with st.container(key="station_details"):
        ui.section_label(station["nome_estacao"], "CADASTRO DA ESTAÇÃO")
        ui.resource_grid(station)
        st.caption("Os itens publicados descrevem a estrutura cadastrada; não confirmam funcionamento atual. “Não informado” não significa inexistente.")
        affected = affected_on_route([station], scenario)
        if affected:
            ui.note("Atenção nesta estação", "Há uma restrição operacional programada neste cenário. Solicite orientação antes do embarque.", "warning")
        if scenario["closed"]:
            ui.note("Linha fechada neste cenário", "A consulta ao cadastro continua disponível. Para viajar, escolha outro horário.", "info")
        with st.expander("Endereço, integrações e fonte"):
            st.write(station["recursos"].get("endereco") or "Endereço não informado no cadastro.")
            integrations = station["recursos"].get("integracoes", "")
            if integrations:
                st.write("**Integrações descritas no cadastro:**")
                st.write(integrations)
                st.caption("A vigência das integrações não é verificada pelo protótipo. Não são usadas para sugerir trajetos fora da Linha 7.")
            st.caption(f"Data registrada no cadastro: {station.get('data_consulta', 'não informada')}.")
            source = station.get("fonte_url", "")
            if source.startswith("https://www.tictrens.com.br/"):
                st.link_button("Consultar fonte da operadora", source, icon=":material/open_in_new:")
    with st.expander(f"Todas as estações · {len(data['stations'])}"):
        trip = st.session_state["trip"]
        route = route_stations(data["stations"], trip["origin"], trip["destination"])
        ui.route_map(data["stations"], affected_on_route(data["stations"], scenario), route)


def support_screen(data, scenario):
    state = st.session_state
    trip, user = state["trip"], state["user"]
    ui.heading("ASSISTÊNCIA AO PASSAGEIRO", "Você não precisa planejar tudo sozinho.",
               "Diga qual apoio ajudaria e acompanhe cada etapa do pedido.")
    st.write(f"**{station_name(data, trip['origin'])} → {station_name(data, trip['destination'])}** · {scenario['horario']} na simulação")
    request = state.get("request")
    if request:
        with st.container(key="support_card"):
            labels = {"pendente": ("Pedido enviado · aguardando equipe", "warning"),
                      "confirmado": ("Equipe designada · confirmação simulada", "success"),
                      "concluido": ("Atendimento concluído na simulação", "success"),
                      "cancelado": ("Pedido cancelado", "info")}
            label, tone = labels[request["status"]]
            ui.note(label, f"Protocolo {request['id']}. Este atendimento é fictício e não contata a operadora.", tone)
            ui.support_steps(request["status"])
            st.write("**Apoio solicitado:** " + "; ".join(request["support"]))
            if request["note"]:
                st.write("**Observação:**")
                st.text(request["note"])
            if request["status"] == "pendente":
                st.write("Ainda não há responsável nem ponto de encontro confirmado. A próxima etapa depende da resposta da equipe.")
            if request["staff"] and request["status"] in {"confirmado", "concluido"}:
                st.write(f"**Quem recebe você:** {request['staff']}")
                st.write(f"**Onde encontrar:** {request['meeting']}")
            if request["status"] in {"pendente", "confirmado"}:
                st.button("Cancelar pedido", on_click=advance_support, args=("cancelar",), key="cancel_request")
        if request["status"] in {"pendente", "confirmado"}:
            with st.expander("Apresentação · simular resposta da equipe", expanded=True):
                st.caption("Controle do apresentador. A equipe e a confirmação são fictícias.")
                if request["status"] == "pendente":
                    st.button("Simular confirmação", type="primary", on_click=advance_support,
                              args=("confirmar",), key="confirm_request", width="stretch")
                else:
                    st.button("Simular conclusão", type="primary", on_click=advance_support,
                              args=("concluir",), key="finish_request", width="stretch")
            return
    if scenario["closed"]:
        ui.note("Escolha outro horário para pedir apoio", "A linha está fechada neste cenário. Altere o horário em Controles da apresentação.", "warning")
        return
    ui.section_label("Qual apoio você precisa?" if not request else "Iniciar outro pedido")
    st.caption("Todos os perfis podem pedir apoio, inclusive para uma necessidade temporária.")
    with st.form("support_form"):
        st.multiselect("Tipo de apoio", SUPPORT_OPTIONS, default=preferred_support(user), key="support_types")
        st.text_area("Algo mais que a equipe deveria saber? (opcional)", key="support_note", max_chars=240,
                     placeholder="Exemplo fictício: prefiro receber orientação por texto.")
        st.form_submit_button("Enviar pedido simulado", type="primary", width="stretch", on_click=send_request, args=(data,))
    if state.get("support_error"):
        st.error(state["support_error"])
    with st.expander("Como funciona esta demonstração?"):
        st.write("O pedido começa pendente. O apresentador simula a resposta da equipe e, depois, a conclusão. Ao mudar o percurso, o horário ou o cenário, é preciso fazer um novo pedido.")
        st.link_button("Orientações oficiais sobre acessibilidade", "https://www.tictrens.com.br/sua-viagem/acessibilidade")


def profile_screen(data):
    user = st.session_state["user"]
    ui.heading("PREFERÊNCIAS E ROTINA", "Um app que acompanha você.", "Escolha o apoio que faz sentido para a sua viagem.")
    prefs, routines_tab, display = st.tabs(["Meu apoio", "Minha rotina", "Leitura"])
    with prefs:
        st.caption("Perfil fictício. As alterações valem apenas nesta sessão; não exigimos diagnóstico.")
        with st.form("profile_form"):
            st.text_input("Nome fictício", value=user["nome"], key="profile_name", max_chars=60)
            st.checkbox("Prefiro um percurso sem escadas", value=user.get("necessita_percurso_sem_escadas", False), key="pref_stairs")
            st.checkbox("Quero orientação no embarque", value=user.get("prefere_orientacao_embarque", False), key="pref_orientation")
            st.checkbox("Quero acompanhamento na estação", value=user.get("solicita_acompanhamento", False), key="pref_accompany")
            st.checkbox("Utilizo cadeira de rodas", value=user.get("usa_cadeira_rodas", False), key="pref_wheelchair")
            options = ["app", "voz_alta", "app_voz", "sms"]
            labels = {"app": "Texto no aplicativo", "voz_alta": "Orientação falada pela equipe", "app_voz": "Texto e orientação falada", "sms": "Mensagem de texto"}
            value = user.get("preferencia_comunicacao", "app")
            st.selectbox("Como prefere se comunicar com a equipe?", options, index=options.index(value) if value in options else 0,
                         format_func=lambda v: labels[v], key="pref_communication")
            st.caption("A preferência é registrada para a simulação; o protótipo não envia mensagens nem gera áudio.")
            st.form_submit_button("Salvar preferências", type="primary", on_click=save_profile, width="stretch")
        if st.session_state.get("profile_error"):
            st.error(st.session_state["profile_error"])
    with routines_tab:
        routines = current_routines(data)
        for routine in routines:
            ida, volta = routine["legs"]["ida"], routine["legs"]["volta"]
            with st.container(border=True):
                st.write(f"**{routine['nome_rotina']}**")
                st.write(f"{station_name(data, ida['origin'])} → {station_name(data, ida['destination'])}")
                st.caption(f"{' · '.join(routine['days'])} | Ida {ida['departure']} | Volta {volta['departure']}")
                st.button("Usar ida", key=f"out_{routine['rotina_id']}", on_click=apply_trip, args=(ida,))
                st.button("Usar retorno", key=f"back_{routine['rotina_id']}", on_click=apply_trip, args=(volta,))
        with st.expander("Criar ou editar minha rotina da sessão", expanded=not bool(routines)):
            ids = [s["estacao_id"] for s in data["stations"]]
            trip = st.session_state["trip"]
            custom = st.session_state.get("session_routine")
            base = custom["legs"]["ida"] if custom else trip
            with st.form("routine_form"):
                st.selectbox("Objetivo", ["Trabalho", "Estudo", "Saúde", "Lazer", "Outro"], key="routine_purpose")
                st.selectbox("Origem habitual", ids, index=ids.index(base["origin"]), key="routine_origin", format_func=lambda sid: station_name(data, sid))
                st.selectbox("Destino habitual", ids, index=ids.index(base["destination"]), key="routine_destination", format_func=lambda sid: station_name(data, sid))
                st.multiselect("Dias da semana", ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
                               default=custom["days"] if custom else ["Seg", "Ter", "Qua", "Qui", "Sex"], key="routine_days")
                st.time_input("Saída de ida", value=time.fromisoformat(base["departure"]), key="routine_departure")
                st.time_input("Saída de retorno", value=time.fromisoformat(custom["legs"]["volta"]["departure"]) if custom else time(18, 0), key="routine_return")
                st.caption("O retorno usa o percurso inverso. Seus horários são preferências; não são previsão de chegada do trem.")
                st.form_submit_button("Salvar rotina da sessão", type="primary", on_click=save_routine, args=(data,), width="stretch")
            if st.session_state.get("routine_error"):
                st.error(st.session_state["routine_error"])
    with display:
        st.toggle("Texto ampliado", key="large_text")
        st.toggle("Mais contraste", key="high_contrast")
        st.caption("As informações usam texto além das cores. Você também pode navegar com Tab e ativar os controles com Enter ou Espaço.")
    st.button("Trocar pessoa da demonstração", icon=":material/logout:", on_click=logout, width="stretch")


def main():
    st.set_page_config(page_title="Embarque Inclusivo · Sua viagem", layout="wide",
                       page_icon=str(ROOT / "identidade visual" / "embarque-inclusivo-simbolo-negativo.png"),
                       initial_sidebar_state="collapsed")
    # Reatribuir preserva as preferências mesmo nas páginas sem esses widgets.
    # O Streamlit remove automaticamente o estado de widgets que deixam de aparecer.
    for key in ("large_text", "high_contrast"):
        st.session_state[key] = st.session_state.get(key, False)
    st.session_state["manual_hour"] = st.session_state.get("manual_hour", 10)
    ui.style(st.session_state["large_text"], st.session_state["high_contrast"])
    ui.brand_header()
    try:
        data = get_data()
    except (OSError, ValueError) as error:
        st.error("Não foi possível carregar a demonstração. Confira os arquivos de dados do projeto.")
        with st.expander("Detalhes para manutenção"):
            st.text(str(error))
        st.stop()
    if not st.session_state.get("user"):
        login_screen(data)
    else:
        scenario = scenario_for(data["occurrences"], st.session_state["scenario_mode"], st.session_state.get("manual_hour", 10))
        demo_controls(data, scenario)
        navigation()
        if st.session_state.get("notice"):
            st.info(st.session_state.pop("notice"))
        page = st.session_state["page"]
        if page == "Viagem":
            trip_screen(data, scenario)
        elif page == "Estações":
            stations_screen(data, scenario)
        elif page == "Apoio":
            support_screen(data, scenario)
        elif page == "Perfil":
            profile_screen(data)
    ui.footer()


if __name__ == "__main__":
    main()
