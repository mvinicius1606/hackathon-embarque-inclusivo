"""Protótipo de demonstração. Requer os CSVs em data/ e data/simulados/.
Execute na raiz do projeto: python -m streamlit run app/src/streamlit_app.py
Correções: contêiner visual, localização/validação dos dados, filtros seguros
 e exibição do percurso selecionado. Não implementa autenticação real.
"""
from pathlib import Path
from html import escape
import unicodedata

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def find_project_root():
    """Localiza data/ junto ao app ou em um dos diretórios superiores."""
    for start in (Path(__file__).resolve().parent, Path.cwd().resolve()):
        for candidate in (start, *start.parents):
            if (candidate / "data" / "simulados").is_dir():
                return candidate
    return Path(__file__).resolve().parent


ROOT = find_project_root()
DATA_DIR = ROOT / "data"


def read_csv_checked(path, required_columns):
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo necessário não encontrado: {path}")
    frame = pd.read_csv(path, sep=";", dtype=str, keep_default_na=False, encoding="utf-8-sig")
    frame.columns = frame.columns.str.strip()
    missing = set(required_columns) - set(frame.columns)
    if missing:
        raise ValueError(f"{path.name}: faltam as colunas {', '.join(sorted(missing))}. "
                         "Confira também o separador ponto e vírgula (;).")
    return frame


@st.cache_data
def load_data(data_dir):
    data_dir = Path(data_dir)
    sim_dir = data_dir / "simulados"
    users = read_csv_checked(sim_dir / "dim_usuario.csv", ["usuario_id", "nome", "dados_sinteticos"])
    rotinas = read_csv_checked(sim_dir / "dim_rotina.csv", ["rotina_id"])
    viagens = read_csv_checked(sim_dir / "fato_viagem_planejada.csv", ["usuario_id", "rotina_id"])
    ocorrencias = read_csv_checked(sim_dir / "dim_ocorrencia.csv",
        ["hora", "status_operacao", "movimento", "impacto_usuarios", "dados_sinteticos"])
    estacoes_dim = read_csv_checked(sim_dir / "dim_estacao.csv", ["estacao_id", "nome_estacao"])
    estacoes_real = read_csv_checked(data_dir / "estacoes_linha7.csv", ["estacao"])

    # Não usar astype(bool): a string "False" também é verdadeira em Python.
    for frame in (users, ocorrencias):
        frame["dados_sinteticos"] = frame["dados_sinteticos"].str.strip().str.casefold().isin(
            ["true", "1", "sim"]
        )
    ocorrencias = ocorrencias.loc[ocorrencias["dados_sinteticos"]].copy()
    ocorrencias["hora"] = pd.to_numeric(ocorrencias["hora"], errors="coerce")
    valid_hours = ocorrencias["hora"].between(0, 23) & (ocorrencias["hora"] % 1 == 0)
    if not valid_hours.all():
        raise ValueError("dim_ocorrencia.csv: hora deve ser um inteiro de 0 a 23.")
    ocorrencias["hora"] = ocorrencias["hora"].astype(int)
    return users, rotinas, viagens, ocorrencias, estacoes_dim, estacoes_real


def normalized(value):
    value = unicodedata.normalize("NFKD", str(value).strip().casefold())
    return " ".join("".join(c for c in value if not unicodedata.combining(c)).split())


def demo_users():
    users = load_data(str(DATA_DIR))[0]
    return users.loc[users["dados_sinteticos"]]


def phone_shell():
    st.markdown(
        """
        <style>
        /* Os widgets precisam estar no contêiner real do Streamlit.
           Uma div aberta em st.markdown não envolve os widgets seguintes. */
        .block-container {
            max-width: 460px;
            margin: 3.5rem auto 1rem auto;
            background: var(--background-color, #ffffff);
            border-radius: 28px;
            border: 1px solid #dfe8f3;
            box-shadow: 0 20px 45px rgba(14, 30, 66, 0.12);
            padding: 16px 14px 24px 14px;
        }
        div[data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #eef6ff 0%, #ffffff 35%, #f4f7fb 100%);
        }
        @media (max-width: 480px) {
            .block-container { border-radius: 16px; margin-top: 3.5rem; }
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
        /* Identidade visual colors */
        .brand-teal { color: #0f8b84; }
        .brand-magenta { color: #b41763; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Cabeçalho com logo da identidade visual (quando disponível)
    logo_path = ROOT / "identidade visual" / "embarque-inclusivo-logo-horizontal.png"
    if logo_path.is_file():
        cols = st.columns([1, 4])
        with cols[0]:
            st.image(str(logo_path), width=120)
        with cols[1]:
            st.markdown("""
            <div style='display:flex;flex-direction:column;justify-content:center;height:100%'>
                <div style='font-size:1.1rem;font-weight:700'>Embarque Inclusivo</div>
                <div style='color:#64748b;font-size:0.85rem'>Demonstração — perfis e operação simulados</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.title("Embarque Inclusivo")


def format_status(value):
    if value is None or pd.isna(value) or str(value).strip() == "":
        return "Sem dado"
    return str(value).replace("_", " ").title()


def login_signup_screen():

    st.markdown(
        """
        <div class="app-header">
            <div><strong>Embarque Inclusivo</strong><br><span style='font-size: 0.8rem; color: #64748b;'>Acesso de demonstração</span></div>
            <span class="pill">Demo</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Acesso simulado, sem senha. Use apenas perfis fictícios.")
    tab1, tab2 = st.tabs(["Entrar", "Cadastrar"])
    st.caption("Perfis disponíveis: " + ", ".join(demo_users()["nome"].tolist()))

    with tab1:
        with st.form("login_form"):
            nome = st.text_input("Nome", key="login_nome")
            submitted = st.form_submit_button("Entrar", use_container_width=True)

        if submitted:
            users = demo_users()
            names = users["nome"].map(normalized)
            typed_name = normalized(nome)
            match = users.loc[names == typed_name]
            if match.empty and typed_name:
                match = users.loc[names.str.split().str[0] == typed_name]
            if len(match) == 1:
                st.session_state["logged_in"] = True
                st.session_state["usuario_logado"] = match.iloc[0].to_dict()
                st.session_state["app_phase"] = 1
                st.rerun()
            else:
                st.error("Informe um nome da demonstração. Se houver nomes repetidos, use o nome completo.")

    with tab2:
        with st.form("cadastro_form"):
            nome_novo = st.text_input("Seu nome", key="cadastro_nome")
            necessidade = st.selectbox("Precisa de apoio principal?", ["Nenhuma", "Mobilidade", "Visual", "Auditiva", "Cognitiva"])
            cadeira_rodas = st.checkbox("Utilizo cadeira de rodas")
            sem_escadas = st.checkbox("Preciso de percurso sem escadas")
            assistencia = st.checkbox("Quero facilitar o suporte durante a viagem")
            criar_rotina_agora = st.checkbox("Criar rotina agora?")
            enviar = st.form_submit_button("Criar conta", use_container_width=True)

        if enviar and nome_novo.strip():
            st.session_state["logged_in"] = True
            st.session_state["usuario_logado"] = {
                "nome": nome_novo.strip(),
                "deficiencia_informada": necessidade,
                "usa_cadeira_rodas": cadeira_rodas,
                "preferencia_comunicacao": "app",
                "necessita_percurso_sem_escadas": sem_escadas,
                "prefere_orientacao_embarque": assistencia,
                "solicita_acompanhamento": assistencia,
                "usuario_id": "USR-DEMO",
                "dados_sinteticos": True,
            }
            # se o usuário escolheu criar rotina agora, ir para a tela de rotina
            if criar_rotina_agora:
                st.session_state["app_phase"] = 1
                st.session_state["show_rotina_after_signup"] = True
            else:
                # avançar para painel principal (mapa genérico se sem rotina)
                st.session_state["app_phase"] = 2
            st.rerun()



def rotina_screen():
    usuario = st.session_state["usuario_logado"]
    users, rotinas, viagens, ocorrencias, estacoes_dim, estacoes_real = load_data(str(DATA_DIR))
    estacoes = estacoes_dim["nome_estacao"].str.strip()
    estacoes = estacoes[estacoes.ne("")].drop_duplicates().tolist()
    if len(estacoes) < 2:
        st.warning("Cadastre pelo menos duas estações para escolher o percurso.")
        return

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

    # Link para alterar rotina a qualquer momento
    st.markdown("**Ações rápidas**")
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_a:
        if st.button("Planejar percurso pontual"):
            st.session_state["plan_trip"] = True
            st.session_state["app_phase"] = 2
            st.rerun()
    with col_b:
        if st.button("Contato com suporte"):
            st.session_state["contact_support"] = True
            st.toast("Contato com suporte simulado iniciado")
    with col_c:
        if st.button("Ver linha completa"):
            st.session_state["view_line"] = True
            st.session_state["app_phase"] = 2
            st.rerun()

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

    if salvar and (origem == destino or not dias):
        st.warning("Escolha estações diferentes e pelo menos um dia da semana.")
        return

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



def dashboard_screen():
    usuario = st.session_state["usuario_logado"]
    users, rotinas, viagens, ocorrencias, estacoes_dim, estacoes_real = load_data(str(DATA_DIR))

    # Se o usuário não tiver rotina definida, mostrar mapa genérico
    rotina = st.session_state.get("rotina", {})
    if not rotina or rotina.get("status") == "Agora não":
        st.markdown("### Mapa da Linha 7–Rubi (genérico)")
        # desenhar mapa simples horizontal com estações
        estacoes = estacoes_dim["nome_estacao"].dropna().unique().tolist()
        fig, ax = plt.subplots(figsize=(6, 1.2))
        ax.hlines(0, 0, len(estacoes)-1, colors="#bdbdbd", linewidth=6)
        xs = list(range(len(estacoes)))
        ax.scatter(xs, [0]*len(xs), s=200, color="#b41763")
        for i, e in enumerate(estacoes):
            ax.text(i, -0.25, e, rotation=45, ha='right', fontsize=8)
        ax.axis('off')
        st.pyplot(fig)
        st.info("Você não tem uma rotina salva — use 'Alterar modos e rotinas' para criar uma.")

    # Botões principais sempre disponíveis
    st.markdown("### Controles")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Planejar percurso pontual", use_container_width=True):
            st.session_state["plan_trip"] = True
            st.toast("Plano pontual iniciado")
    with c2:
        if st.button("Contato com suporte", use_container_width=True):
            st.toast("Contato com suporte simulado")
    with c3:
        if st.button("Alterar modos e rotinas", use_container_width=True):
            st.session_state["app_phase"] = 1
            st.rerun()
    with c4:
        if st.button("Ver linha completa", use_container_width=True):
            st.session_state["view_line_full"] = True
            st.toast("Exibindo a linha completa")

    st.markdown(
        """
        <div class="app-header">
            <div><strong>Minha viagem</strong><br><span style='font-size: 0.8rem; color: #64748b;'>Fase 3</span></div>
            <span class="pill">Simulação</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(f"Bem-vindo, {usuario['nome']}")

    hora_demo = st.slider("Hora da simulação", 0, 23, 7)
    if "data" in ocorrencias.columns:
        datas = ocorrencias["data"].drop_duplicates().sort_values().tolist()
        if len(datas) > 1:
            data_demo = st.selectbox("Data da simulação", datas)
            ocorrencias = ocorrencias.loc[ocorrencias["data"] == data_demo]
    matches = ocorrencias.loc[ocorrencias["hora"] == hora_demo]
    if matches.empty:
        st.warning(f"Sem dados simulados para {hora_demo:02d}:00. Escolha outro horário.")
        return
    if len(matches) != 1:
        st.warning("Há mais de um registro para esse horário. Confira dim_ocorrencia.csv.")
        return
    ocorrencia = matches.iloc[0]

    st.markdown(
        f"""
        <div class="status-card">
            <div style="font-size: 0.75rem; color: #475569; text-transform: uppercase; letter-spacing: 0.08em;">Situação da linha</div>
            <div style="font-size: 1.3rem; font-weight: 800; margin-top: 6px;">{escape(format_status(ocorrencia['status_operacao']))}</div>
            <div style="margin-top: 6px; color: #334155;">{escape(str(ocorrencia['impacto_usuarios']))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    with cols[0]:
        st.metric("Movimento", format_status(ocorrencia["movimento"]))
    with cols[1]:
        st.metric("Horario", f"{int(ocorrencia['hora']):02d}:00")

    actions = [
        ("🛟", "Suporte técnico"),
        ("❓", "Ajuda"),
        ("📅", "Agendamento"),
        ("🤝", "Assistência"),
    ]

    action_cols = st.columns(2)
    for idx, (icon, label) in enumerate(actions):
        with action_cols[idx % 2]:
            if st.button(f"{icon} {label}", key=f"action_{idx}", use_container_width=True):
                st.session_state["action_message"] = label
                st.toast(f"{label} acionado na demonstração.")

    if "action_message" in st.session_state:
        st.info(f"Ação ativa: {st.session_state['action_message']}")

    st.markdown("### Detalhes da viagem")
    rotina = st.session_state.get("rotina", {})
    origem = rotina.get("origem", "")
    destino = rotina.get("destino", "")
    # 'Ver linha completa' só para quem tem rotina
    if st.session_state.get("view_line") or st.session_state.get("view_line_full"):
        if rotina and origem and destino:
            st.success("Visualização completa da linha habilitada para usuários com rotina cadastrada.")
        else:
            st.warning("A visualização completa está disponível apenas para usuários com rotina cadastrada.")
            st.session_state.pop("view_line", None)
            st.session_state.pop("view_line_full", None)
    
    if not origem or not destino:
        st.info("Configure uma rotina para consultar as estações do percurso.")
        if st.button("Configurar rotina"):
            st.session_state["app_phase"] = 1
            st.rerun()
        return
    st.markdown(
        f"""
        <div class='card'>
            <div style='font-size: 0.8rem; color: #64748b;'>Rota informada</div>
            <div style='font-size: 1.2rem; font-weight: 700; margin-top: 6px;'>{escape(origem)} → {escape(destino)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if rotina.get("horario"):
        st.write("Horário habitual: " + rotina["horario"][:5])
    else:
        st.caption("Consulta avulsa; rotina ainda não salva.")

    st.markdown("### Acessibilidade da estação")
    st.caption("Cadastro estático: os itens abaixo não confirmam funcionamento atual.")
    stations = estacoes_real["estacao"].map(normalized)
    origem_rows = estacoes_real.loc[stations == normalized(origem)]
    destino_rows = estacoes_real.loc[stations == normalized(destino)]
    estacao_origem = origem_rows.iloc[0] if len(origem_rows) == 1 else None
    estacao_destino = destino_rows.iloc[0] if len(destino_rows) == 1 else None

    for label, estacao in [("Origem", estacao_origem), ("Destino", estacao_destino)]:
        if estacao is None:
            st.warning(f"{label}: cadastro ausente ou ambíguo para esta estação.")
            continue
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
    st.caption("Controle da demonstração: simula o estado de um pedido, sem contato com a operadora.")
    request_key = f"apoio_{usuario['usuario_id']}_{origem}_{destino}_{hora_demo}"
    # Apenas permitir suporte para usuários que indicaram necessidade de apoio
    permite_suporte = str(usuario.get("deficiencia_informada", "")).lower() not in ["nenhuma", "", "none"] or bool(usuario.get("usa_cadeira_rodas"))
    if not permite_suporte:
        st.info("Suporte disponível apenas para usuários que informaram necessidade de apoio no perfil.")
        status = st.radio("Estado da solicitação simulada", ["Sem suporte"], horizontal=True, key=request_key)
    else:
        status = st.radio("Estado da solicitação simulada", ["Pendente", "Confirmado", "Concluído"],
                          horizontal=True, key=request_key)
    if status == "Confirmado":
        st.success("Confirmação simulada. Responsável fictício: João da equipe de apoio. Ponto de encontro ilustrativo: entrada principal.")
    elif status == "Pendente":
        st.warning("Solicitação em análise. Aguarde confirmação da equipe de suporte.")
    else:
        st.info("Suporte concluído e acompanhamento encerrado para esta viagem.")

    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()



def main():
    st.set_page_config(page_title="Embarque Inclusivo", page_icon="🚉", layout="centered")
    phone_shell()
    st.caption("Demonstração — usuários, operação e atendimento simulados")
    try:
        load_data(str(DATA_DIR))
    except (OSError, ValueError, pd.errors.ParserError) as error:
        st.error(f"Não foi possível carregar os dados: {error}")
        st.info("Execute este arquivo dentro do repositório, mantendo a pasta data/ e os CSVs originais.")
        st.code("python -m streamlit run app/src/streamlit_app.py", language="bash")
        st.stop()

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
