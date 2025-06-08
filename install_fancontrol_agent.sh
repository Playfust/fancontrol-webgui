#!/bin/bash

set -e

echo "📦 Mise à jour des paquets..."
apt update
apt install -y python3 python3-pip python3-venv unzip wget
cd /opt

echo "⬇️ Téléchargement de l'archive ZIP..."
wget -O fancontrol-agent.zip https://github.com/Playfust/fancontrol-webgui/releases/download/v0.2/fancontrol-agent.zip

echo "📦 Extraction..."
unzip fancontrol-agent.zip
rm fancontrol-agent.zip
mv agent ./fancontrol-agent
cd fancontrol-agent

echo "👤 Création de l'utilisateur fanagent..."
id fanagent &>/dev/null || useradd -r -s /usr/sbin/nologin fanagent

echo "🔐 Ajout des permissions sudo..."
cp sudoers.fanagent /etc/sudoers.d/fanagent
chmod 440 /etc/sudoers.d/fanagent

echo "🐍 Création de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

echo "🛠️ Installation du service systemd..."
cat <<EOF > /etc/systemd/system/fancontrol-agent.service
[Unit]
Description=Fancontrol Agent API
After=network.target

[Service]
User=root
WorkingDirectory=/opt/fancontrol-agent
ExecStart=/opt/fancontrol-agent/venv/bin/python3 agent.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "🔄 Activation du service au démarrage..."
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable fancontrol-agent
systemctl start fancontrol-agent

echo "✅ Installation de l'agent terminée et service lancé !"
echo "👉 Agent accessible sur le port 5001"
