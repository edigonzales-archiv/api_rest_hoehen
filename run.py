#!venv/bin/python
from flask import request
from flask import Flask
from geojson import Point
from geojson import Feature
from osgeo import gdal
from osgeo.gdalconst import *
import struct

DTM_VRT = "/home/stefan/Downloads/dtm/grid/50cm/dtm.vrt"
DSM_VRT = "/home/stefan/Downloads/dom/grid/50cm/dom.vrt"

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
    is_lv95 = check_for_lv95(params)
    print is_lv95
    
    if is_lv95:
        epsg = "EPSG:2056"
        # transform coordinate from LV95 to LV03
        pass
    else:
        epsg = "EPSG:21781"
        
    # get height from gdal vrt files
    terrain = get_height(params['easting'], params['northing'], 'dtm')
    surface = get_height(params['easting'], params['northing'], 'dom')

    # create geojson output
    feature = create_geojson(params['easting'], params['northing'], terrain, surface, epsg)

    return str(feature)

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

def get_height(easting, northing, type):
    if type == 'dtm':
        filename = DTM_VRT
    else:
        filename = DSM_VRT

    ds = gdal.Open(filename)
    gt = ds.GetGeoTransform()
    rb = ds.GetRasterBand(1)

    mx = float(easting)
    my = float(northing)

    px = int((mx - gt[0]) / gt[1]) #x pixel
    py = int((my - gt[3]) / gt[5]) #y pixel

    if px < 0 or py < 0:
        return "None"
    else:
        structval = rb.ReadRaster(px, py, 1, 1, buf_type = gdal.GDT_Float32)
        tuple_of_floats = struct.unpack('f', structval)
        height = float(tuple_of_floats[0])
        # This is a bit heuristic since it depends on how you set no-data value.
        if height <= 0:
            return "None"
        return height

def create_geojson(easting, northing, terrain, surface, epsg):
    
    epsg ={"properties": {"name": "urn:ogc:def:crs:EPSG::3785"},"type": "name"}
    
    point = Point((easting, northing), epsg)

    properties = {}
    properties["terrain"] = "%.1f" % terrain
    properties["surface"] = "%.1f" % surface
    
    feature = Feature(geometry=point, id=1, properties=properties)
    print feature
    #my_feature = Feature(geometry=my_point, id=1)
    

    return feature


if __name__ == '__main__':
    app.run(debug=True)

#http://www.catais.org/api/v1.0/rest/services/height?easting=600000&northing=200000
#http://www.catais.org/api/v1.0/rest/services/height?easting=607885&northing=228280
#http://www.catais.org/api/v1.0/rest/services/height?easting=2607885&northing=1228280

#http://127.0.0.1:5000/height?easting=600000&northing=200000
#http://127.0.0.1:5000/height?easting=607885&northing=228280
#http://127.0.0.1:5000/height?easting=2607885&northing=1228280
