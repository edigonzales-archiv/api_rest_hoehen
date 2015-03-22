from flask import request
from flask import Flask
from geojson import Point
from geojson import Feature

app = Flask(__name__)

@app.route('/height', methods=['GET'])
def height():
    easting = request.args.get('easting', '')
    northing = request.args.get('northing', '')
    
    

    return str(easting)
