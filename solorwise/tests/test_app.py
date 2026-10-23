"""Streamlit integration checks: navigation, calculator, and quiz workflows."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

from content import QUIZ

APP = str(Path(__file__).parents[1] / "app.py")


def start_app():
    app = AppTest.from_file(APP, default_timeout=20).run()
    assert not app.exception
    return app


def test_navigation_and_campaign_placeholder():
    app = start_app()
    assert any(button.label == "Visit Our Instagram Campaign" and button.disabled for button in app.button)
    for page in ["Solar Calculator", "Clean Energy Education", "About / Methodology", "Home"]:
        app.radio(key="page").set_value(page).run()
        assert not app.exception
    app.button[0].click().run()
    assert app.radio(key="page").value == "Solar Calculator"


def test_calculator_results_zero_edges_and_persistent_inputs():
    app = start_app()
    app.radio(key="page").set_value("Solar Calculator").run()
    metrics = {metric.label: metric.value for metric in app.metric}
    assert metrics["Monthly savings"] == "RM 100.00"
    assert metrics["Annual savings"] == "RM 1,200.00"
    assert metrics["Simple payback"] == "10.00 years"
    app.slider(key="_input_reduction").set_value(0).run()
    assert any(metric.label == "Simple payback" and metric.value == "N/A" for metric in app.metric)
    assert app.warning
    app.slider(key="_input_reduction").set_value(100).run()
    app.number_input(key="_input_cost").set_value(0.0).run()
    assert any(metric.label == "Simple payback" and metric.value == "0.00 years" for metric in app.metric)
    app.number_input(key="_input_bill").set_value(350.0).run()
    app.radio(key="page").set_value("Home").run()
    app.radio(key="page").set_value("Solar Calculator").run()
    assert app.number_input(key="_input_bill").value == 350.0
    next(button for button in app.button if button.label == "Reset to example").click().run()
    assert app.number_input(key="_input_bill").value == 200.0
    assert app.slider(key="_input_reduction").value == 50
    assert not app.exception


def test_quiz_immediate_feedback_score_persistence_and_retry():
    app = start_app()
    app.radio(key="page").set_value("Clean Energy Education").run()
    assert all(app.radio(key=f"_quiz_{i}").value is None for i in range(5))
    for i, question in enumerate(QUIZ):
        app.radio(key=f"_quiz_{i}").set_value(question["options"][question["correct"]]).run()
        assert not app.exception
        assert any("Correct!" in message.value for message in app.success)
    assert any("Final score: 5 / 5" in message.value for message in app.success)
    app.radio(key="_quiz_0").set_value(QUIZ[0]["options"][0]).run()
    assert any("The correct answer is:" in message.value for message in app.info)
    assert any("Final score: 4 / 5" in message.value for message in app.success)
    app.radio(key="page").set_value("Home").run()
    app.radio(key="page").set_value("Clean Energy Education").run()
    assert any("Final score: 4 / 5" in message.value for message in app.success)
    next(button for button in app.button if button.label == "Try the quiz again").click().run()
    assert all(app.radio(key=f"_quiz_{i}").value is None for i in range(5))
    assert not any("Final score:" in message.value for message in app.success)
    assert not app.exception
