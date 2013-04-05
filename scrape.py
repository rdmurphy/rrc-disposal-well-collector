import requests
import copy

from pyquery import PyQuery as pq

POST_URL = 'http://webapps2.rrc.state.tx.us/EWA/uicQueryAction.do'
DEFAULT_PAYLOAD = {
    'methodToCall': 'search',
    'pager.offset': 0,
    'pager.pageSize': 100,
    'searchArgs.countyCodeArg': 'None Selected',
    'searchArgs.districtCodeArg': 'None Selected',
    'searchArgs.h10StatusArg': '1',
    'searchArgs.injectionTypeArg': '',
    'searchArgs.permittedFluidArg': 'None Selected',
    'searchArgs.specialtyTypeArg': 'None Selected'
}


def get_number_of_records(url, query):
    p = pq(url, query, method='post')
    pager_links = p.find('table.DataGrid tr').eq(0).find('a')
    num_of_records = pager_links.eq(len(pager_links) - 1).text()

    return int(num_of_records) * 100


def write_html_to_disk(html_page, offset, type):
    with open('well_html/wells_offset_{0}_({1}).html'.format(offset, type), 'wb') as f:
        f.write(html_page)


def collect_html_pages(injection_type, type):
    query = copy.deepcopy(DEFAULT_PAYLOAD)
    query['searchArgs.injectionTypeArg'] = injection_type

    num_of_records = get_number_of_records(POST_URL, query)

    while query['pager.offset'] < num_of_records:
        offset_num = query['pager.offset']
        r = requests.post(POST_URL, data=query)
        write_html_to_disk(r.text, offset_num, type)

        query['pager.offset'] += 100

        print('Collected {0}-{1} of {2} from RRC'.format(offset_num, offset_num + 100, type))


def main():
    collect_html_pages('Disposal into a nonproductive zone (W-14)', 'W-14')
    collect_html_pages('Disposal into a productive zone (H-1)', 'H-1')


if __name__ == '__main__':
    main()
