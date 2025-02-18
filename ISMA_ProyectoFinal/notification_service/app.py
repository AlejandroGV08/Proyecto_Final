from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    notification = request.json
    print(f"Notification sent: {notification}")
    return jsonify(notification), 200

if __name__ == '__main__':
    app.run(port=5003)