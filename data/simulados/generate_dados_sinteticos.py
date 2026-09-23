from __future__ import annotations

import csv
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATIONS_PATH = ROOT / "data" / "estacoes_linha7.csv"
OUT_DIR = ROOT / "data" / "simulados"
REFERENCE_DATE = date(2026, 1, 15)


def load_station_rows() -> list[dict]:
    with STATIONS_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def normalize_station_id(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return f"EST-{slug}"


def to_iso(value: date) -> str:
    return value.isoformat()


def calculate_age(birth_date: date, reference_date: date) -> int:
    years = reference_date.year - birth_date.year
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        years -= 1
    return years


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def build_station_lookup() -> dict[str, str]:
    rows = load_station_rows()
    lookup: dict[str, str] = {}
    for index, row in enumerate(rows, start=1):
        name = row["estacao"].strip()
        lookup[name] = f"EST-{index:03d}"
    return lookup


def build_dim_estacao() -> list[dict]:
    rows = load_station_rows()
    result = []
    for index, row in enumerate(rows, start=1):
        result.append(
            {
                "estacao_id": f"EST-{index:03d}",
                "nome_estacao": row["estacao"].strip(),
                "linha": row["linha"].strip(),
                "ordem_na_linha": index,
                "fonte_url": "https://www.tictrens.com.br/linha7-rubi",
                "data_consulta": "2026-01-15",
            }
        )
    return result


def build_users() -> list[dict]:
    users = [
        {
            "usuario_id": "USR-001",
            "nome": "João Pereira",
            "idade_referencia": 34,
            "data_referencia_idade": to_iso(REFERENCE_DATE),
            "sexo": "masculino",
            "data_nascimento": "1992-03-11",
            "cpf": "CPF_TESTE_001",
            "endereco_logradouro": "Avenida Auro Soares de Moura Andrade",
            "endereco_numero": "664",
            "endereco_complemento": "Condomínio Residencial Barra Funda",
            "endereco_bairro": "Barra Funda",
            "endereco_municipio": "São Paulo",
            "endereco_uf": "SP",
            "endereco_cep": "01156-001",
            "deficiencia_informada": "visual",
            "usa_cadeira_rodas": False,
            "preferencia_comunicacao": "voz_alta",
            "necessita_percurso_sem_escadas": False,
            "prefere_orientacao_embarque": True,
            "solicita_acompanhamento": True,
            "dados_sinteticos": True,
        },
        {
            "usuario_id": "USR-002",
            "nome": "Maria Silva",
            "idade_referencia": 27,
            "data_referencia_idade": to_iso(REFERENCE_DATE),
            "sexo": "feminino",
            "data_nascimento": "1998-09-14",
            "cpf": "CPF_TESTE_002",
            "endereco_logradouro": "Rua Francisco da Cunha Menezes",
            "endereco_numero": "1066",
            "endereco_complemento": "Apartamento 42",
            "endereco_bairro": "Vila Aurora",
            "endereco_municipio": "São Paulo",
            "endereco_uf": "SP",
            "endereco_cep": "04843-020",
            "deficiencia_informada": "mobilidade",
            "usa_cadeira_rodas": True,
            "preferencia_comunicacao": "app_voz",
            "necessita_percurso_sem_escadas": True,
            "prefere_orientacao_embarque": True,
            "solicita_acompanhamento": True,
            "dados_sinteticos": True,
        },
        {
            "usuario_id": "USR-003",
            "nome": "Amanda Costa",
            "idade_referencia": 15,
            "data_referencia_idade": to_iso(REFERENCE_DATE),
            "sexo": "feminino",
            "data_nascimento": "2010-07-21",
            "cpf": "CPF_TESTE_003",
            "endereco_logradouro": "Avenida Santa Marina",
            "endereco_numero": "296",
            "endereco_complemento": "Casa 02",
            "endereco_bairro": "Água Branca",
            "endereco_municipio": "São Paulo",
            "endereco_uf": "SP",
            "endereco_cep": "02732-040",
            "deficiencia_informada": "nenhuma",
            "usa_cadeira_rodas": False,
            "preferencia_comunicacao": "app",
            "necessita_percurso_sem_escadas": False,
            "prefere_orientacao_embarque": False,
            "solicita_acompanhamento": False,
            "dados_sinteticos": True,
        },
        {
            "usuario_id": "USR-004",
            "nome": "Lucas Mendes",
            "idade_referencia": 42,
            "data_referencia_idade": to_iso(REFERENCE_DATE),
            "sexo": "masculino",
            "data_nascimento": "1984-01-08",
            "cpf": "CPF_TESTE_004",
            "endereco_logradouro": "Rua Camarões",
            "endereco_numero": "129",
            "endereco_complemento": "Bloco C, ap 31",
            "endereco_bairro": "Pirituba",
            "endereco_municipio": "São Paulo",
            "endereco_uf": "SP",
            "endereco_cep": "02913-090",
            "deficiencia_informada": "nenhuma",
            "usa_cadeira_rodas": False,
            "preferencia_comunicacao": "sms",
            "necessita_percurso_sem_escadas": False,
            "prefere_orientacao_embarque": False,
            "solicita_acompanhamento": False,
            "dados_sinteticos": True,
        },
        {
            "usuario_id": "USR-005",
            "nome": "Beatriz Nunes",
            "idade_referencia": 31,
            "data_referencia_idade": to_iso(REFERENCE_DATE),
            "sexo": "feminino",
            "data_nascimento": "1994-11-17",
            "cpf": "CPF_TESTE_005",
            "endereco_logradouro": "Rua Antonio Feres Sada",
            "endereco_numero": "88",
            "endereco_complemento": "Casa A",
            "endereco_bairro": "Várzea Paulista",
            "endereco_municipio": "São Paulo",
            "endereco_uf": "SP",
            "endereco_cep": "13220-000",
            "deficiencia_informada": "nenhuma",
            "usa_cadeira_rodas": False,
            "preferencia_comunicacao": "app",
            "necessita_percurso_sem_escadas": False,
            "prefere_orientacao_embarque": True,
            "solicita_acompanhamento": False,
            "dados_sinteticos": True,
        },
        {
            "usuario_id": "USR-006",
            "nome": "Rafael Souza",
            "idade_referencia": 29,
            "data_referencia_idade": to_iso(REFERENCE_DATE),
            "sexo": "masculino",
            "data_nascimento": "1997-05-05",
            "cpf": "CPF_TESTE_006",
            "endereco_logradouro": "Rua Felícia Pereira Pinto",
            "endereco_numero": "215",
            "endereco_complemento": "Próximo ao terminal",
            "endereco_bairro": "Campo Limpo Paulista",
            "endereco_municipio": "São Paulo",
            "endereco_uf": "SP",
            "endereco_cep": "12230-000",
            "deficiencia_informada": "mobilidade",
            "usa_cadeira_rodas": False,
            "preferencia_comunicacao": "voz_alta",
            "necessita_percurso_sem_escadas": True,
            "prefere_orientacao_embarque": True,
            "solicita_acompanhamento": True,
            "dados_sinteticos": True,
        },
    ]

    for user in users:
        birth = date.fromisoformat(user["data_nascimento"])
        user["idade_referencia"] = calculate_age(birth, REFERENCE_DATE)
    return users


def build_tempo() -> list[dict]:
    rows = [
        {"tempo_id": "TMP-0700", "horario": "07:00", "hora": 7, "minuto": 0, "periodo_dia": "manha"},
        {"tempo_id": "TMP-0730", "horario": "07:30", "hora": 7, "minuto": 30, "periodo_dia": "manha"},
        {"tempo_id": "TMP-0800", "horario": "08:00", "hora": 8, "minuto": 0, "periodo_dia": "manha"},
        {"tempo_id": "TMP-0815", "horario": "08:15", "hora": 8, "minuto": 15, "periodo_dia": "manha"},
        {"tempo_id": "TMP-0915", "horario": "09:15", "hora": 9, "minuto": 15, "periodo_dia": "manha"},
        {"tempo_id": "TMP-0930", "horario": "09:30", "hora": 9, "minuto": 30, "periodo_dia": "manha"},
        {"tempo_id": "TMP-0945", "horario": "09:45", "hora": 9, "minuto": 45, "periodo_dia": "manha"},
        {"tempo_id": "TMP-1015", "horario": "10:15", "hora": 10, "minuto": 15, "periodo_dia": "manha"},
        {"tempo_id": "TMP-1430", "horario": "14:30", "hora": 14, "minuto": 30, "periodo_dia": "tarde"},
        {"tempo_id": "TMP-1800", "horario": "18:00", "hora": 18, "minuto": 0, "periodo_dia": "tarde"},
        {"tempo_id": "TMP-1820", "horario": "18:20", "hora": 18, "minuto": 20, "periodo_dia": "tarde"},
        {"tempo_id": "TMP-1900", "horario": "19:00", "hora": 19, "minuto": 0, "periodo_dia": "noite"},
        {"tempo_id": "TMP-1930", "horario": "19:30", "hora": 19, "minuto": 30, "periodo_dia": "noite"},
        {"tempo_id": "TMP-2000", "horario": "20:00", "hora": 20, "minuto": 0, "periodo_dia": "noite"},
    ]
    return rows


def build_ocorrencias_horarias() -> list[dict]:
    ocorrencias = []
    for hora in range(24):
        if hora < 4 or hora >= 24:
            status = "fechado"
            movimento = "sem_servico"
            estacoes = "toda a linha"
            descricao = "Linha 7-Rubi sem operação e sem demanda de passageiros em estação."
            impacto = "usuários devem reagendar a viagem e evitar deslocamento." 
        elif 4 <= hora < 6:
            status = "operacao_inicial"
            movimento = "baixo"
            estacoes = "toda a linha"
            descricao = "Operação inicial com trens esparsos e baixa demanda antes dos horários de pico."
            impacto = "Passageiros com rotina muito cedo podem encontrar trens menos frequentes." 
        elif 6 <= hora <= 8:
            status = "normal"
            movimento = "alto"
            estacoes = "Palmeiras-Barra Funda; Lapa; Pirituba; Jundiaí"
            descricao = "Horário de pico com maior concentração de passageiros e trens mais cheios."
            impacto = "A demanda aumenta em origem e destino dos deslocamentos de trabalho e estudo." 
        elif 9 <= hora <= 12:
            status = "normal"
            movimento = "baixo"
            estacoes = "toda a linha"
            descricao = "Serviço funcionando em operação normal com menor movimento e viagens mais previsíveis."
            impacto = "Muitas rotinas de trabalho e estudo já estão em andamento, mas a linha segue estável." 
        elif hora == 13:
            status = "restricao_operacional"
            movimento = "moderado"
            estacoes = "Vila Aurora; Perus; Caieiras"
            descricao = "Queda de energia em estações selecionadas aumenta o tempo de embarque e exige atenção às informações da operação."
            impacto = "Usuários com rotina de almoço ou deslocamento intermediante podem sofrer atrasos e necessidade de apoio extra."
        elif 14 <= hora <= 15:
            status = "normal"
            movimento = "moderado"
            estacoes = "toda a linha"
            descricao = "Recuperação do serviço e movimentação moderada, com ajuste do fluxo de passageiros."
            impacto = "A operação volta a ficar previsível, mas ainda há necessidade de atenção em estações centrais."
        elif 16 <= hora <= 18:
            status = "normal"
            movimento = "alto"
            estacoes = "Palmeiras-Barra Funda; Lapa; Água Branca; Várzea Paulista"
            descricao = "Pico vespertino com maior densidade de passageiros e filas maiores nas estações mais centrais."
            impacto = "A linha fica mais intensa para quem trabalha no fim do expediente ou retorna para casa." 
        elif 19 <= hora <= 21:
            status = "normal"
            movimento = "moderado"
            estacoes = "toda a linha"
            descricao = "Operação normal com movimento reduzido em comparação ao pico, mas ainda frequente."
            impacto = "Usuários de lazer e retorno doméstico ainda encontram trens em uso contínuo." 
        elif 22 <= hora <= 23:
            status = "normal"
            movimento = "baixo"
            estacoes = "toda a linha"
            descricao = "Horário final de operação com baixa demanda e acabamento do serviço diário."
            impacto = "Rota de retorno doméstico torna-se mais tranquila, mas o último trem deve ser considerado." 
        else:
            status = "normal"
            movimento = "baixo"
            estacoes = "toda a linha"
            descricao = "Operação normal."
            impacto = "Sem impacto relevante para a rotina planejada."

        ocorrencias.append(
            {
                "ocorrencia_id": f"OC-{hora:02d}",
                "data": "2026-09-01",
                "hora": hora,
                "horario": f"{hora:02d}:00",
                "status_operacao": status,
                "movimento": movimento,
                "estacoes_afetadas": estacoes,
                "descricao": descricao,
                "impacto_usuarios": impacto,
                "dados_sinteticos": True,
            }
        )
    return ocorrencias


def build_rotinas() -> list[dict]:
    return [
        {
            "rotina_id": "ROT-001",
            "nome_rotina": "Trabalho principal - Maria",
            "objetivo": "trabalho",
            "segunda": True,
            "terca": True,
            "quarta": True,
            "quinta": True,
            "sexta": True,
            "sabado": False,
            "domingo": False,
            "ativa": True,
            "dados_sinteticos": True,
        },
        {
            "rotina_id": "ROT-002",
            "nome_rotina": "Lazer fim de semana - Maria",
            "objetivo": "lazer",
            "segunda": False,
            "terca": False,
            "quarta": False,
            "quinta": False,
            "sexta": False,
            "sabado": True,
            "domingo": True,
            "ativa": True,
            "dados_sinteticos": True,
        },
        {
            "rotina_id": "ROT-003",
            "nome_rotina": "Estudo principal - Amanda",
            "objetivo": "estudo",
            "segunda": True,
            "terca": True,
            "quarta": True,
            "quinta": True,
            "sexta": True,
            "sabado": False,
            "domingo": False,
            "ativa": True,
            "dados_sinteticos": True,
        },
        {
            "rotina_id": "ROT-004",
            "nome_rotina": "Encontro e lazer - Amanda",
            "objetivo": "lazer",
            "segunda": False,
            "terca": False,
            "quarta": False,
            "quinta": False,
            "sexta": True,
            "sabado": True,
            "domingo": False,
            "ativa": True,
            "dados_sinteticos": True,
        },
        {
            "rotina_id": "ROT-005",
            "nome_rotina": "Visita pontual - João",
            "objetivo": "compromisso_pessoal",
            "segunda": False,
            "terca": False,
            "quarta": False,
            "quinta": False,
            "sexta": False,
            "sabado": True,
            "domingo": False,
            "ativa": True,
            "dados_sinteticos": True,
        },
        {
            "rotina_id": "ROT-006",
            "nome_rotina": "Trabalho de segunda a sexta - Lucas",
            "objetivo": "trabalho",
            "segunda": True,
            "terca": True,
            "quarta": True,
            "quinta": True,
            "sexta": True,
            "sabado": False,
            "domingo": False,
            "ativa": True,
            "dados_sinteticos": True,
        },
        {
            "rotina_id": "ROT-007",
            "nome_rotina": "Treino e encontro - Beatriz",
            "objetivo": "lazer",
            "segunda": False,
            "terca": False,
            "quarta": False,
            "quinta": True,
            "sexta": True,
            "sabado": True,
            "domingo": False,
            "ativa": True,
            "dados_sinteticos": True,
        },
        {
            "rotina_id": "ROT-008",
            "nome_rotina": "Consulta periódica - Rafael",
            "objetivo": "compromisso_pessoal",
            "segunda": True,
            "terca": False,
            "quarta": True,
            "quinta": False,
            "sexta": True,
            "sabado": False,
            "domingo": False,
            "ativa": True,
            "dados_sinteticos": True,
        },
    ]


def build_fact_rows(station_lookup: dict[str, str]) -> list[dict]:
    rows = [
        {
            "viagem_planejada_id": "VP-001",
            "usuario_id": "USR-002",
            "rotina_id": "ROT-001",
            "sentido": "ida",
            "estacao_origem_id": station_lookup["Jundiaí"],
            "estacao_destino_id": station_lookup["Palmeiras-Barra Funda"],
            "tempo_saida_id": "TMP-0915",
            "tempo_chegada_id": "TMP-1015",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 60,
            "antecedencia_assistencia_minutos": 20,
            "assistencia_prevista": True,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-002",
            "usuario_id": "USR-002",
            "rotina_id": "ROT-001",
            "sentido": "volta",
            "estacao_origem_id": station_lookup["Palmeiras-Barra Funda"],
            "estacao_destino_id": station_lookup["Jundiaí"],
            "tempo_saida_id": "TMP-1820",
            "tempo_chegada_id": "TMP-1900",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 40,
            "antecedencia_assistencia_minutos": 25,
            "assistencia_prevista": True,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-003",
            "usuario_id": "USR-002",
            "rotina_id": "ROT-002",
            "sentido": "ida",
            "estacao_origem_id": station_lookup["Várzea Paulista"],
            "estacao_destino_id": station_lookup["Lapa"],
            "tempo_saida_id": "TMP-0800",
            "tempo_chegada_id": "TMP-0815",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 15,
            "antecedencia_assistencia_minutos": 20,
            "assistencia_prevista": True,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-004",
            "usuario_id": "USR-002",
            "rotina_id": "ROT-002",
            "sentido": "volta",
            "estacao_origem_id": station_lookup["Lapa"],
            "estacao_destino_id": station_lookup["Várzea Paulista"],
            "tempo_saida_id": "TMP-1930",
            "tempo_chegada_id": "TMP-2000",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 30,
            "antecedencia_assistencia_minutos": 20,
            "assistencia_prevista": True,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-005",
            "usuario_id": "USR-003",
            "rotina_id": "ROT-003",
            "sentido": "ida",
            "estacao_origem_id": station_lookup["Caieiras"],
            "estacao_destino_id": station_lookup["Palmeiras-Barra Funda"],
            "tempo_saida_id": "TMP-0700",
            "tempo_chegada_id": "TMP-0730",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 30,
            "antecedencia_assistencia_minutos": 0,
            "assistencia_prevista": False,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-006",
            "usuario_id": "USR-003",
            "rotina_id": "ROT-003",
            "sentido": "volta",
            "estacao_origem_id": station_lookup["Palmeiras-Barra Funda"],
            "estacao_destino_id": station_lookup["Caieiras"],
            "tempo_saida_id": "TMP-1430",
            "tempo_chegada_id": "TMP-1800",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 210,
            "antecedencia_assistencia_minutos": 0,
            "assistencia_prevista": False,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-007",
            "usuario_id": "USR-003",
            "rotina_id": "ROT-004",
            "sentido": "ida",
            "estacao_origem_id": station_lookup["Perus"],
            "estacao_destino_id": station_lookup["Vila Aurora"],
            "tempo_saida_id": "TMP-1800",
            "tempo_chegada_id": "TMP-1900",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 60,
            "antecedencia_assistencia_minutos": 0,
            "assistencia_prevista": False,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-008",
            "usuario_id": "USR-003",
            "rotina_id": "ROT-004",
            "sentido": "volta",
            "estacao_origem_id": station_lookup["Vila Aurora"],
            "estacao_destino_id": station_lookup["Perus"],
            "tempo_saida_id": "TMP-1930",
            "tempo_chegada_id": "TMP-2000",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 30,
            "antecedencia_assistencia_minutos": 0,
            "assistencia_prevista": False,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-009",
            "usuario_id": "USR-001",
            "rotina_id": "ROT-005",
            "sentido": "ida",
            "estacao_origem_id": station_lookup["Lapa"],
            "estacao_destino_id": station_lookup["Palmeiras-Barra Funda"],
            "tempo_saida_id": "TMP-0800",
            "tempo_chegada_id": "TMP-0815",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 15,
            "antecedencia_assistencia_minutos": 15,
            "assistencia_prevista": True,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-010",
            "usuario_id": "USR-001",
            "rotina_id": "ROT-005",
            "sentido": "volta",
            "estacao_origem_id": station_lookup["Palmeiras-Barra Funda"],
            "estacao_destino_id": station_lookup["Lapa"],
            "tempo_saida_id": "TMP-1900",
            "tempo_chegada_id": "TMP-1930",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 30,
            "antecedencia_assistencia_minutos": 15,
            "assistencia_prevista": True,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-011",
            "usuario_id": "USR-004",
            "rotina_id": "ROT-006",
            "sentido": "ida",
            "estacao_origem_id": station_lookup["Pirituba"],
            "estacao_destino_id": station_lookup["Palmeiras-Barra Funda"],
            "tempo_saida_id": "TMP-0700",
            "tempo_chegada_id": "TMP-0730",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 30,
            "antecedencia_assistencia_minutos": 0,
            "assistencia_prevista": False,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-012",
            "usuario_id": "USR-004",
            "rotina_id": "ROT-006",
            "sentido": "volta",
            "estacao_origem_id": station_lookup["Palmeiras-Barra Funda"],
            "estacao_destino_id": station_lookup["Pirituba"],
            "tempo_saida_id": "TMP-1800",
            "tempo_chegada_id": "TMP-1830",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 30,
            "antecedencia_assistencia_minutos": 0,
            "assistencia_prevista": False,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-013",
            "usuario_id": "USR-005",
            "rotina_id": "ROT-007",
            "sentido": "ida",
            "estacao_origem_id": station_lookup["Vila Clarice"],
            "estacao_destino_id": station_lookup["Água Branca"],
            "tempo_saida_id": "TMP-0800",
            "tempo_chegada_id": "TMP-0945",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 105,
            "antecedencia_assistencia_minutos": 0,
            "assistencia_prevista": False,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-014",
            "usuario_id": "USR-005",
            "rotina_id": "ROT-007",
            "sentido": "volta",
            "estacao_origem_id": station_lookup["Água Branca"],
            "estacao_destino_id": station_lookup["Vila Clarice"],
            "tempo_saida_id": "TMP-1930",
            "tempo_chegada_id": "TMP-2000",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 30,
            "antecedencia_assistencia_minutos": 0,
            "assistencia_prevista": False,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-015",
            "usuario_id": "USR-006",
            "rotina_id": "ROT-008",
            "sentido": "ida",
            "estacao_origem_id": station_lookup["Botujuru"],
            "estacao_destino_id": station_lookup["Várzea Paulista"],
            "tempo_saida_id": "TMP-0815",
            "tempo_chegada_id": "TMP-0915",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 60,
            "antecedencia_assistencia_minutos": 15,
            "assistencia_prevista": True,
            "dados_sinteticos": True,
        },
        {
            "viagem_planejada_id": "VP-016",
            "usuario_id": "USR-006",
            "rotina_id": "ROT-008",
            "sentido": "volta",
            "estacao_origem_id": station_lookup["Várzea Paulista"],
            "estacao_destino_id": station_lookup["Botujuru"],
            "tempo_saida_id": "TMP-1800",
            "tempo_chegada_id": "TMP-1900",
            "chegada_dia_offset": 0,
            "duracao_planejada_minutos": 60,
            "antecedencia_assistencia_minutos": 20,
            "assistencia_prevista": True,
            "dados_sinteticos": True,
        },
    ]
    return rows


def validate_data() -> None:
    users = build_users()
    rotinas = build_rotinas()
    tempo = build_tempo()
    estacoes = build_dim_estacao()
    station_lookup = build_station_lookup()
    rows = build_fact_rows(station_lookup)

    ocorrencias = build_ocorrencias_horarias()
    assert len(ocorrencias) == 24, "Deve haver exatamente 24 registros horários."
    assert {item["data"] for item in ocorrencias} == {"2026-09-01"}
    assert ocorrencias[0]["hora"] == 0 and ocorrencias[-1]["hora"] == 23
    assert ocorrencias[0]["status_operacao"] == "fechado"
    assert ocorrencias[4]["status_operacao"] == "operacao_inicial"
    assert ocorrencias[13]["status_operacao"] == "restricao_operacional"
    assert any(item["status_operacao"] == "normal" for item in ocorrencias)

    assert len(users) == 6, "Deve haver exatamente seis usuários nesta massa inicial."
    assert {user["nome"] for user in users} == {"João Pereira", "Maria Silva", "Amanda Costa", "Lucas Mendes", "Beatriz Nunes", "Rafael Souza"}, "Nomes esperados inconsistentes."

    user_ids = {user["usuario_id"] for user in users}
    assert len(user_ids) == len(users)

    cpf_values = [u["cpf"] for u in users]
    assert len(set(cpf_values)) == 6
    assert all(isinstance(value, str) and value.startswith("CPF_TESTE_") for value in cpf_values)

    for user in users:
        birth = date.fromisoformat(user["data_nascimento"])
        calculated = calculate_age(birth, REFERENCE_DATE)
        assert user["idade_referencia"] == calculated, f"Idade inconsistente para {user['nome']}"

    assert len(rotinas) == 8
    for rotina in rotinas:
        assert any([rotina["segunda"], rotina["terca"], rotina["quarta"], rotina["quinta"], rotina["sexta"], rotina["sabado"], rotina["domingo"]])
        assert rotina["ativa"] is True

    by_rotina: dict[str, list[dict]] = {}
    for row in rows:
        by_rotina.setdefault(row["rotina_id"], []).append(row)

    for rotina_id, list_rows in by_rotina.items():
        assert len(list_rows) == 2, f"Rotina {rotina_id} deve ter exatamente dois trechos."
        sentidos = {r["sentido"] for r in list_rows}
        assert sentidos == {"ida", "volta"}
        origem_ida = next(r["estacao_origem_id"] for r in list_rows if r["sentido"] == "ida")
        destino_ida = next(r["estacao_destino_id"] for r in list_rows if r["sentido"] == "ida")
        origem_volta = next(r["estacao_origem_id"] for r in list_rows if r["sentido"] == "volta")
        destino_volta = next(r["estacao_destino_id"] for r in list_rows if r["sentido"] == "volta")
        assert origem_volta == destino_ida
        assert destino_volta == origem_ida

        ida = next(r for r in list_rows if r["sentido"] == "ida")
        volta = next(r for r in list_rows if r["sentido"] == "volta")
        assert ida["tempo_chegada_id"] in {t["tempo_id"] for t in tempo}
        assert volta["tempo_saida_id"] in {t["tempo_id"] for t in tempo}
        assert ida["tempo_chegada_id"] != volta["tempo_saida_id"]

        ida_hora = next(t["horario"] for t in tempo if t["tempo_id"] == ida["tempo_chegada_id"])
        volta_hora = next(t["horario"] for t in tempo if t["tempo_id"] == volta["tempo_saida_id"])
        assert datetime.strptime(volta_hora, "%H:%M") >= datetime.strptime(ida_hora, "%H:%M")
        assert ida["duracao_planejada_minutos"] > 0
        assert volta["duracao_planejada_minutos"] > 0

    assert len(rows) == 16, "Deve haver exatamente 16 trechos planejados."
    assert len({r["usuario_id"] for r in rows}) == 6
    assert len({r["rotina_id"] for r in rows}) == 8

    valid_stations = {item["estacao_id"] for item in estacoes}
    for row in rows:
        assert row["estacao_origem_id"] in valid_stations
        assert row["estacao_destino_id"] in valid_stations
        assert row["estacao_origem_id"] != row["estacao_destino_id"]
        assert row["dados_sinteticos"] is True
        assert row["assistencia_prevista"] in {True, False}

    assert all(not row["assistencia_prevista"] or row["antecedencia_assistencia_minutos"] > 0 for row in rows)
    assert sum(1 for row in rows if row["assistencia_prevista"]) >= 1
    assert len(estacoes) >= 1

    print("Validação concluída com sucesso: 6 usuários, 8 rotinas, 16 trechos planejados e dimensão de estações real integrada.")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    station_lookup = build_station_lookup()

    users = build_users()
    rotinas = build_rotinas()
    tempo = build_tempo()
    estacoes = build_dim_estacao()
    ocorrencias = build_ocorrencias_horarias()
    fact_rows = build_fact_rows(station_lookup)

    write_csv(
        OUT_DIR / "dim_estacao.csv",
        estacoes,
        ["estacao_id", "nome_estacao", "linha", "ordem_na_linha", "fonte_url", "data_consulta"],
    )

    write_csv(
        OUT_DIR / "dim_usuario.csv",
        users,
        [
            "usuario_id",
            "nome",
            "idade_referencia",
            "data_referencia_idade",
            "sexo",
            "data_nascimento",
            "cpf",
            "endereco_logradouro",
            "endereco_numero",
            "endereco_complemento",
            "endereco_bairro",
            "endereco_municipio",
            "endereco_uf",
            "endereco_cep",
            "deficiencia_informada",
            "usa_cadeira_rodas",
            "preferencia_comunicacao",
            "necessita_percurso_sem_escadas",
            "prefere_orientacao_embarque",
            "solicita_acompanhamento",
            "dados_sinteticos",
        ],
    )

    write_csv(
        OUT_DIR / "dim_tempo.csv",
        tempo,
        ["tempo_id", "horario", "hora", "minuto", "periodo_dia"],
    )

    write_csv(
        OUT_DIR / "dim_rotina.csv",
        rotinas,
        [
            "rotina_id",
            "nome_rotina",
            "objetivo",
            "segunda",
            "terca",
            "quarta",
            "quinta",
            "sexta",
            "sabado",
            "domingo",
            "ativa",
            "dados_sinteticos",
        ],
    )

    write_csv(
        OUT_DIR / "dim_ocorrencia.csv",
        ocorrencias,
        [
            "ocorrencia_id",
            "data",
            "hora",
            "horario",
            "status_operacao",
            "movimento",
            "estacoes_afetadas",
            "descricao",
            "impacto_usuarios",
            "dados_sinteticos",
        ],
    )

    write_csv(
        OUT_DIR / "fato_viagem_planejada.csv",
        fact_rows,
        [
            "viagem_planejada_id",
            "usuario_id",
            "rotina_id",
            "sentido",
            "estacao_origem_id",
            "estacao_destino_id",
            "tempo_saida_id",
            "tempo_chegada_id",
            "chegada_dia_offset",
            "duracao_planejada_minutos",
            "antecedencia_assistencia_minutos",
            "assistencia_prevista",
            "dados_sinteticos",
        ],
    )

    validate_data()
    print(f"Arquivos gerados em: {OUT_DIR}")


if __name__ == "__main__":
    main()
