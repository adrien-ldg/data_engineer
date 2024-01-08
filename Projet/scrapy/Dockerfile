# Utiliser une image Python officielle basée sur Debian
FROM python:3.8-slim

# Mettre à jour les paquets et installer les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libxml2-dev libxslt1-dev libjpeg-dev libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY /requirements.txt .
COPY /env/ .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exécuter le scrapping avec Scrapy et stocker les données dans MongoDB
CMD scrapy crawl nom_du_spider
