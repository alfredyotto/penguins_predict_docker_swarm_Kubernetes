
PARTIE 1 : DOCKER

 Partie 1 – Docker et Dockerfile
 1. Introduction

Cette partie du projet a pour objectif de mettre en œuvre la conteneurisation des différents composants de l’application d’intelligence artificielle à l’aide de Docker. Elle se concentre principalement sur la création de Dockerfiles optimisés pour le backend et le frontend, tout en respectant les bonnes pratiques recommandées dans un contexte cloud.

L’application est composée de :

* Un **backend** d’API de prédiction basé sur Python (FastAPI/Flask)
* Un **frontend web** développé avec un framework JavaScript moderne (Vue.js dans notre cas)

---

2. Choix techniques globaux

* **Docker** a été choisi afin de garantir la portabilité, la reproductibilité et l’isolation de l’application.
* L’utilisation de **builds multi-stage** permet de réduire la taille finale des images Docker.
* Les images officielles **slim** et **alpine** ont été privilégiées pour minimiser la surface d’attaque et l’empreinte mémoire.
* Les dépendances applicatives sont externalisées dans des fichiers dédiés (`requirements.txt`, `package.json`).

---

 3. Dockerfile du Backend

 3.1 Image de base

Le backend utilise l’image :

```
python:3.11-slim
```
Ce choix permet de bénéficier d’une version récente de Python tout en réduisant la taille de l’image par rapport à une image complète.

 3.2 Dépendances Machine Learning

Les bibliothèques de Machine Learning nécessaires au projet sont installées via le fichier `requirements.txt`, notamment :

* `numpy`
* `pandas`
* `scikit-learn`
* `tensorflow-lite` (ou `tflite-runtime`)

L’installation est effectuée avec l’option `--no-cache-dir` afin de réduire la taille finale de l’image Docker.

3.3 Build multi-stage

Le Dockerfile backend est divisé en deux étapes :

1. **Builder** : installation des dépendances Python
2. **Image finale** : exécution de l’application avec uniquement les éléments nécessaires

Cette approche permet d’éliminer les fichiers temporaires et outils inutiles dans l’image finale.

3.4 Exposition du port et Healthcheck

* Le port **8000** est exposé pour accéder à l’API.
* Un **healthcheck HTTP** est défini afin de vérifier l’état de l’API via l’endpoint `/health`.

Cela permet une meilleure supervision et facilite l’orchestration avec Docker Compose, Swarm ou Kubernetes par la suite.

---

 4. Dockerfile du Frontend

4.1 Build de l’application

Le frontend est construit à l’aide de l’image :

```
node:18-alpine
```
Cette image légère est utilisée uniquement pour la phase de build afin de générer les fichiers statiques de production.

 4.2 Serveur Nginx

Les fichiers générés sont ensuite servis via l’image :

```
nginx:alpine
```
Nginx est choisi pour sa performance, sa stabilité et sa légèreté.

4.3 Build multi-stage

Le multi-stage build permet :

* D’exclure Node.js de l’image finale
* De réduire significativement la taille du conteneur frontend

---

5. Optimisation et bonnes pratiques

5.1 Utilisation de .dockerignore

Chaque service (backend et frontend) dispose de son propre fichier `.dockerignore`. Celui-ci permet d’exclure :

* Les fichiers temporaires (`__pycache__`, `node_modules`)
* Les fichiers de configuration sensibles (`.env`)
* Les dossiers inutiles au build (`.git`, environnements virtuels)

Cela réduit le contexte de build, améliore les performances et renforce la sécurité.

5.2 Séparation des responsabilités

Chaque service possède :

* Son propre Dockerfile
* Ses dépendances dédiées

Cette séparation facilite la maintenance, les mises à jour et l’orchestration ultérieure.

5.3 Versionnement des images

Les images Docker peuvent être versionnées (ex : `backend:1.0.0`) afin d’assurer la traçabilité et la stabilité des déploiements.

---

 6. Conclusion

Cette première partie permet de poser des bases solides pour la suite du projet. Les Dockerfiles réalisés respectent les bonnes pratiques de conteneurisation, sont optimisés pour un usage cloud et constituent une fondation fiable pour l’orchestration avec Docker Compose, Docker Swarm et Kubernetes dans les parties suivantes.

---

**Environnement de développement :**

* Système : Windows
* Outil : Docker Desktop (WSL2)