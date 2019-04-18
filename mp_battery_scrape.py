#!/usr/bin/python

import requests
from pandas import DataFrame
from bs4 import BeautifulSoup


def scrape_batteries(working_ion ="Mg",
                     filter_property="average_voltage"):
    print("Scraping batteries from battery-explorer")
    print("Working ion: {}".format(working_ion))
    print("Filtering property: {}".format(filter_property))

    batteries = {}

    for i in range(0, 17):
        url = 'https://www.materialsproject.org/batteries/search?query={{"working_ion":{{"$in":["{ion}"]}},"average_voltage":{{"$gte":{0},"$lte":{1}}}}}' \
            .format(-2.1 + i / 10.0, -1.9 + i / 10.0, ion=working_ion, property=filter_property)

        response = requests.get(url)
        response_batteries_list = response.json()

        assert response.status_code == 200
        assert isinstance(response_batteries_list, list)
        assert not isinstance(response_batteries_list, dict)

        for battery in response_batteries_list:
            batteries[battery["battid"]] = battery

        print('Found {} batteries and {} unique batteries so far. Searches run: {}'\
            .format(len(batteries), len(set(batteries)), i))

    return batteries


def scrape_battery_materials(battery):

    print("Scraping battery {}".format(battery["battid"]))

    url = "https://www.materialsproject.org/batteries/{}".format(battery["battid"])
    battery_get = requests.get(url, cookies={"sessionid" : sessionid})

    assert battery_get.status_code == 200

    battery_soup = BeautifulSoup(battery_get.text, "html.parser")

    material_spans = battery_soup("span", attrs={"class": "label-bg"})

    if len(material_spans) > 2:
        print("Found a battery with too many materials, write code to handle it.\n" \
                                           "\n" \
                                           "{}".format(material_spans))
        return None

    return (battery["battid"], dict(map(
                (lambda span_tag:( span_tag.string.split()[-1],  # charged / discharged
                                   span_tag.parent.parent.a['href'].split('/')[-1])),  # <material-id>
                material_spans)))


def compose_battery_data(battery, battery_data):
    return [battery[0],
            battery[1]['discharged'],
            battery[1]['charged'],
            battery_data['reduced_cell_formula'],
            battery_data['type'],
            battery_data['spacegroup']['symbol'],
            battery_data['average_voltage'],
            battery_data['capacity_grav'],
            battery_data['capacity_vol'],
            battery_data['specific_e_wh/kg'],
            battery_data['e_density_wh/l'],
            battery_data['stability_charge'],
            battery_data['stability_discharge']]


sessionid = "on8w86ghahhxkdqu1xmtv8pfkgf0p7j4"
assert not sessionid == "", "sessionid for materialsproject cannot be empty, insert it in the string after extracting it from your logged in user"

li_batteries = scrape_batteries(working_ion="Li")

print(li_batteries)

li_battery_materials = dict([scrape_battery_materials(battery) for battery in li_batteries.values()])

print(li_battery_materials)

data_columns = ['Battid',
                'Discharged_ID',
                'Charged_ID',
                'Reduced_Cell_Formula',
                'Type',
                'Spacegroup',
                'Average_Voltage',
                'Capacity_Grav',
                'Capacity_Vol',
                'Specific_E_Wh/kg',
                'E Density Wh/l',
                'Stability Charge',
                'Stability Discharge']

battery_data = [compose_battery_data(battery, li_batteries[battery[0]])
                for battery in li_battery_materials.items()]

df = DataFrame.from_records(battery_data, columns=data_columns)

print("Printing CSV")
print(df.to_csv(index=False))
# mg_batteries = scrape_batteries(working_ion="Mg")
