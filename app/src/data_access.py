"""Leitura do cadastro e das tabelas sintéticas usadas pelo protótipo."""
from pathlib import Path
import unicodedata

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
BOOL_FIELDS = (
    "usa_cadeira_rodas", "necessita_percurso_sem_escadas",
    "prefere_orientacao_embarque", "solicita_acompanhamento", "dados_sinteticos",
)
DAYS = {"segunda": "Seg", "terca": "Ter", "quarta": "Qua", "quinta": "Qui",
        "sexta": "Sex", "sabado": "Sáb", "domingo": "Dom"}


def normalize(value):
    text = unicodedata.normalize("NFKD", str(value).strip().casefold())
    return " ".join("".join(c for c in text if not unicodedata.combining(c)).split())


def as_bool(value):
    return normalize(value) in {"true", "1", "sim"}


def read_table(path, required):
    frame = pd.read_csv(path, sep=";", dtype=str, keep_default_na=False,
                        encoding="utf-8-sig")
    frame.columns = frame.columns.str.strip()
    missing = set(required) - set(frame.columns)
    if missing:
        raise ValueError(f"{path.name}: faltam os campos {', '.join(sorted(missing))}.")
    return frame


def load_data(root=ROOT):
    root = Path(root)
    folder = root / "data" / "simulados"
    users = read_table(folder / "dim_usuario.csv", ["usuario_id", "nome", "dados_sinteticos"])
    for field in BOOL_FIELDS:
        users[field] = users[field].map(as_bool)
    users = users.loc[users.dados_sinteticos].to_dict("records")
    stations = read_table(folder / "dim_estacao.csv", ["estacao_id", "ordem_na_linha", "nome_estacao"])
    stations["ordem_na_linha"] = pd.to_numeric(stations.ordem_na_linha, errors="raise")
    stations = stations.sort_values("ordem_na_linha").to_dict("records")
    static = read_table(root / "data" / "estacoes_linha7.csv", ["estacao"])
    static_by_name = {normalize(r["estacao"]): r for r in static.to_dict("records")}
    for station in stations:
        station["recursos"] = static_by_name.get(normalize(station["nome_estacao"]), {})
    occurrences = read_table(folder / "dim_ocorrencia.csv",
                            ["hora", "status_operacao", "movimento", "dados_sinteticos"])
    occurrences = occurrences.loc[occurrences.dados_sinteticos.map(as_bool)].copy()
    occurrences["hora"] = pd.to_numeric(occurrences.hora, errors="raise").astype(int)
    if set(occurrences.hora) != set(range(24)) or len(occurrences) != 24:
        raise ValueError("A demonstração precisa de uma ocorrência para cada hora, de 0 a 23.")
    times = read_table(folder / "dim_tempo.csv", ["tempo_id", "horario"])
    routines = read_table(folder / "dim_rotina.csv", ["rotina_id", "nome_rotina"])
    trips = read_table(folder / "fato_viagem_planejada.csv",
                      ["usuario_id", "rotina_id", "sentido", "tempo_saida_id", "tempo_chegada_id"])
    time_map = dict(zip(times.tempo_id, times.horario))
    station_ids = {s["estacao_id"] for s in stations}
    for trip in trips.to_dict("records"):
        if any(trip[f] not in time_map for f in ("tempo_saida_id", "tempo_chegada_id")):
            raise ValueError("Há um horário de viagem sem registro em dim_tempo.csv.")
        if any(trip[f] not in station_ids for f in ("estacao_origem_id", "estacao_destino_id")):
            raise ValueError("Há uma viagem fora do cadastro de estações.")
    return {"users": users, "stations": stations,
            "occurrences": {r["hora"]: r for r in occurrences.to_dict("records")},
            "times": time_map, "routines": routines.to_dict("records"),
            "trips": trips.to_dict("records")}


def user_routines(data, user_id):
    result = []
    for routine in data["routines"]:
        legs = [r for r in data["trips"] if r["usuario_id"] == user_id
                and r["rotina_id"] == routine["rotina_id"]]
        if not legs or not as_bool(routine.get("ativa")):
            continue
        item = dict(routine)
        item["days"] = [label for field, label in DAYS.items() if as_bool(item.get(field))]
        item["legs"] = {leg["sentido"]: {
            "origin": leg["estacao_origem_id"], "destination": leg["estacao_destino_id"],
            "departure": data["times"][leg["tempo_saida_id"]],
            "arrival": data["times"][leg["tempo_chegada_id"]],
            "direction": leg["sentido"], "routine_id": item["rotina_id"],
            "name": item["nome_rotina"],
        } for leg in legs}
        result.append(item)
    return result
