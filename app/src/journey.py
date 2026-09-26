"""Regras determinísticas de percurso, cenários e assistência fictícia."""
from copy import deepcopy

from data_access import as_bool, normalize

SCENARIOS = {
    "tranquilo": {"label": "Viagem tranquila", "hour": 10, "note": "10h · baixo movimento"},
    "moderado": {"label": "Movimento moderado", "hour": 14, "note": "14h · sem ocorrência"},
    "pico": {"label": "Horário de pico", "hour": 7, "note": "7h · alto movimento"},
    "ocorrencia": {"label": "Pico com ocorrência", "hour": 7, "note": "7h · restrição no percurso"},
    "horario": {"label": "Escolher horário", "hour": None, "note": "Explore as 24 horas"},
}
SUPPORT_OPTIONS = ["Orientação na estação", "Apoio no embarque e desembarque",
                   "Percurso sem escadas", "Acompanhamento durante a passagem pela estação"]


def route_stations(stations, origin, destination):
    ordered = sorted(stations, key=lambda s: int(s["ordem_na_linha"]))
    ids = [s["estacao_id"] for s in ordered]
    if origin not in ids or destination not in ids:
        raise ValueError("Escolha estações do cadastro da Linha 7–Rubi.")
    if origin == destination:
        raise ValueError("Escolha uma origem diferente do destino.")
    a, b = ids.index(origin), ids.index(destination)
    return ordered[a:b+1] if a < b else list(reversed(ordered[b:a+1]))


def scenario_for(occurrences, mode, manual_hour=10):
    if mode not in SCENARIOS:
        raise ValueError("Cenário desconhecido.")
    hour = manual_hour if mode == "horario" else SCENARIOS[mode]["hour"]
    if hour not in occurrences:
        raise ValueError("Horário fora da demonstração.")
    base_hour = 13 if mode == "ocorrencia" else hour
    item = deepcopy(occurrences[base_hour])
    item.update(hora=hour, horario=f"{hour:02d}:00", mode=mode)
    if mode == "ocorrencia":
        # Sobreposição da ocorrência existente das 13h ao pico das 7h.
        # Não cria nem afirma falha de elevador: o cadastro não confirma esse equipamento.
        item["movimento"] = "alto"
    item["context_id"] = f"{mode}:{hour}"
    item["closed"] = item["status_operacao"] == "fechado"
    item["incident"] = item["status_operacao"] == "restricao_operacional"
    return item


def affected_on_route(route, scenario):
    if not scenario["incident"]:
        return []
    raw = normalize(scenario.get("estacoes_afetadas", ""))
    names = {normalize(n) for n in raw.split(";")}
    return [s for s in route if raw == "toda a linha" or normalize(s["nome_estacao"]) in names]


def route_insights(user, route, scenario):
    """Cada aviso tem título, explicação e ação; nunca certifica acesso ou funcionamento."""
    items = []
    affected = affected_on_route(route, scenario)
    if scenario["closed"]:
        items.append(("error", "Sem operação neste horário",
                      "Neste cenário a linha está fechada. Escolha outro horário para simular a viagem e solicitar apoio."))
    elif affected:
        names = ", ".join(s["nome_estacao"] for s in affected)
        items.append(("warning", "Uma ocorrência afeta seu percurso",
                      f"Restrição operacional simulada em {names}. O embarque pode demorar; solicite orientação antes de sair."))
    elif scenario["incident"]:
        items.append(("info", "Ocorrência em outro trecho",
                      "A ocorrência simulada não está entre sua origem e seu destino. Isso não confirma ausência de reflexos na linha."))
    if not scenario["closed"] and scenario["movimento"] == "alto":
        message = "Considere mais tempo para circular e embarcar. O movimento exibido é uma simulação."
        if user.get("prefere_orientacao_embarque") or user.get("solicita_acompanhamento"):
            message = "Seu perfil pede orientação. Combine um ponto de encontro para facilitar o embarque em meio ao movimento."
        items.append(("warning", "Movimento alto", message))
    if user.get("necessita_percurso_sem_escadas"):
        endpoints = [route[0], route[-1]]
        incomplete = [s["nome_estacao"] for s in endpoints
                      if not any(as_bool(s["recursos"].get(k)) for k in ("rampa", "elevador"))]
        message = (f"O cadastro não informa rampa ou elevador em {', '.join(incomplete)}. " if incomplete
                   else "Há rampas publicadas para as estações de embarque e desembarque. ")
        message += "É preciso confirmar o acesso entre rua, plataforma e trem com a equipe."
        items.append(("warning" if incomplete else "info", "Você prefere um percurso sem escadas", message))
    if user.get("prefere_orientacao_embarque") and normalize(user.get("deficiencia_informada")) == "visual":
        missing = [s["nome_estacao"] for s in (route[0], route[-1])
                   if not as_bool(s["recursos"].get("piso_tatil"))]
        if missing:
            items.append(("info", "Orientação pode ajudar neste trajeto",
                          f"Piso tátil não consta no cadastro de {', '.join(missing)}. Você pode pedir acompanhamento na estação."))
    return items


def preferred_support(user):
    selected = []
    if user.get("prefere_orientacao_embarque"):
        selected += SUPPORT_OPTIONS[:2]
    if user.get("necessita_percurso_sem_escadas"):
        selected.append(SUPPORT_OPTIONS[2])
    if user.get("solicita_acompanhamento"):
        selected.append(SUPPORT_OPTIONS[3])
    return selected


def request_context(user, trip, scenario):
    return (user["usuario_id"], trip["origin"], trip["destination"], scenario["context_id"])


def create_request(user, trip, scenario, support, sequence, previous=None, note=""):
    if scenario["closed"]:
        raise ValueError("Escolha um horário com operação para solicitar assistência.")
    if not support or any(value not in SUPPORT_OPTIONS for value in support):
        raise ValueError("Selecione pelo menos um tipo de apoio.")
    context = request_context(user, trip, scenario)
    if previous and previous["context"] == context and previous["status"] in {"pendente", "confirmado"}:
        return previous
    return {"id": f"DEMO-{sequence:03d}", "context": context, "status": "pendente",
            "support": list(support), "note": note.strip()[:240],
            "origin": trip["origin"], "destination": trip["destination"],
            "hour": scenario["horario"], "staff": None, "meeting": None,
            "history": ["Pedido enviado"]}


def transition_request(request, action):
    if request is None:
        raise ValueError("Envie um pedido antes de avançar o atendimento.")
    transitions = {("pendente", "confirmar"): "confirmado",
                   ("confirmado", "concluir"): "concluido",
                   ("pendente", "cancelar"): "cancelado",
                   ("confirmado", "cancelar"): "cancelado"}
    status = transitions.get((request["status"], action))
    if status is None:
        raise ValueError("Essa ação não está disponível no estado atual do pedido.")
    result = deepcopy(request)
    result["status"] = status
    result["history"].append({"confirmado": "Equipe designada", "concluido": "Atendimento concluído",
                              "cancelado": "Pedido cancelado"}[status])
    if status == "confirmado":
        result["staff"] = "Ana · equipe de apoio fictícia"
        result["meeting"] = "Entrada principal da estação de origem · ponto ilustrativo"
    return result
