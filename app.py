from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)
DATA_FILE = 'coordinates.json'

# Ensure the JSON file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/get-coordinates', methods=['GET'])
def get_coordinates():
    with open(DATA_FILE, 'r') as f:
        coordinates = json.load(f)
    return jsonify(coordinates)

@app.route('/save-coordinate', methods=['POST'])
def save_coordinate():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    
    if lat is None or lng is None:
        return jsonify({'success': False, 'message': 'Invalid data.'}), 400
    
    with open(DATA_FILE, 'r') as f:
        coordinates = json.load(f)
    
    coordinates.append({'lat': lat, 'lng': lng})
    
    with open(DATA_FILE, 'w') as f:
        json.dump(coordinates, f, indent=2)
    
    return jsonify({'success': True, 'message': 'Coordinate saved.'})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
