#!/bin/bash

set -e

echo "📦 Mise à jour des paquets..."
apt update
apt install -y unzip python3 python3-pip python3-venv wget
cd /opt

echo "⬇️ Téléchargement de l'archive ZIP..."
wget -O fancontrol-webgui.zip https://github.com/Playfust/fancontrol-webgui/releases/download/v0.2/fancontrol-dashboard.zip

echo "📦 Extraction..."
unzip fancontrol-dashboard.zip
rm fancontrol-dashboard.zip
mv dashboard ./fancontrol-webgui
cd fancontrol-webgui

echo "🐍 Création de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

echo "🛠️ Installation du service systemd..."
cat <<EOF > /etc/systemd/system/fancontrol-webgui.service
[Unit]
Description=Fancontrol Dashboard Web UI
After=network.target

[Service]
User=root
WorkingDirectory=/opt/fancontrol-webgui
ExecStart=/opt/fancontrol-webgui/venv/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "🔄 Activation du service au démarrage..."
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable fancontrol-webgui
systemctl start fancontrol-webgui

echo "✅ Installation terminée et service lancé !"
echo "👉 Interface accessible sur le port 5003"
