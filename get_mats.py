#!/usr/bin/python

import requests
from bs4 import BeautifulSoup


def scrape_batteries(working_ion ="Mg",
                     filter_property="average_voltage"):
    print("Scraping batteries from battery-explorer")
    print("Working ion: {}".format(working_ion))
    print("Filtering property: {}".format(filter_property))

    batteries = {}

    for i in range(0, 30):
        url = 'https://www.materialsproject.org/batteries/search?query={{"working_ion":{{"$in":["{ion}"]}},"average_voltage":{{"$gte":{0},"$lte":{1}}}}}' \
            .format(-2.1 + i / 10.0, -1.9 + i / 10.0, ion=working_ion, property=filter_property)

        response = requests.get(url)
        response_batteries_list = response.json()

        assert response.status_code == 200
        assert isinstance(response_batteries_list, list)
        assert not isinstance(response_batteries_list, dict)

        for battery in response_batteries_list:
            batteries[battery["battid"]] = battery

        print(len(batteries))
        print(len(set(batteries)))

    return batteries

def scrape_battery_materials(batteries):

    print("Scraping battery info")

    battery_materials = {}

    for battery in batteries:
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
            continue

        battery_materials.update(
            map((lambda span_tag:
                 (battery["battid"] + '-' + span_tag.string.split()[-1], # <battid>-charged / <battid>-discharged
                  span_tag.parent.parent.a['href'].split('/')[-1])), # <material-id>
                material_spans))

    return battery_materials

sessionid = "on8w86ghahhxkdqu1xmtv8pfkgf0p7j4"
assert not sessionid == "", "sessionid for materialsproject cannot be empty, insert it in the string after extracting it from your logged in user"

li_batteries = scrape_batteries(working_ion="Li")

# print(li_batteries)

li_battery_materials = scrape_battery_materials(list(li_batteries.values()))

print(li_battery_materials)
# mg_batteries = scrape_batteries(working_ion="Mg")
