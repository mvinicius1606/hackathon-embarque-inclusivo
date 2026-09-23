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

    estacoes_real = estacoes_real.fillna("")
    estacoes_dim = estacoes_dim.fillna("")

    return users, rotinas, viagens, ocorrencias, estacoes_dim, estacoes_real


@st.cache_data
def build_station_lookup(dim_estacoes):
    return {
        row["estacao_id"]: row["nome_estacao"]
        for _, row in dim_estacoes.iterrows()
    }


def format_status(value: str) -> str:
    return value.replace("_", " ").title()


def main():
    st.set_page_config(page_title="Embarque Inclusivo", page_icon="🚉", layout="wide")
    st.title("🚉 Embarque Inclusivo - Linha 7–Rubi")
    st.caption("Demonstração sintética do MVP para mobilidade inclusiva")

    users, rotinas, viagens, ocorrencias, estacoes_dim, estacoes_real = load_data()
    station_lookup = build_station_lookup(estacoes_dim)

    usuarios = users[users["dados_sinteticos"].astype(bool)]
    usuario_selecionado = st.sidebar.selectbox("Usuário fictício", usuarios["nome"].tolist())
    usuario = usuarios[usuarios["nome"] == usuario_selecionado].iloc[0]

    todas_viagens = viagens[viagens["usuario_id"] == usuario["usuario_id"]].copy()
    rotinas_do_usuario = rotinas[
        rotinas["rotina_id"].isin(todas_viagens["rotina_id"].unique())
    ].copy()

    if rotinas_do_usuario.empty:
        st.warning("Nenhuma rotina encontrada para o usuário selecionado.")
        return

    rotina_principal = rotinas_do_usuario.iloc[0]
    user_triage = st.sidebar.selectbox(
        "Trecho planejado",
        [
            f"{row['sentido'].title()} - {station_lookup.get(row['estacao_origem_id'])} → {station_lookup.get(row['estacao_destino_id'])}"
            for _, row in todas_viagens.iterrows()
        ],
    )

    selected_trip_index = [
        f"{row['sentido'].title()} - {station_lookup.get(row['estacao_origem_id'])} → {station_lookup.get(row['estacao_destino_id'])}"
        for _, row in todas_viagens.iterrows()
    ].index(user_triage)
    viagem = todas_viagens.iloc[selected_trip_index]

    hora_demo = st.sidebar.slider("Hora da viagem (simulação)", 0, 23, int(viagem["tempo_saida_id"].split("-")[-1][:2] if "TMP-" in viagem["tempo_saida_id"] else 8))

    ocorrencia_atual = ocorrencias[ocorrencias["hora"] == hora_demo].iloc[0]

    origem_nome = station_lookup.get(viagem["estacao_origem_id"], "Estação desconhecida")
    destino_nome = station_lookup.get(viagem["estacao_destino_id"], "Estação desconhecida")

    origem_real = estacoes_real[estacoes_real["estacao"] == origem_nome]
    destino_real = estacoes_real[estacoes_real["estacao"] == destino_nome]

    st.subheader(f"Perfil do usuário: {usuario['nome']}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Idade", int(usuario["idade_referencia"]))
    col2.metric("Deficiência informada", usuario["deficiencia_informada"])
    col3.metric("Usa cadeira de rodas", "Sim" if usuario["usa_cadeira_rodas"] else "Não")
    col4.metric("Apoio solicitado", "Sim" if usuario["solicita_acompanhamento"] else "Não")

    st.markdown("### Necessidades e preferências")
    st.write(
        f"- Preferência de comunicação: {usuario['preferencia_comunicacao']}\n"
        f"- Percurso sem escadas: {'Sim' if usuario['necessita_percurso_sem_escadas'] else 'Não'}\n"
        f"- Orientação de embarque: {'Sim' if usuario['prefere_orientacao_embarque'] else 'Não'}\n"
        f"- Acompanhamento: {'Sim' if usuario['solicita_acompanhamento'] else 'Não'}"
    )

    st.markdown("### Rotina e viagem")
    colA, colB = st.columns(2)
    with colA:
        st.info(f"Rotina principal: {rotina_principal['nome_rotina']}")
        st.write(f"Objetivo: {rotina_principal['objetivo']}")
        st.write(
            "Dias ativos: "
            + ", ".join(
                [
                    dia
                    for dia, ativo in {
                        "Segunda": rotina_principal["segunda"],
                        "Terça": rotina_principal["terca"],
                        "Quarta": rotina_principal["quarta"],
                        "Quinta": rotina_principal["quinta"],
                        "Sexta": rotina_principal["sexta"],
                        "Sábado": rotina_principal["sabado"],
                        "Domingo": rotina_principal["domingo"],
                    }.items()
                    if ativo
                ]
            )
        )
    with colB:
        st.success(f"Trecho selecionado: {origem_nome} → {destino_nome}")
        st.write(f"Sentido: {viagem['sentido']}")
        st.write(f"Duração planejada: {int(viagem['duracao_planejada_minutos'])} minutos")
        st.write(f"Antecedência de assistência: {int(viagem['antecedencia_assistencia_minutos'])} minutos")
        st.write(f"Assistência prevista: {'Sim' if viagem['assistencia_prevista'] else 'Não'}")

    st.markdown("### Situação operacional da Linha 7–Rubi")
    cols = st.columns(4)
    cols[0].metric("Status", format_status(ocorrencia_atual["status_operacao"]))
    cols[1].metric("Movimento", format_status(ocorrencia_atual["movimento"]))
    cols[2].metric("Hora", f"{int(ocorrencia_atual['hora']):02d}:00")
    cols[3].metric("Estações afetadas", ocorrencia_atual["estacoes_afetadas"][:25] + ("..." if len(ocorrencia_atual["estacoes_afetadas"]) > 25 else ""))

    st.warning(ocorrencia_atual["impacto_usuarios"])
    st.caption(ocorrencia_atual["descricao"])

    st.markdown("### Acessibilidade das estações")
    st.write("Origem:", origem_nome)
    if not origem_real.empty:
        origem_features = origem_real.iloc[0]
        st.json(
            {
                "banheiro acessível feminino": origem_features.get("banheiro_acessivel_feminino", ""),
                "banheiro acessível masculino": origem_features.get("banheiro_acessivel_masculino", ""),
                "banheiro acessível unissex": origem_features.get("banheiro_acessivel_unissex", ""),
                "elevador": origem_features.get("elevador", ""),
                "rampa": origem_features.get("rampa", ""),
                "piso tátil": origem_features.get("piso_tatil", ""),
                "transposição de plataformas": origem_features.get("transposicao_de_plataformas", ""),
                "telefone adaptado para PCR": origem_features.get("telefone_adaptado_pcr", ""),
            }
        )
    else:
        st.write("Dados de acessibilidade não disponíveis para esta estação no cadastro real.")

    st.write("Destino:", destino_nome)
    if not destino_real.empty:
        destino_features = destino_real.iloc[0]
        st.json(
            {
                "banheiro acessível feminino": destino_features.get("banheiro_acessivel_feminino", ""),
                "banheiro acessível masculino": destino_features.get("banheiro_acessivel_masculino", ""),
                "banheiro acessível unissex": destino_features.get("banheiro_acessivel_unissex", ""),
                "elevador": destino_features.get("elevador", ""),
                "rampa": destino_features.get("rampa", ""),
                "piso tátil": destino_features.get("piso_tatil", ""),
                "transposição de plataformas": destino_features.get("transposicao_de_plataformas", ""),
                "telefone adaptado para PCR": destino_features.get("telefone_adaptado_pcr", ""),
            }
        )
    else:
        st.write("Dados de acessibilidade não disponíveis para esta estação no cadastro real.")

    st.markdown("### Históricos do usuário")
    st.dataframe(
        todas_viagens[[
            "viagem_planejada_id",
            "sentido",
            "estacao_origem_id",
            "estacao_destino_id",
            "duracao_planejada_minutos",
            "assistencia_prevista",
        ]].assign(
            estacao_origem=lambda df: df["estacao_origem_id"].map(station_lookup),
            estacao_destino=lambda df: df["estacao_destino_id"].map(station_lookup),
        )[[
            "viagem_planejada_id",
            "sentido",
            "estacao_origem",
            "estacao_destino",
            "duracao_planejada_minutos",
            "assistencia_prevista",
        ]],
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
