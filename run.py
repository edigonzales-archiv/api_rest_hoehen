#!venv/bin/python
from flask import request
from flask import Flask
from flask import jsonify
from flask import json
from flask import Response
from osgeo import gdal
from osgeo.gdalconst import *
from osgeo import ogr
from osgeo import osr
import struct

#DTM_VRT = "/home/stefan/Downloads/dtm/grid/50cm/dtm.vrt"
#DSM_VRT = "/home/stefan/Downloads/dom/grid/50cm/dom.vrt"

#DTM_VRT = "/opt/Geodaten/ch/so/kva/hoehen/2014/dtm/grid/50cm/dtm.vrt"
#DSM_VRT = "/opt/Geodaten/ch/so/kva/hoehen/2014/dom/grid/50cm/dom.vrt"

DTM_VRT = "/home/stefan/Projekte/api_rest_hoehen/dtm.vrt"
DSM_VRT = "/home/stefan/Projekte/api_rest_hoehen/dom.vrt"

# File path of chenyx06a.gsb hardcoded!
S_SRS = "+proj=somerc +lat_0=46.952405555555555N +lon_0=7.439583333333333E +ellps=bessel +x_0=2600000 +y_0=1200000 +towgs84=674.374,15.056,405.346 +units=m +k_0=1 +nadgrids=@null"
T_SRS = "+proj=somerc +lat_0=46.952405555555555N +lon_0=7.439583333333333E +ellps=bessel +x_0=600000 +y_0=200000 +towgs84=674.374,15.056,405.346 +units=m +units=m +k_0=1 +nadgrids=/home/stefan/Projekte/api_rest_hoehen/chenyx06a.gsb"

app = Flask(__name__)

@app.route('/height', methods=['GET'])
def height():
    easting = request.args.get('easting', '')
    northing = request.args.get('northing', '')

    # do some basic parameters checks and return none
    # if non-sense coords
    try:
        easting, northing = check_parameters(request.args)
    except TypeError, e:
        data = {"terrain": "None", "surface": "None"}
        resp = Response(response=json.dumps(data), status=200, mimetype="application/json")
        return resp

    # try to figure out if the request is in LV95
    is_lv95 = check_for_lv95(easting, northing)
    
    # transform coordinate from LV95 to LV03    
    if is_lv95:
        easting, northing = lv95tolv03(easting, northing)
        
    # get height from gdal vrt files
    terrain = get_height(easting, northing, 'dtm')
    surface = get_height(easting, northing, 'dom')

    # Why does jsonify not work here? Is it a Python version issue?
    if terrain and surface:
        #data = jsonify(terrain="%.1f" % terrain, surface="%.1f" % surface)
        data = {"terrain": "%.1f" % terrain, "surface": "%.1f" % surface}
    else:
        #data = jsonify(terrain="None", surface="None")
        data = {"terrain": "None", "surface": "None"}
        
    #resp = Response(response=data, status=200, mimetype="application/json")
    resp = Response(response=json.dumps(data), status=200, mimetype="application/json")
    return resp

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

    return (easting, northing)


def check_for_lv95(easting, northing):    
    if easting > 2000000 and northing > 1000000:
        return True


def lv95tolv03(easting, northing):
    source = osr.SpatialReference()
    source.ImportFromProj4(S_SRS)

    target = osr.SpatialReference()
    target.ImportFromProj4(T_SRS)
    
    transform = osr.CoordinateTransformation(source, target)
    
    point = ogr.CreateGeometryFromWkt("POINT ("+str(easting)+ " "+str(northing)+")")
    point.Transform(transform)
    return (point.GetX(), point.GetY())
    

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
        return
    else:
        structval = rb.ReadRaster(px, py, 1, 1, buf_type = gdal.GDT_Float32)
        # Is this THE way to handle out of range errors correctly?
        # It still throws an error on console...
        if structval:
            tuple_of_floats = struct.unpack('f', structval)
            height = float(tuple_of_floats[0])
            # This is a bit heuristic since it depends on how you set no-data value.
            if height <= 0:
                return
            return height
        else:
            return
            

if __name__ == '__main__':
    app.run(debug=True)

#http://www.catais.org/api/v1.0/rest/services/height?easting=600000&northing=200000
#http://www.catais.org/api/v1.0/rest/services/height?easting=607885&northing=228280
#http://www.catais.org/api/v1.0/rest/services/height?easting=2607885&northing=1228280
#http://www.catais.org/api/v1.0/rest/services/height?easting=700000&northing=250000

#http://127.0.0.1:5000/height?easting=600000&northing=200000
#http://127.0.0.1:5000/height?easting=607885&northing=228280
#http://127.0.0.1:5000/height?easting=600000&northing=240000
#http://127.0.0.1:5000/height?easting=2607885&northing=1228280
