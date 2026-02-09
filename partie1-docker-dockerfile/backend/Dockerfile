# I- Choix d'une image Python optimisée (version slim pour réduire la taille)
FROM python:3.11-slim AS builder

# Installer wget pour le healthcheck
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier uniquement le fichier requirements.txt pour installer les dépendances
COPY requirements.txt .

# Installer les dépendances ML sans cache pour réduire la taille de l'image
RUN pip install --no-cache-dir -r requirements.txt

# II- Créer l'image finale
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances installées depuis l'image builder
COPY --from=builder /usr/local /usr/local

# Copier le code source de l'application
COPY . .
COPY models/ /app/models/

# Exposer le port sur lequel l'API sera accessible
EXPOSE 8000

# Définir un healthcheck pour vérifier que l'API est en bonne santé
#HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1
HEALTHCHECK CMD wget -qO- http://localhost:8000/health || exit 1

# Commande par défaut pour lancer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
