#!flask/bin/python
from flask import request
from flask import Flask
from geojson import Point
from geojson import Feature

app = Flask(__name__)

@app.route('/api1/rest/services/height', methods=['GET'])
def index():
    
#    easting = request.args.get('easting', '')
#    northing = request.args.get('northing', '')
#    try:
#        float(northing)
#    except ValueError, e:
#        print e
    

    params = check_parameters(request.args)
    print "params: "  + str(params)
    
    if not params:
        print "abbruch"
        return '{"dtm":"None"}'
        
    
    
    return "Hello, World!"
    
def check_parameters(args):
    easting = args.get('easting', '')
    northing = args.get('northing', '')
    
    if easting == '':
        return
        
    if northing == '':
        return
        
    try:
        easting = float(easting)
    except ValueError, e:
        print e
        return

    try:
        northing = float(northing)
    except ValueError, e:
        print e
        return        

    x = float(easting)
    y = float(northing)
        
    my_point = Point((easting, northing))
    my_feature = Feature(geometry=my_point, id=1)
    #print my_feature
    
    return {'easting': easting, 'northing': northing}


if __name__ == '__main__':
    app.run(debug=True)


#http://127.0.0.1:5000/api1/rest/services/height?easting=600000&northing=200000
#http://127.0.0.1:5000/api1/rest/services/height?easting=607885&northing=228280
