#!venv/bin/python
from flask import request
from flask import Flask
from geojson import Point
from geojson import Feature

app = Flask(__name__)

@app.route('/height', methods=['GET'])
def height():
    easting = request.args.get('easting', '')
    northing = request.args.get('northing', '')

    # do some basic parameters checks
    params = check_parameters(request.args)
    print "params: "  + str(params)
    
    # return an empty point feature if easting and/or northing is not set correctly.
    if not params:
        result = create_empty_geojson()
        return result

    # try to figure out if the request is in LV95
    isLV95 = check_for_lv95(params)
    print isLV95
    
    if isLV95:
        # transform coordinate from LV95 to LV03
        pass
        
    # get height...
    


    return str(easting)



def check_parameters(args):
    easting = args.get('easting', '')
    northing = args.get('northing', '')
    
    if easting == '' or  northing == '':
        return
        
    try:
        easting = float(easting)
        northing = float(northing)        
    except ValueError, e:
        return

    return {'easting': easting, 'northing': northing}

def create_empty_geojson():
    # Cannot create empty geometry with geojson lib.
    # Let's create it by hand.
    return '{"geometry":{"coordinates": [], "type": "Point"}, "id": 1, "properties": {"terrain": "None", "surface": "None"}, "type": "Feature"}'

def check_for_lv95(params):
    easting = params['easting']
    northing = params['northing']
    
    if easting > 2000000 and northing > 1000000:
        return True




def create_geojson(easting, northing, dtm, dsm):
    print easting
    print northing
    #my_point = Point((easting, northing))
    #print my_point
#    my_feature = Feature(geometry=my_point, id=1)
    #my_feature = Feature(geometry=my_point, id=1)
    
    my_point = Point((-3.68, 40.41))    
    Feature(geometry=my_point)
    return Feature(geometry=my_point)





if __name__ == '__main__':
    app.run(debug=True)

#http://www.catais.org/api/v1.0/rest/services/height?easting=600000&northing=200000
#http://www.catais.org/api/v1.0/rest/services/height?easting=607885&northing=228280
#http://www.catais.org/api/v1.0/rest/services/height?easting=2607885&northing=1228280

#http://127.0.0.1:5000/height?easting=600000&northing=200000
#http://127.0.0.1:5000/height?easting=607885&northing=228280
#http://127.0.0.1:5000/height?easting=2607885&northing=1228280
