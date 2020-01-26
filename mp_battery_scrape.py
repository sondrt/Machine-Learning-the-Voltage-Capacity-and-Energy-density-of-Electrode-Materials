#!/usr/bin/python

import requests
from pandas import DataFrame


def scrape_batteries(working_ion="Li",
                     filter_property="average_voltage"):
    print("Scraping batteries from battery-explorer")
    print("Working ion: {}".format(working_ion))
    print("Filtering property: {}".format(filter_property))

    batteries = {}

    # Scrape over the full range of average voltage in the materials database
    for i in range(0, 150):
        url = 'https://www.materialsproject.org/batteries/search?query={{"working_ion":{{"$in":["{ion}"]}},"average_voltage":{{"$gte":{0},"$lte":{1}}}}}' \
            .format(-2.1 + i / 10.0, -1.9 + i / 10.0, ion=working_ion, property=filter_property)

        response = requests.get(url)
        response_batteries_list = response.json()

        assert response.status_code == 200
        assert isinstance(response_batteries_list, list)
        assert not isinstance(response_batteries_list, dict)

        for battery in response_batteries_list:
            batteries[battery["battid"]] = battery

        print('Found {} batteries and {} unique batteries so far. Searches run: {}' \
              .format(len(batteries), len(set(batteries)), i))

    return batteries


def fetch_battery_from_api(battery, apikey):
    print("Scraping battery {}".format(battery["battid"]))

    api_key_header = {"X-API-KEY": apikey}
    url = "https://www.materialsproject.org/rest/v2/battery/{}".format(battery["battid"])
    battery_get = requests.get(url, headers=api_key_header)
    response_obj = battery_get.json()

    assert battery_get.status_code == 200
    assert response_obj["valid_response"] == True

    battery_data = response_obj["response"][0]

    if len(battery_data["adj_pairs"]) > 2:
        print("Found a battery with too many materials, write code to handle it. {} material pairs found."
              .format(len(battery_data["adj_pairs"])))
        return None

    return (battery_data["battid"], battery_data)


def compose_battery_data(battery):
    print(battery)
    return [battery["battid"],
            battery["adj_pairs"][0]['id_discharge'],
            battery["adj_pairs"][0]['id_charge'],
            battery['reduced_cell_formula'],
            battery['type'],
            #battery['spacegroup']['symbol'],
            battery['average_voltage'],
            battery['capacity_grav'],
            battery['capacity_vol'],
            battery['energy_grav'],
            battery['energy_vol'],
            battery["adj_pairs"][0]['stability_charge'],
            battery["adj_pairs"][0]['stability_discharge']]



def scrape_battery_data_to_csv(working_ion, output_filename, apikey):
    print("Fetching batteries from Materials Project")

    batteries_list = scrape_batteries(working_ion=working_ion)

    print("Found {} batteries with working ion {}".format(len(batteries_list.values()), working_ion))

    battery_materials = dict(filter(
        lambda element: element != None,
        [fetch_battery_from_api(battery, apikey) for battery in batteries_list.values()]))

    print("Fetched {} battery data objects from rest api".format(len(battery_materials.values())))

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

    battery_data = [compose_battery_data(battery) for battery in list(battery_materials.values())]

    df = DataFrame.from_records(battery_data, columns=data_columns)

    print("Exporting selected battery data to file: {}".format(output_filename))
    df.to_csv(output_filename, index=False)


# Example for scraping all Mg-batteries and exporting them to mg_batteries.csv
#scrape_battery_data_to_csv("Mg", "mg_batteries.csv", "GKDHNwKre8uiowqhPh")

scrape_battery_data_to_csv("Li", "Li_batteries.csv", "GKDHNwKre8uiowqhPh")
