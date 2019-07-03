from Magics import macro as macro
import requests
import os
import boto3

def xyplot(x, y, title = "", where = None):
     #Setting the cartesian view
    projection = macro.mmap(subpage_map_projection = 'cartesian',
                subpage_x_automatic = 'on',
                subpage_y_automatic = 'on',
                     )
    #Vertical axis
    vertical = macro.maxis(axis_orientation = "vertical",
                     axis_grid =  "on",
                     axis_grid_colour = "grey",
                     axis_grid_thickness = 1,
                     axis_grid_line_style = "dot")

    #Horizontal axis
    horizontal = macro.maxis(axis_orientation = "horizontal",
                     axis_grid =  "on",
                     axis_grid_colour = "grey",
                     axis_grid_thickness = 1,
                     axis_grid_line_style = "dot")
    x[0] = x[0]*1.
    input = macro.minput(input_x_values = x,
            input_y_values = y)
    graph = macro.mgraph(graph_line_colour = "navy", 
                         graph_line_thickness = 2)
    
    input = macro.minput(input_x_values = x,
            input_y_values = y)
    text = macro.mtext(text_lines = [title])
    if where:
        where.clear_output()
        with where:
            display(macro.plot(projection, vertical, horizontal, input, graph, text))
    else:
        return macro.plot(projection, vertical, horizontal, input, graph, text)


def geoplot(data):
    contour = macro.mcont(contour_automatic_setting = "ecmwf", legend=True)
    legend = macro.mlegend(legend_display_type="continuous")
    return macro.plot(data, contour, macro.mcoast(), macro.mtext(), legend)


def time_series(lat, lon):
    r = requests.get("http://point-db-api.sylvie.svc.cluster.local:5000/time-series/lat/%d/lon/%d" % (lat, lon))
    return r.json()

def get_data_bucket(index):
    s3 = boto3.client('s3', endpoint_url='http://%(AWS_ENDPOINT)s' % os.environ)
    objs = s3.list_objects(Bucket='eccharts-fields')
    object_name = objs['Contents'][index]['Key']
    data = '/tmp/bucket-%d.grib' % index
    s3.download_file('eccharts-fields', object_name, data)
    return data

def get_metadata_bucket(index):
    s3 = boto3.client('s3', endpoint_url='http://%(AWS_ENDPOINT)s' % os.environ)
    objs = s3.list_objects(Bucket='eccharts-fields')
    object = objs['Contents'][index]
    return object

def get_data_bucket_count():
    s3 = boto3.client('s3', endpoint_url='http://%(AWS_ENDPOINT)s' % os.environ)
    objs = s3.list_objects(Bucket='eccharts-fields')
    
    return len(objs)

    
    