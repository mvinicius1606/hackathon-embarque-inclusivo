"""Fluxos reais de widgets, callbacks e reruns com o AppTest do Streamlit."""
import unittest
from datetime import time
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app" / "src" / "streamlit_app.py"


class AppTests(unittest.TestCase):
    def app(self, user="USR-002"):
        at = AppTest.from_file(str(APP), default_timeout=20).run()
        self.assertFalse(list(at.exception))
        at.button(key=f"login_{user}").click().run()
        self.assertFalse(list(at.exception))
        return at

    def assert_healthy(self, at):
        self.assertEqual([e.message for e in at.exception], [])

    def test_navigation_support_and_context_reset(self):
        at = self.app()
        for scenario in ("tranquilo", "moderado", "pico", "ocorrencia"):
            at.selectbox(key="scenario_mode").select(scenario).run()
            self.assert_healthy(at)
        at.button(key="nav_Apoio").click().run()
        at.button(key="FormSubmitter:support_form-Enviar pedido simulado").click().run()
        self.assertEqual(at.session_state["request"]["status"], "pendente")
        at.button(key="confirm_request").click().run()
        self.assertEqual(at.session_state["request"]["status"], "confirmado")
        at.button(key="nav_Viagem").click().run()
        self.assertEqual(at.session_state["request"]["status"], "confirmado")
        at.button(key="nav_Apoio").click().run()
        at.button(key="finish_request").click().run()
        self.assertEqual(at.session_state["request"]["status"], "concluido")
        at.selectbox(key="scenario_mode").select("tranquilo").run()
        self.assertIsNone(at.session_state["request"])
        at.selectbox(key="scenario_mode").select("horario").run()
        at.slider(key="manual_hour").set_value(2).run()
        self.assertNotIn("Enviar pedido simulado", [b.label for b in at.button])
        self.assert_healthy(at)

    def test_routine_return_and_trip_validation(self):
        at = self.app()
        original = dict(at.session_state["trip"])
        at.radio(key="chosen_direction").set_value("Volta")
        at.button(key="FormSubmitter:routine_picker-Usar esta viagem").click().run()
        self.assertEqual(at.session_state["trip"]["origin"], original["destination"])
        self.assertEqual(at.session_state["trip"]["destination"], original["origin"])
        at.button(key="edit_trip").click().run()
        at.selectbox(key="edit_destination").select(at.selectbox(key="edit_origin").value)
        at.button(key="FormSubmitter:trip_form-Consultar viagem").click().run()
        self.assertTrue(list(at.error))
        self.assertTrue(at.session_state["trip_editor"])
        self.assert_healthy(at)

    def test_profile_reading_persists_and_custom_routine(self):
        at = self.app("USR-003")
        at.button(key="nav_Perfil").click().run()
        at.toggle(key="large_text").set_value(True).run()
        at.toggle(key="high_contrast").set_value(True).run()
        at.button(key="nav_Viagem").click().run()
        at.button(key="nav_Perfil").click().run()
        self.assertTrue(at.session_state["large_text"])
        self.assertTrue(at.session_state["high_contrast"])
        at.checkbox(key="pref_stairs").check()
        at.button(key="FormSubmitter:profile_form-Salvar preferências").click().run()
        self.assertTrue(at.session_state["user"]["necessita_percurso_sem_escadas"])
        at.selectbox(key="routine_origin").select("EST-003")
        at.selectbox(key="routine_destination").select("EST-007")
        at.time_input(key="routine_departure").set_value(time(8, 0))
        at.time_input(key="routine_return").set_value(time(17, 0))
        at.button(key="FormSubmitter:routine_form-Salvar rotina da sessão").click().run()
        custom = at.session_state["session_routine"]
        self.assertEqual(custom["legs"]["volta"]["origin"], "EST-007")
        self.assertEqual(custom["legs"]["volta"]["destination"], "EST-003")
        self.assertEqual(at.session_state["page"], "Viagem")
        self.assert_healthy(at)

    def test_station_search_and_temporary_support(self):
        at = self.app("USR-003")
        at.button(key="nav_Estações").click().run()
        at.text_input(key="station_search").set_value("agua branca").run()
        self.assertEqual(at.selectbox(key="station_choice").options, ["Água Branca"])
        at.text_input(key="station_search").set_value("estacao inexistente").run()
        self.assertTrue(any("Nenhuma estação" in i.value for i in at.info))
        at.button(key="nav_Apoio").click().run()
        at.multiselect(key="support_types").set_value(["Orientação na estação"])
        at.button(key="FormSubmitter:support_form-Enviar pedido simulado").click().run()
        self.assertEqual(at.session_state["request"]["status"], "pendente")
        at.button(key="cancel_request").click().run()
        self.assertEqual(at.session_state["request"]["status"], "cancelado")
        self.assert_healthy(at)


if __name__ == "__main__":
    unittest.main()
