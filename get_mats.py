#!/usr/bin/python

import requests

for i in range(0, 140):
    req = 'https://www.materialsproject.org/batteries/search?query={{"working_ion":{{"$in":["Li"]}},"average_voltage":{{"$gte":{0},"$lte":{1}}}}}'.format(-2.1 + i/10.0, -1.9 + i/10.0)
    print(requests.get(req).text)
