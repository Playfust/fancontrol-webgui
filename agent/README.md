# Fancontrol Agent

Agent léger en Python/Flask pour contrôler `fancontrol` à distance (lecture/écriture de config, contrôle du service, lecture des capteurs).

## 🚀 Installation

### 1. Créer un utilisateur dédié

```bash
sudo useradd -r -s /bin/false fanagent
```

### 2. Déposer le fichier sudoers

```bash
sudo cp sudoers.fanagent /etc/sudoers.d/fanagent
sudo chmod 440 /etc/sudoers.d/fanagent
```

### 3. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 4. Lancer l'agent

```bash
sudo python3 agent.py
```

## 🔐 Sécurité

- L'agent doit être restreint au réseau local
- Ajouter une clé API ou auth plus tard
- À utiliser avec un pare-feu (ufw, iptables)

## 📡 Routes disponibles

- `GET /sensors` – Donne les infos `lm-sensors`
- `GET /config` – Lit `/etc/fancontrol`
- `POST /config` – Met à jour `/etc/fancontrol` (JSON: `{ config: "<texte>" }`)
- `POST /service` – Contrôle le service (JSON: `{ action: "restart" }`)
