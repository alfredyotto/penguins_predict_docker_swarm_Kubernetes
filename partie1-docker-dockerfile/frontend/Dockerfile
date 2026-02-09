# I- Utilisons Node.js pour construire l'application
FROM node:18-alpine AS builder

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers package.json et package-lock.json
COPY package*.json .

# Installer les dépendances du projet
RUN npm install

# Copier le reste du code source
COPY . .

# Construire l'application pour la production
RUN npm run build

# II- Utilisons Nginx pour servir l'application
FROM nginx:alpine

COPY default.conf.template /etc/nginx/templates/default.conf.template

# Copier les fichiers générés par le build vers le répertoire de Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Exposer le port 80 pour le serveur web
EXPOSE 80


