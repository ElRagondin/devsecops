import json
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

COLUMNS = ("todo", "doing", "done")


def load_cards(data_file: Path) -> list[dict[str, str | int]]:
    if not data_file.exists():
        return []
    return json.loads(data_file.read_text(encoding="utf-8"))


def save_cards(data_file: Path, cards: list[dict[str, str | int]]) -> None:
    data_file.write_text(json.dumps(cards, ensure_ascii=False), encoding="utf-8")


def create_app(data_file: Path | None = None) -> Flask:
    app = Flask(__name__)
    app.config["DATA_FILE"] = data_file or Path(app.root_path) / "data.json"

    @app.get("/")
    def index() -> str:
        cards = load_cards(app.config["DATA_FILE"])
        cards_by_column = {
            column: [card for card in cards if card["column"] == column]
            for column in COLUMNS
        }
        return render_template("index.html", cards_by_column=cards_by_column)

    @app.post("/cards")
    def add_card() -> str:
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        if title:
            cards = load_cards(app.config["DATA_FILE"])
            next_id = max((int(card.get("id", 0)) for card in cards), default=0) + 1
            cards.append(
                {"id": next_id, "title": title, "description": description, "column": "todo"}
            )
            save_cards(app.config["DATA_FILE"], cards)
        return redirect(url_for("index"))

    @app.post("/cards/<int:card_id>/move")
    def move_card(card_id: int) -> str:
        target_column = request.form["column"]
        if target_column in COLUMNS:
            cards = load_cards(app.config["DATA_FILE"])
            for card in cards:
                if card.get("id") == card_id:
                    card["column"] = target_column
                    save_cards(app.config["DATA_FILE"], cards)
                    break
        return redirect(url_for("index"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
