import pandas as pd
from cromulent import model, vocab
import json
import os

# Prevent serializer from crossing between records
vocab.add_linked_art_boundary_check()

output_dir = '/Users/damoncrockett/paperbase/lux/'
os.makedirs(output_dir, exist_ok=True)  

groups_file_path = 'JSONL/groups.jsonl'

with open(groups_file_path, 'w') as jsonl_file:
    lml_collection = model.Set(ident='https://paperbase.xyz/records/lmlcollection.json', label='Lens Media Lab Collection')
    lml_collection.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300025976", label="Collection")
    curating = model.Activity(label='Curating')
    curating.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300054277", label="Curating")
    curating.carried_out_by = model.Group(ident='https://paperbase.xyz/records/lml.json', label='Lens Media Lab')
    lml_collection.used_for = curating

    lml = model.Group(ident='https://paperbase.xyz/records/lml.json', label='Lens Media Lab')
    lml.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300443965", label="Laboratory")
    lml.member_of = model.Group(ident='https://paperbase.xyz/records/ipch.json', label='Institute for the Preservation of Cultural Heritage')

    ipch = model.Group(ident='https://paperbase.xyz/records/ipch.json', label='Institute for the Preservation of Cultural Heritage')
    ipch.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300343397", label="Research Institute")

    for record in [lml_collection, lml, ipch]:
        js = model.factory.toJSON(record)
        rec = json.dumps(js)
        jsonl_file.write(rec + "\n")

    # Write to individual JSON file
    for record in [lml_collection, lml, ipch]:
        filename = record.id.split('/')[-1]
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w') as individual_file:
            rec = json.dumps(js)
            individual_file.write(rec)