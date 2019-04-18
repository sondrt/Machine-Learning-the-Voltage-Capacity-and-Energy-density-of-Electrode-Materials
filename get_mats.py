#!/usr/bin/python
from typing import Any

import json
import requests


def scrape_battery_list(working_ion ="Mg",
                        filter_property="average_voltage"):
    print("Making 14 requests to scrape batteries")
    print("Working ion: {}".format(working_ion))
    print("Filtering property: {}".format(filter_property))

    battery_materials = {}

    for i in range(0, 15):
        url = 'https://www.materialsproject.org/batteries/search?query={{"working_ion":{{"$in":["{ion}"]}},"average_voltage":{{"$gte":{0},"$lte":{1}}}}}' \
            .format(-2.1 + i / 10.0, -1.9 + i / 10.0, ion=working_ion, property=filter_property)

        response = requests.get(url)
        response_batteries_list = response.json()

        assert response.status_code == 200
        assert isinstance(response_batteries_list, list)
        assert not isinstance(response_batteries_list, dict)

        for battery in response_batteries_list:
            battery_materials[battery["battid"]] = battery

        print(len(battery_materials))
        print(len(set(battery_materials)))

    return list(battery_materials.values())


li_batteries = scrape_battery_list(working_ion="Li")

print(li_batteries)
# mg_batteries = scrape_batteries(working_ion="Mg")
