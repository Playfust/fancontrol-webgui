from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/config', methods=['GET'])
def get_config():
    result = subprocess.check_output(['sudo', 'cat', '/etc/fancontrol'])
    return jsonify({'config': result.decode()})

@app.route('/config', methods=['POST'])
def update_config():
    config = request.json.get('config')
    subprocess.run(['sudo', 'tee', '/etc/fancontrol'], input=config.encode())
    return jsonify({'status': 'updated'})

@app.route('/service', methods=['POST'])
def control_service():
    action = request.json.get('action')
    if action not in ['start', 'stop', 'restart']:
        return jsonify({'error': 'Invalid action'}), 400
    subprocess.call(['sudo', 'systemctl', action, 'fancontrol'])
    return jsonify({'status': f'{action} sent'})

@app.route('/sensors', methods=['GET'])
def get_sensors():
    output = subprocess.getoutput('sensors')
    return jsonify({'sensors': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
