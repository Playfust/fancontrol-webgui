from flask import Flask, render_template, request, redirect, url_for
import json
import os
import requests

app = Flask(__name__)
CONFIG_FILE = "agents.json"

def load_agents():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_agents(agents):
    with open(CONFIG_FILE, "w") as f:
        json.dump(agents, f, indent=4)

@app.route('/')
def index():
    agents = load_agents()
    status = {}
    for name, url in agents.items():
        try:
            resp = requests.post(f"{url}/service", json={"action": "status"}, timeout=2)
            result = resp.json()
            status[name] = result.get("status", "inconnu")
        except Exception:
            status[name] = "erreur"
    return render_template('index.html', agents=agents, status=status)

@app.route('/edit-agents', methods=['GET', 'POST'])
def edit_agents():
    if request.method == 'POST':
        names = request.form.getlist('name')
        urls = request.form.getlist('url')
        agents = dict(zip(names, urls))
        save_agents(agents)
        return redirect(url_for('index'))
    agents = load_agents()
    return render_template('edit_agents.html', agents=agents)

@app.route('/<agent>/sensors')
def sensors(agent):
    agents = load_agents()
    try:
        resp = requests.get(f"{agents[agent]}/sensors")
        sensors_output = resp.json().get("sensors", "Erreur de lecture")
    except Exception as e:
        sensors_output = f"Erreur : {str(e)}"
    return render_template('sensors.html', agent=agent, output=sensors_output)

@app.route('/<agent>/config', methods=['GET', 'POST'])
def edit_config(agent):
    agents = load_agents()
    url = f"{agents[agent]}/config"
    if request.method == 'POST':
        new_config = request.form.get('config')
        try:
            requests.post(url, json={"config": new_config})
        except Exception as e:
            return f"Erreur : {str(e)}"
        return redirect(url_for('index'))
    else:
        try:
            resp = requests.get(url)
            current_config = resp.json().get("config", "")
        except Exception as e:
            current_config = f"Erreur : {str(e)}"
        return render_template('config.html', agent=agent, config=current_config)

@app.route('/<agent>/service/<action>')
def control_service(agent, action):
    agents = load_agents()
    try:
        requests.post(f"{agents[agent]}/service", json={"action": action})
    except Exception as e:
        return f"Erreur : {e}"
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
