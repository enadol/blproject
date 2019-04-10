#!python3
import json
from collections import OrderedDict

#para cambiar el formato del json con indents y crear el nuevo file reformateado
fh=json.loads(open('../2018-2019/bundesliga.json', 'r').read(), object_pairs_hook=OrderedDict)
fh2=json.dumps(fh, indent=4, sort_keys=True)
with open('../2018-2019/bl.json', 'w') as outfile:
    outfile.write(fh2)
    outfile.close()