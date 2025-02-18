from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos en memoria (solo para ejemplo)
tasks = []

@app.route('/tasks', methods=['POST'])
def create_task():
    task = request.json
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    return jsonify(task) if task else ('', 404)

if __name__ == '__main__':
    app.run(port=5002)