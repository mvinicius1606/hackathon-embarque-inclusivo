from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
SIM_DIR = DATA_DIR / "simulados"


@st.cache_data
def load_data():
    users = pd.read_csv(SIM_DIR / "dim_usuario.csv", sep=";")
    rotinas = pd.read_csv(SIM_DIR / "dim_rotina.csv", sep=";")
    viagens = pd.read_csv(SIM_DIR / "fato_viagem_planejada.csv", sep=";")
    ocorrencias = pd.read_csv(SIM_DIR / "dim_ocorrencia.csv", sep=";")
    estacoes_dim = pd.read_csv(SIM_DIR / "dim_estacao.csv", sep=";")
    estacoes_real = pd.read_csv(DATA_DIR / "estacoes_linha7.csv", sep=";")

    for frame in [users, rotinas, viagens, ocorrencias, estacoes_dim, estacoes_real]:
        frame.fillna("", inplace=True)

    return users, rotinas, viagens, ocorrencias, estacoes_dim, estacoes_real


@st.cache_data
def build_station_lookup(dim_estacoes):
    return {row["estacao_id"]: row["nome_estacao"] for _, row in dim_estacoes.iterrows()}


@st.cache_data
def demo_users():
    users = pd.read_csv(SIM_DIR / "dim_usuario.csv", sep=";")
    return users[users["dados_sinteticos"].astype(bool)]


def phone_shell():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        div[data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #eef6ff 0%, #ffffff 35%, #f4f7fb 100%);
        }
        [data-testid="stSidebar"] {display: none;}
        .phone-frame {
            max-width: 420px;
            min-height: 90vh;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 28px;
            border: 1px solid #dfe8f3;
            box-shadow: 0 20px 45px rgba(14, 30, 66, 0.12);
            padding: 16px 14px 20px 14px;
        }
        .app-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 4px 14px 4px;
            color: #1b2440;
        }
        .pill {
            display: inline-block;
            background: #eaf2ff;
            color: #1d4ed8;
            border-radius: 999px;
            padding: 5px 10px;
            font-size: 0.72rem;
            font-weight: 700;
        }
        .status-card {
            background: linear-gradient(135deg, #e0f2fe, #f0fdf4);
            border-radius: 20px;
            padding: 14px;
            border: 1px solid #d4f1e3;
            margin-bottom: 12px;
        }
        .support-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
            margin-top: 10px;
        }
        .mini-action {
            background: #f5f8ff;
            border-radius: 16px;
            padding: 12px 10px;
            border: 1px solid #dbeafe;
            text-align: center;
            font-weight: 600;
            color: #1d4ed8;
        }
        .big-button {
            width: 100%;
            border-radius: 16px;
            min-height: 52px;
            font-weight: 700;
        }
        .card {
            border-radius: 18px;
            background: #f9fbff;
            border: 1px solid #e5edf8;
            padding: 14px;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_status(value):
    if value is None:
        return "Sem dado"
    return str(value).replace("_", " ").title()


def login_signup_screen():
    st.markdown('<div class="phone-frame">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="app-header">
            <div><strong>Embarque Inclusivo</strong><br><span style='font-size: 0.8rem; color: #64748b;'>Acesso de demonstração</span></div>
            <span class="pill">Demo</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["Entrar", "Cadastrar"])

    with tab1:
        with st.form("login_form"):
            nome = st.text_input("Nome", key="login_nome")
            senha = st.text_input("Senha", type="password", key="login_senha")
            submitted = st.form_submit_button("Entrar", use_container_width=True)

        if submitted:
            users = demo_users()
            match = users[users["nome"].astype(str).str.lower() == nome.strip().lower()]
            if not match.empty:
                st.session_state["logged_in"] = True
                st.session_state["usuario_logado"] = match.iloc[0].to_dict()
                st.session_state["app_phase"] = 1
                st.rerun()
            else:
                st.error("Usuário não encontrado. Use um perfil da demonstração ou cadastre um novo.")

    with tab2:
        with st.form("cadastro_form"):
            nome_novo = st.text_input("Seu nome", key="cadastro_nome")
            senha_nova = st.text_input("Crie uma senha", type="password", key="cadastro_senha")
            necessidade = st.selectbox("Precisa de apoio principal?", ["Nenhuma", "Mobilidade", "Visual", "Auditiva", "Cognitiva"])
            assistencia = st.checkbox("Quero facilitar o suporte durante a viagem")
            enviar = st.form_submit_button("Criar conta", use_container_width=True)

        if enviar and nome_novo.strip():
            st.session_state["logged_in"] = True
            st.session_state["usuario_logado"] = {
                "nome": nome_novo.strip(),
                "deficiencia_informada": necessidade,
                "usa_cadeira_rodas": necessidade == "Mobilidade",
                "preferencia_comunicacao": "app",
                "necessita_percurso_sem_escadas": necessidade == "Mobilidade",
                "prefere_orientacao_embarque": assistencia,
                "solicita_acompanhamento": assistencia,
                "usuario_id": "USR-DEMO",
                "dados_sinteticos": True,
            }
            st.session_state["app_phase"] = 1
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def rotina_screen():
    usuario = st.session_state["usuario_logado"]
    users, rotinas, viagens, ocorrencias, estacoes_dim, estacoes_real = load_data()
    station_lookup = build_station_lookup(estacoes_dim)
    estacoes = [row["nome_estacao"] for _, row in estacoes_dim.iterrows()]

    st.markdown('<div class="phone-frame">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="app-header">
            <div><strong>Minha rotina</strong><br><span style='font-size: 0.8rem; color: #64748b;'>Fase 2</span></div>
            <span class="pill">Perfil</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(f"Olá, {usuario['nome']}")

    with st.form("rotina_form"):
        origem = st.selectbox("Origem", estacoes, index=0)
        destino = st.selectbox("Destino", estacoes, index=1)
        horario = st.time_input("Horário habitual")
        dias = st.multiselect("Dias da semana", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"], default=["Segunda", "Quarta", "Sexta"])
        apoio = st.checkbox("Preciso de ajuda no embarque")
        necessidade = st.selectbox("Tipo de apoio", ["Nenhum", "Cadeira de rodas", "Orientação", "Apoio em embarque", "Agora não"])

        col1, col2 = st.columns(2)
        with col1:
            salvar = st.form_submit_button("Salvar rotina", use_container_width=True)
        with col2:
            agora_nao = st.form_submit_button("Agora não", use_container_width=True)

    if salvar:
        st.session_state["rotina"] = {
            "origem": origem,
            "destino": destino,
            "horario": str(horario),
            "dias": dias,
            "apoio": apoio,
            "tipo_apoio": necessidade,
        }
        st.session_state["app_phase"] = 2
        st.success("Rotina salva com sucesso.")
        st.rerun()

    if agora_nao:
        st.session_state["rotina"] = {"status": "Agora não", "origem": origem, "destino": destino}
        st.session_state["app_phase"] = 2
        st.info("Você pode configurar a rotina depois. A demonstração segue com o cenário atual.")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def dashboard_screen():
    usuario = st.session_state["usuario_logado"]
    users, rotinas, viagens, ocorrencias, estacoes_dim, estacoes_real = load_data()
    station_lookup = build_station_lookup(estacoes_dim)

    st.markdown('<div class="phone-frame">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="app-header">
            <div><strong>Minha viagem</strong><br><span style='font-size: 0.8rem; color: #64748b;'>Fase 3</span></div>
            <span class="pill">Online</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(f"Bem-vindo, {usuario['nome']}")

    status_busca = st.selectbox("Selecione a rotina", ["Trabalho", "Estudo", "Consulta", "Lazer"], index=0)
    hora_demo = st.slider("Hora da simulação", 0, 23, 7)
    ocorrencia = ocorrencias[ocorrencias["hora"] == hora_demo].iloc[0]

    st.markdown(
        f"""
        <div class="status-card">
            <div style="font-size: 0.75rem; color: #475569; text-transform: uppercase; letter-spacing: 0.08em;">Situação da linha</div>
            <div style="font-size: 1.3rem; font-weight: 800; margin-top: 6px;">{format_status(ocorrencia['status_operacao'])}</div>
            <div style="margin-top: 6px; color: #334155;">{ocorrencia['impacto_usuarios']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    with cols[0]:
        st.metric("Movimento", format_status(ocorrencia["movimento"]))
    with cols[1]:
        st.metric("Horario", f"{int(ocorrencia['hora']):02d}:00")

    st.markdown("<div class='support-grid'>", unsafe_allow_html=True)
    actions = [
        ("🛟", "Suporte técnico"),
        ("❓", "Ajuda"),
        ("📅", "Agendamento"),
        ("🤝", "Assistência"),
    ]
    for icon, label in actions:
        col = st.columns(2)[0] if False else None
    st.markdown("</div>", unsafe_allow_html=True)

    action_cols = st.columns(2)
    for idx, (icon, label) in enumerate(actions):
        with action_cols[idx % 2]:
            if st.button(f"{icon} {label}", key=f"action_{idx}", use_container_width=True):
                st.session_state["action_message"] = label
                st.toast(f"{label} acionado na demonstração.")

    if "action_message" in st.session_state:
        st.info(f"Ação ativa: {st.session_state['action_message']}")

    st.markdown("### Detalhes da viagem")
    origem = "Palmeiras-Barra Funda"
    destino = "Lapa"
    st.markdown(
        """
        <div class='card'>
            <div style='font-size: 0.8rem; color: #64748b;'>Rota atual</div>
            <div style='font-size: 1.2rem; font-weight: 700; margin-top: 6px;'>Palmeiras-Barra Funda → Lapa</div>
            <div style='color: #475569; margin-top: 8px;'>Saída: 07:30 · Duração: 15 min · Assistência prevista: Sim</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Acessibilidade da estação")
    estacao_origem = estacoes_real[estacoes_real["estacao"] == origem].iloc[0]
    estacao_destino = estacoes_real[estacoes_real["estacao"] == destino].iloc[0]

    for label, estacao in [("Origem", estacao_origem), ("Destino", estacao_destino)]:
        st.write(f"{label}: {estacao['estacao']}")
        st.json(
            {
                "elevador": estacao.get("elevador"),
                "rampa": estacao.get("rampa"),
                "piso_tatil": estacao.get("piso_tatil"),
                "banheiro_acessivel_unissex": estacao.get("banheiro_acessivel_unissex"),
                "transposicao_de_plataformas": estacao.get("transposicao_de_plataformas"),
            }
        )

    st.markdown("### Status do apoio")
    status = st.radio("Estado da solicitação", ["Pendente", "Confirmado", "Concluído"], horizontal=True)
    if status == "Confirmado":
        st.success("Responsável designado: João da operação de apoio. Ponto de encontro: plataforma central.")
    elif status == "Pendente":
        st.warning("Solicitação em análise. Aguarde confirmação da equipe de suporte.")
    else:
        st.info("Suporte concluído e acompanhamento encerrado para esta viagem.")

    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Embarque Inclusivo", page_icon="🚉", layout="centered")
    phone_shell()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "app_phase" not in st.session_state:
        st.session_state["app_phase"] = 0

    if not st.session_state["logged_in"]:
        login_signup_screen()
    elif st.session_state["app_phase"] == 0:
        login_signup_screen()
    elif st.session_state["app_phase"] == 1:
        rotina_screen()
    else:
        dashboard_screen()


if __name__ == "__main__":
    main()
