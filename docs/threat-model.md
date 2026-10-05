# Threat model — Mini Kanban

## Périmètre

```text
Développeur → GitHub → GitHub Actions / runner auto-hébergé
→ image Docker → GHCR → conteneur Mini Kanban → SQLite
```

Le runner est une machine de lab réservée au dépôt. Le socket Docker lui est accessible pour permettre le déploiement ; cet accès est assimilable à un privilège élevé sur cette machine.

## Actifs et frontières de confiance

| Actif | Risque principal | Frontière |
|---|---|---|
| Code et workflows GitHub | modification non revue | pull request / branche protégée |
| Jetons et clés | fuite ou réutilisation | Git, GitHub Actions, runner |
| Dépendances et image de base | composant vulnérable ou malveillant | PyPI, registre OCI |
| Image publiée | substitution ou altération | registry / digest / signature |
| Base SQLite | perte ou modification de cartes | volume Docker |
| Runner auto-hébergé | persistance ou élévation de privilèges | VM de lab / socket Docker |

## Menaces et contrôles

| STRIDE | Menace | Contrôle automatisé | Décision |
|---|---|---|---|
| Information disclosure | secret commité | Gitleaks | échec immédiat, révocation et rotation du secret |
| Tampering | modification dangereuse du code | Bandit et Semgrep | échec sur finding bloquant, analyse documentée des faux positifs |
| Tampering | dépendance ou image vulnérable | pip-audit et Trivy | blocage des CVE critiques corrigées ; vulnérabilité non corrigée tracée |
| Tampering | image remplacée après le build | digest OCI et signature Cosign | vérification avant déploiement obligatoire |
| Elevation of privilege | conteneur trop privilégié | Trivy config, utilisateur non-root, read-only, capabilities supprimées | échec si une configuration critique est détectée |
| Repudiation | origine de l'artefact inconnue | SHA de commit, SBOM CycloneDX, signature OIDC | artefact non signé non déployé |
| Denial of service | application indisponible | healthcheck Docker et sonde HTTP | rollback manuel vers un digest antérieur validé |
| Information disclosure | défaut HTTP exploitable | OWASP ZAP baseline | rapport conservé comme artefact et findings analysés |

## Hypothèses et limites

- Ce TP ne comporte pas d'authentification : il ne doit pas contenir de données réelles ou sensibles.
- Le port `8000` est publié sur toutes les interfaces à la demande du projet ; le filtrage réseau et le TLS relèvent de l'infrastructure devant l'application.
- Le runner persistant est une limitation connue. Il ne doit pas exécuter des workflows provenant de forks ou de contributeurs non approuvés.
- Un SBOM inventorie les composants ; il ne constitue pas à lui seul une preuve d'absence de vulnérabilité.
