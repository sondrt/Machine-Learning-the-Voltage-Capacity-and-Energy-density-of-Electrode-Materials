#!/usr/bin/python
from typing import Any

import json
import requests


def scrape_batteries(working_ion = "Mg",
                     filter_property="average_voltage"):
    print("Making 14 requests to scrape batteries")
    print("Working ion: {}".format(working_ion))
    print("Filtering property: {}".format(filter_property))

    results: List[Dict] = []

    for i in range(0, 30):
        url = 'https://www.materialsproject.org/batteries/search?query={{"working_ion":{{"$in":["{ion}"]}},"average_voltage":{{"$gte":{0},"$lte":{1}}}}}' \
            .format(-2.1 + i / 10.0, -1.9 + i / 10.0, ion=working_ion, property=filter_property)

        response = requests.get(url)

        assert response.status_code == 200
        assert not isinstance(response.json(), dict)

        results.extend(response.json())

        print("len(results))

    return results


print(scrape_batteries(working_ion="Li"))
# scrape_batteries(working_ion="Mg")
