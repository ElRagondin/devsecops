# Mini Kanban DevSecOps

Application Kanban minimale réalisée pour un TP DevSecOps de deux jours.

## Fonctions

- Trois colonnes : **À faire**, **En cours**, **Terminé**.
- Création de cartes avec titre et description.
- Déplacement d'une carte entre les colonnes.
- Persistance locale dans `data.json`.

## Lancer localement

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
PYTHONPATH=. .venv/bin/pytest tests/ -q
.venv/bin/python app.py
```

L'application écoute sur `http://localhost:8000`.

## Lancer avec Docker

```bash
docker build -t mini-kanban .
docker run --rm -p 8000:8000 mini-kanban
```

## Contrôles DevSecOps à ajouter

Le prochain jalon ajoute au pipeline GitHub Actions : Gitleaks, Bandit, pip-audit et Trivy.
