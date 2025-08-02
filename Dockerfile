FROM bitnami/spark:3

USER root

# 1) installer pip3 + dev tools
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# 2) mettre à jour pip/setuptools/wheel
RUN pip3 install --upgrade pip setuptools wheel

# 3) copier et installer les dépendances Python
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# 4) copier ton code
COPY . /opt/bitnami/spark/app

# 5) repasser en utilisateur spark (1001)
USER 1001
WORKDIR /opt/bitnami/spark/app 
