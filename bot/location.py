import urllib.request
import json


def get_city_name(payload):

    lat_ = payload["coordinates"]["lat"]
    long_ = payload["coordinates"]["long"]
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng="
                                      + str(lat_) + "," + str(long_) +
                                      "&key=AIzaSyCSydwOnjMcl7Gz8IFQLaTEp1aj5ww4vU4")

    resp = response.read().decode('UTF-8')
    print(resp)
    resp = json.loads(resp)
    for entry in resp["address_components"]:
        if "administrative_area_level_2" in entry["types"]:
            print(entry)
            return entry['long_name']
    for entry in resp["address_components"]:
        if "administrative_area_level_1" in entry["types"]:
            print(entry)
            return entry['long_name']
