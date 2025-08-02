FROM bitnami/spark:3

USER root

# Installation ultra-minimale : plus besoin de numpy/sklearn !
RUN apt-get update && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Installer seulement kafka-python (plus besoin de numpy/sklearn !)
RUN pip3 install --no-cache-dir kafka-python==2.0.2

# Copier le code
COPY . /opt/bitnami/spark/app

# Repasser en utilisateur spark (1001)
USER 1001
WORKDIR /opt/bitnami/spark/app