#!/usr/bin/python

import requests


def scrape_batteries(working_ion="Mg",
                     filter_property="average_voltage"):
    print("Making 14 requests to scrape batteries")
    print("Working ion: {}".format(working_ion))
    print("Filtering property: {}".format(filter_property))
    
    for i in range(0, 14):
        req = 'https://www.materialsproject.org/batteries/search?query={{"working_ion":{{"$in":["{ion}"]}},"average_voltage":{{"$gte":{0},"$lte":{1}}}}}' \
            .format(-2.1 + i / 10.0, -1.9 + i / 10.0, ion=working_ion, property=filter_property)
        print(requests.get(req).text)


scrape_batteries(working_ion="Li")
