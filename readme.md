This repo contains processed and zipped ontology files for KBase hosted on GitHub for ease of loading using the folowing script.

```
import urllib
import zipfile
import json

ws = biokbase.narrative.clients.get('workspace')

def load_ont(prefix):
    urllib.urlretrieve ("https://github.com/JamesJeffryes/KBOntologies/blob/master/{}.json.zip?raw=true".format(prefix), "/tmp/{}.json.zip".format(prefix))
    ws = biokbase.narrative.clients.get('workspace')
    data = json.loads(zipfile.ZipFile('/tmp/{}.json.zip'.format(prefix)).read('{}.json'.format(prefix)))
    print(ws.save_objects({
        'workspace': 'KBaseOntology',
         "objects": [{
             "type": "KBaseOntology.OntologyDictionary",
             "data": data,
             "name": '{}_ontology'.format(prefix)
         }]}))
```
