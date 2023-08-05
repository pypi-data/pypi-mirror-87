import pandas as pd
from xml.etree import ElementTree
from fimaster.utils import get, is_bday
from datetime import datetime, timedelta

field_mappings = {
    'Id':'id', 'NEW_DATE':'date', 'BC_1MONTH':'1month','BC_2MONTH':'2monthh', 'BC_3MONTH':'3month',
    'BC_6MONTH':'6month', 'BC_1YEAR':'1year', 'BC_2YEAR': '2year', 'BC_3YEAR': '3year', 'BC_5YEAR':'5year',
    'BC_7YEAR':'7year', 'BC_10YEAR':'10year', 'BC_20YEAR': '20year', 'BC_30YEAR': '30year'
}
go_back_days = 7

def get_yield_curve_curr_month():
    url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/XmlView.aspx?data=yield'
    return parse_xml(get(url))

def construct_url(year, month, day):
    url = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter='
    if year:
        url += ' year(NEW_DATE) eq ' + str(year)
    if month:
        url += ' and month(NEW_DATE) eq ' + str(month)
    if day:
        url += ' and day(NEW_DATE) eq ' + str(day)
    return url

def get_yield_curve_bus_adj(date):
    data = parse_xml(get(construct_url(date.year, date.month, date.day)))
    curr_date = date
    day_adjusted = 0
    while len(data) == 0:
        if day_adjusted == go_back_days:
            raise Exception('went back '+ str(day_adjusted) + ' business days (from '+str(date)+' ), no yield data found.')

        curr_date = curr_date - timedelta(days=1)
        data = parse_xml(get(construct_url(curr_date.year, curr_date.month, curr_date.day)))
        #print(curr_date, data)
        if is_bday(curr_date):
            day_adjusted += 1
    return data

def get_yield_curve(year=None, month=None, day=None):
    if day:
        return get_yield_curve_bus_adj(datetime(year, month, day))
    return parse_xml(get(construct_url(year, month, day)))

def get_yield_curve_by_dates(dates):
     return [ get_yield_curve_bus_adj(dt) for dt in dates]
         

def parse_xml(xml_str):
    df = pd.DataFrame({ h:[] for h in field_mappings.values()})
    root = ElementTree.fromstring(xml_str)
    #last_updated = root.find('{http://www.w3.org/2005/Atom}updated').text
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        id = entry.find('{http://www.w3.org/2005/Atom}id').text
        dict_data = {}
        for y in entry.find('{http://www.w3.org/2005/Atom}content/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
            field = y.tag.replace('{http://schemas.microsoft.com/ado/2007/08/dataservices}', '')
            if field in field_mappings:
                dict_data[field_mappings[field]] = y.text
        df = df.append(dict_data, ignore_index=True)
    return df

