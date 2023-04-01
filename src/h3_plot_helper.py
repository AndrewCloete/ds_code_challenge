"""
References
https://gist.github.com/jens-andersson-2-wcar/7cecb40db1fbc051f2822262be42d11b
https://github.com/uber/h3-py-notebooks/blob/master/notebooks/usage.ipynb
"""

from geojson import Feature, FeatureCollection
import json
import h3

def h3_index_to_geojson(h3_indexes):
    list_features = []
    for h3_index in h3_indexes:
        try:
            geometry_for_row = { "type" : "Polygon", "coordinates": [h3.h3_to_geo_boundary(h=h3_index,geo_json=True)]}
            feature = Feature(geometry = geometry_for_row , id=h3_index)
            list_features.append(feature)
        except:
            print("An exception occurred for hex " + h3_index) 

    feat_collection = FeatureCollection(list_features)
    geojson_result = json.dumps(feat_collection)
    return geojson_result
