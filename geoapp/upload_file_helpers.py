import pandas as pd 
import xlrd 
from django.http import HttpResponse
import requests
from urllib.parse import urlencode
from django.conf import settings
import os


def generate_excel_status(filename=None):
    new_data = {'address':[],'latitude':[],'longitute':[]}
    api_key = "your_api_key" # add you geocoding api key 
    excel_data_df = pd.read_excel(filename)
    current_data = excel_data_df.to_dict(orient='record')
    for row in current_data:
        lat, lng =  extract_lat_lng(api_key, row['address'], data_type='json')
        new_data['address'] = new_data['address'] + [row['address']]
        new_data['latitude'] = new_data['latitude'] + [lat]
        new_data['longitute'] = new_data['longitute'] + [lng]

    directory =  settings.STATIC_DIR + '/files/'
    file_path = directory + f'{filename}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    df = pd.DataFrame(new_data)
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    return True        
    
def extract_lat_lng(api_key, address, data_type='json'):
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address":address, "key":api_key} 
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    req = requests.get(url)
    if req.status_code not in range(200,299):
        return {}
    latlong = {}
    try:
        latlong = req.json()['results'][0]['geometry']['location']
    except:
        pass
    return latlong.get('lat'), latlong.get('lng')
        