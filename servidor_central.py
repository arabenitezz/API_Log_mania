from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
db = SQLAlchemy(app)

# Creating the database model
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    timestamp = db.Column(db.String, nullable=False)  
    service_name = db.Column(db.String, nullable=False)
    severity_level = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False) 

# Create database tables
with app.app_context():
    db.create_all()

# Valid API keys
VALID_API_KEYS = {
    "service_1": "abc123",
    "service_2": "def456"
}

@app.route('/logs', methods=['POST'])
def receive_logs():
    api_key = request.headers.get('Authorization')

    if api_key not in VALID_API_KEYS.values():
        return jsonify({'error': 'Acceso no autorizado'}), 401
    
    log_data = request.get_json()

    # Expected log fields
    log_fields = {'timestamp', 'service_name', 'severity_level', 'message'}

    if log_data and log_fields.issubset(log_data.keys()):
        # Create a new Log object
        new_log = Log(
            timestamp=log_data['timestamp'],
            service_name=log_data['service_name'],
            severity_level=log_data['severity_level'],
            message=log_data['message']
        )
        # Add and commit the log to the database
        db.session.add(new_log)
        db.session.commit()

        return jsonify({'status': 'Log recibido con éxito'}), 200
    else:
        return jsonify({'error': 'Error fatal. Datos inválidos'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)






