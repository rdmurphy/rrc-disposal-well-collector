import csv
import re
import urllib
from glob import glob

from pyquery import PyQuery as pq

GEO_KML_FILES = glob('well_geokml/geo_*.xml')
lat_match = 'GIS_LAT83=\"(.*?)\"\+SDE'  # 11 off front, 5 off back
lon_match = 'GIS_LONG83=\"(.*?)</FEATURE>'  # 12 off front, 14 off back

with open('well_data_output/geocoded_well_apis.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow([  # header row
        'well',
        'lat',
        'lon',
    ])

    for geo_file in GEO_KML_FILES:
        with open(geo_file, 'rb') as f:
            file_text = f.read()
            script = pq(file_text).find('SCRIPT')

            fields = urllib.unquote(re.search('\'(.+)', script.text()).group()[1:-2])
            counts = len(re.findall('GIS_LAT83', fields))

            if counts > 0:
                lat = re.search(lat_match, fields).group()[11:-5]
                lon = re.search(lon_match, fields).group()[12:-14]
            else:
                lat = None
                lon = None

            writer.writerow([
                geo_file[16:-4],
                str(lat),
                str(lon),
            ])
