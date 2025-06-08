from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

AGENTS = {
    "machine1": "http://192.168.1.10:5001",
    "machine2": "http://192.168.1.11:5001"
}

@app.route('/')
def index():
    return render_template('index.html', agents=AGENTS)

@app.route('/<agent>/sensors')
def sensors(agent):
    try:
        resp = requests.get(f"{AGENTS[agent]}/sensors")
        sensors_output = resp.json().get("sensors", "Erreur de lecture")
    except Exception as e:
        sensors_output = f"Erreur : {str(e)}"
    return render_template('sensors.html', agent=agent, output=sensors_output)

@app.route('/<agent>/service/<action>')
def control_service(agent, action):
    try:
        requests.post(f"{AGENTS[agent]}/service", json={"action": action})
    except Exception as e:
        return f"Erreur : {e}"
    return redirect(url_for('index'))

@app.route('/<agent>/config', methods=['GET', 'POST'])
def edit_config(agent):
    url = f"{AGENTS[agent]}/config"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
