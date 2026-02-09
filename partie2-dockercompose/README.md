 Partie 2 – Docker Compose

 1. Objectif de la partie
Cette partie a pour objectif d’orchestrer les différents services de l’application à l’aide de **Docker Compose**. Elle permet de déployer une application multi-conteneurs de manière cohérente, reproductible et configurable, en s’appuyant sur les images Docker créées lors de la Partie 1.

Les services orchestrés sont :
* Backend (API FastAPI)
* Frontend (Application Web servie par Nginx)
* Base de données PostgreSQL
* Cache Redis

---
2. Organisation des fichiers
```
partie-2-dockercompose/
├── docker-compose.yml
├── .env.exemple
├── .env
└── README.md
```

* `docker-compose.yml` : définition de l’ensemble des services, réseaux et volumes
* `.env.exemple` : exemple de variables d’environnement (sans données sensibles) versionné sur git
* `.env` :  variables d’environnement non versionné sur Git

---
 3. Description du fichier docker-compose.yml

Le fichier `docker-compose.yml` définit :

* **Les services** : backend, frontend, PostgreSQL et Redis
* **Les réseaux personnalisés** :

  * `backend-net` pour les services internes (API, base de données, cache)
  * `frontend-net` pour l’interface utilisateur
* **Les volumes persistants** :

  * `pgdata` pour la persistance des données PostgreSQL
  * `ml_models` pour le stockage des modèles de Machine Learning
* **Les dépendances entre services** grâce à `depends_on` et aux healthchecks
* **Les limites de ressources** (CPU et mémoire) pour chaque conteneur

Cette configuration permet une isolation claire des services et prépare l’application à une mise à l’échelle ultérieure.

---
 4. Gestion des variables d’environnement

Les variables d’environnement sont externalisées dans un fichier `.env` (non versionné) afin de renforcer la sécurité et la flexibilité de la configuration.

Le fichier `.env.example` contient un exemple de configuration :

* Paramètres de la base de données PostgreSQL
* Informations de connexion utilisées par le backend
* Configuration de Redis

---
5. Persistance et gestion des données

* Les données PostgreSQL sont stockées dans un **volume nommé** afin de garantir leur persistance après l’arrêt des conteneurs.
* Un volume dédié est prévu pour le stockage des **modèles ML pré-entraînés**.
* Un dossier de sauvegarde est monté pour faciliter les opérations de backup de la base de données.

---
 6. Sécurité et bonnes pratiques

* Les secrets ne sont pas stockés directement dans le fichier `docker-compose.yml`.
* Les réseaux sont isolés afin de limiter l’exposition des services internes.
* Des limites de ressources sont définies pour éviter la surconsommation.

---
 7. Démarrage de l’application

Depuis le dossier `partie-2-dockercompose` :

```bash----
docker compose up --build
```

### Arrêt de l’application

```bash---
docker compose down
```

---

### 8. Vérifications

* Backend : [http://localhost:8000] (http://localhost:8000)
* Healthcheck backend : [http://localhost:8000/health] (http://localhost:8000/health)
* Frontend : [http://localhost:3000] (http://localhost:3000)

---
9. Conclusion

Cette partie permet de valider l’orchestration locale de l’application multi-services à l’aide de Docker Compose. Elle constitue une étape intermédiaire essentielle avant le déploiement en cluster avec Docker Swarm et Kubernetes.
