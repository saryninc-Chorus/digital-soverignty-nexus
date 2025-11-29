from flask import Flask, render_template, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'online',
        'platform': 'Quantum Sovereignty Network',
        'timestamp': datetime.datetime.now().isoformat(),
        'message': 'ÀṢẼ! The Trinity is Active! 🔱'
    })

@app.route('/api/network')
def network():
    return jsonify({
        'nodes': 1,
        'active': True,
        'sovereignty_score': 100
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
