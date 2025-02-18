from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos en memoria (solo para ejemplo)
users = []

@app.route('/users', methods=['POST'])
def create_user():
    user = request.json
    users.append(user)
    return jsonify(user), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    return jsonify(user) if user else ('', 404)

if __name__ == '__main__':
    app.run(port=5001)