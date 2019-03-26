#key: GKDHNwKre8uiowqhPh
from pymatgen.ext.matproj import MPRester
import json
from pprint import pprint
 
#mvc_ids = dict()
#mvc_file = open("mvc_file",'w+')

with MPRester("GKDHNwKre8uiowqhPh") as m:
	mvc_cif = (m.query(criteria={"task_id": {"$regex":"mvc-"}}, properties = ["task_id","cif"]))


for mvc in mvc_cif:
    mvc_raw = json.dumps(mvc["cif"])
    mvc_bytes = bytes(mvc_raw, "utf-8")
    mvc_unescaped = mvc_bytes.decode("unicode_escape")
#    print(mvc_unescaped)	
    with open(mvc['task_id'],'w+') as f:
	    json.dump(mvc_unescaped, f)



#for key in mvc_cif:
























