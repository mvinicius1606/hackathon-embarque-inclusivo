"""Regressões dos comportamentos que sustentam a demonstração."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "src"))

from data_access import as_bool, load_data, user_routines
from journey import (SCENARIOS, SUPPORT_OPTIONS, route_stations, scenario_for,
                     affected_on_route, route_insights, create_request, transition_request)


class JourneyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_data()
        cls.maria = cls.data["users"][1]
        cls.trip = user_routines(cls.data, cls.maria["usuario_id"])[0]["legs"]["ida"]

    def test_csv_booleans_and_all_routines_load(self):
        self.assertFalse(as_bool("False"))
        self.assertFalse(self.data["users"][2]["usa_cadeira_rodas"])
        self.assertTrue(self.maria["usa_cadeira_rodas"])
        routines = [r for u in self.data["users"] for r in user_routines(self.data, u["usuario_id"])]
        self.assertEqual(len(routines), 8)
        for r in routines:
            self.assertEqual(r["legs"]["ida"]["origin"], r["legs"]["volta"]["destination"])
            self.assertEqual(r["legs"]["ida"]["destination"], r["legs"]["volta"]["origin"])
            self.assertTrue(r["legs"]["ida"]["departure"])
            self.assertTrue(r["legs"]["volta"]["arrival"])

    def test_route_order_and_invalid_routes(self):
        stations = self.data["stations"]
        forward = route_stations(stations, "EST-001", "EST-017")
        backward = route_stations(stations, "EST-017", "EST-001")
        self.assertEqual(forward, list(reversed(backward)))
        self.assertEqual(len(forward), 17)
        for destination in ("EST-001", "EST-INVALIDA"):
            with self.assertRaises(ValueError):
                route_stations(stations, "EST-001", destination)

    def test_four_scenarios_and_24_hours(self):
        scenarios = {key: scenario_for(self.data["occurrences"], key) for key in SCENARIOS}
        self.assertEqual([scenarios[k]["movimento"] for k in list(SCENARIOS)[:4]],
                         ["baixo", "moderado", "alto", "alto"])
        self.assertFalse(scenarios["pico"]["incident"])
        self.assertTrue(scenarios["ocorrencia"]["incident"])
        self.assertEqual(scenarios["pico"]["hora"], scenarios["ocorrencia"]["hora"])
        self.assertEqual(self.data["occurrences"][13]["hora"], 13)
        for hour in range(24):
            s = scenario_for(self.data["occurrences"], "horario", hour)
            self.assertEqual(s["closed"], hour < 4)

    def test_incident_only_marks_stations_on_route(self):
        scenario = scenario_for(self.data["occurrences"], "ocorrencia")
        route = route_stations(self.data["stations"], self.trip["origin"], self.trip["destination"])
        self.assertEqual({s["nome_estacao"] for s in affected_on_route(route, scenario)},
                         {"Vila Aurora", "Perus", "Caieiras"})
        short_route = route_stations(self.data["stations"], "EST-001", "EST-003")
        self.assertEqual(affected_on_route(short_route, scenario), [])
        self.assertIn("Ocorrência em outro trecho", [n[1] for n in route_insights(self.maria, short_route, scenario)])

    def test_missing_accessibility_is_unknown(self):
        route = [{"estacao_id": "a", "nome_estacao": "Origem", "recursos": {}},
                 {"estacao_id": "b", "nome_estacao": "Destino", "recursos": {}}]
        scenario = scenario_for(self.data["occurrences"], "tranquilo")
        notes = route_insights(self.maria, route, scenario)
        self.assertTrue(any("não informa rampa ou elevador" in n[2] for n in notes))

    def test_support_lifecycle_deduplication_and_no_diagnosis_gate(self):
        amanda = self.data["users"][2]
        scenario = scenario_for(self.data["occurrences"], "tranquilo")
        request = create_request(amanda, self.trip, scenario, [SUPPORT_OPTIONS[0]], 1)
        self.assertEqual(request["status"], "pendente")
        self.assertIsNone(request["staff"])
        self.assertIsNone(request["meeting"])
        self.assertEqual(create_request(amanda, self.trip, scenario, [SUPPORT_OPTIONS[0]], 2, request)["id"], "DEMO-001")
        with self.assertRaises(ValueError):
            transition_request(request, "concluir")
        confirmed = transition_request(request, "confirmar")
        self.assertEqual(confirmed["status"], "confirmado")
        self.assertIn("fictícia", confirmed["staff"])
        self.assertEqual(request["status"], "pendente")
        self.assertEqual(transition_request(confirmed, "concluir")["status"], "concluido")
        self.assertEqual(transition_request(confirmed, "cancelar")["status"], "cancelado")

    def test_closed_and_empty_support_cannot_create_request(self):
        closed = scenario_for(self.data["occurrences"], "horario", 2)
        with self.assertRaises(ValueError):
            create_request(self.maria, self.trip, closed, SUPPORT_OPTIONS, 1)
        with self.assertRaises(ValueError):
            create_request(self.maria, self.trip, scenario_for(self.data["occurrences"], "tranquilo"), [], 1)


if __name__ == "__main__":
    unittest.main()
