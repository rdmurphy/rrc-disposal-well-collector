"""

0 = UIC No.
2 = API No.
4 = District
6 = Lease No.
8 = Lease Name
9 = Well No.
10 = Field Name
11 = Operator Name
12 = County
13 = Oil/Gas

"""

import csv
import re
from glob import glob

from pyquery import PyQuery as pq

WELL_FILES_PATHS = glob('well_html/wells_offset*.html')
targets = [0, 2, 4, 6, 8, 9, 10, 11, 12, 13]

with open('well_data_output/well_data.csv', 'wb') as rfile:
    writer = csv.writer(rfile)
    writer.writerow([
        'UIC No.',
        'API No.',
        'District',
        'Lease No.',
        'Lease Name',
        'Well No.',
        'Field Name',
        'Operator Name',
        'County',
        'Oil/Gas',
        'Type',
    ])

    for path in WELL_FILES_PATHS:
        print('Working on {0}'.format(path))
        with open(path, 'rb') as well_file:
            table_rows = pq(well_file.read()).find('table').eq(8).find('tr')
            for i, row in enumerate(table_rows):
                if i % 3 == 0 and i != 0:
                    cells = pq(row).find('td')
                    results = []
                    for target in targets:
                        results.append(cells.eq(target).text())
                    results.append(re.search(r'\(.*?\)', path).group()[1:-1])
                    writer.writerow(results)
