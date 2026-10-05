import json
from pathlib import Path

from app import create_app


def test_application_entrypoint_exists():
    assert Path("app.py").is_file()


def test_home_page_shows_the_three_kanban_columns():
    app = create_app()
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"A faire" in response.data
    assert b"En cours" in response.data
    assert b"Termine" in response.data


def test_user_can_add_a_card_to_the_todo_column(tmp_path):
    app = create_app(data_file=tmp_path / "cards.json")
    response = app.test_client().post(
        "/cards",
        data={"title": "Ecrire les tests", "description": "Ajouter Pytest"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Ecrire les tests" in response.data
    assert b"Ajouter Pytest" in response.data


def test_user_can_move_a_card_to_another_column(tmp_path):
    data_file = tmp_path / "cards.json"
    data_file.write_text(
        json.dumps([
            {"id": 1, "title": "Ecrire les tests", "description": "", "column": "todo"}
        ]),
        encoding="utf-8",
    )
    app = create_app(data_file=data_file)

    response = app.test_client().post("/cards/1/move", data={"column": "doing"})

    assert response.status_code == 302
    assert json.loads(data_file.read_text(encoding="utf-8"))[0]["column"] == "doing"
