from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# URLs de los microservicios
USER_SERVICE_URL = "http://localhost:5001"
TASK_SERVICE_URL = "http://localhost:5002"
NOTIFICATION_SERVICE_URL = "http://localhost:5003"

@app.route('/users', methods=['POST'])
def create_user():
    response = requests.post(f"{USER_SERVICE_URL}/users", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/tasks', methods=['POST'])
def create_task():
    # Enviar la tarea al Task Service
    task_response = requests.post(f"{TASK_SERVICE_URL}/tasks", json=request.json)
    
    if task_response.status_code == 201:
        # Enviar notificación al Notification Service
        task_data = task_response.json()
        notification_data = {
            "task_id": task_data["id"],
            "assigned_to": task_data["assigned_to"],
            "message": f"Nueva tarea asignada: {task_data['title']}"
        }
        requests.post(f"{NOTIFICATION_SERVICE_URL}/notify", json=notification_data)
    
    return jsonify(task_response.json()), task_response.status_code

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    response = requests.get(f"{TASK_SERVICE_URL}/tasks/{task_id}")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(port=5000)