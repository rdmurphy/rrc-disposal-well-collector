import csv
from time import sleep
from glob import glob

import requests

url = 'http://gis2.rrc.state.tx.us/arcims_sc/ims?ServiceName=simp&CustomService=Query&Form=True&Encode=True'

with open('well_data_output/well_data.csv', 'rb') as f:
    API_IDS = set()
    reader = csv.reader(f)
    reader.next()  # header row
    for line in reader:
        API_IDS.add(line[1])

COLLECTED_KML_IDS = [x[4:-4] for x in glob('well_geokml/geo_*.xml')]

for ID in API_IDS:
    if ID not in COLLECTED_KML_IDS:
        str_id = str(ID)
        if len(str_id) < 8:
            str_id = str_id.zfill(8)
        payload = {
            'ArcXMLRequest': '<ARCXML version="1.1"><REQUEST><GET_FEATURES outputmode="xml" geometry="false" featurelimit="10" checkesc="false" envelope="false"><LAYER id="20" /><SPATIALQUERY subfields="API GIS_WELL_NUMBER GIS_SYMBOL_DESCRIPTION GIS_LOCATION_SOURCE GIS_LAT27 GIS_LONG27 GIS_LAT83 GIS_LONG83" where= "API=\'' + str_id + '\'"/></GET_FEATURES></REQUEST></ARCXML>'
        }

        r = requests.post(url, data=payload)
        print('Now collecting: {0}'.format(str_id))
        with open('well_geokml/geo_{0}.xml'.format(str_id), 'wb') as f:
            f.write(r.text)
        sleep(5)
