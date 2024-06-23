import pandas as pd
from cromulent import model, vocab
import json
import os

def add_record_to_jsonl(data, filename):
    with open(filename, "a") as file:
        json_record = json.dumps(data)
        file.write(json_record + "\n")

df = pd.read_pickle('notebooks/reconc.pkl')

# Prevent serializer from crossing between records
vocab.add_linked_art_boundary_check()

mans = df.man.loc[df.man.notnull()].unique()
mans = [item for item in mans if item != '[Indeterminate]']

output_dir = '/Users/damoncrockett/paperbase/lux/'
os.makedirs(output_dir, exist_ok=True)  

man_file_path = 'manufacturers.jsonl'
bran_file_path = 'brands.jsonl'

with open(man_file_path, 'w') as jsonl_file:
    for man in mans:

        thisman = df.loc[df.man == man]

        mansafes = thisman.mansafe.unique()
        assert len(mansafes) == 1
        mansafe = f'MAN_{mansafes[0]}.json'

        manufacturer = model.Group(ident=f'https://paperbase.xyz/records/{mansafe}', label=man)
        manufacturer.identified_by = vocab.PrimaryName(content=man)
        manufacturer.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300160084", 
                                        label="Company")
       
        equivs = thisman.manid.unique()
        assert len(equivs) == 1
        equiv = equivs[0]
        
        if not pd.isna(equiv):
            manufacturer.equivalent = model.Group(ident=equiv, label=man)

        # Convert to JSON
        js = model.factory.toJSON(manufacturer)
        rec = json.dumps(js)
        
        # Write to JSONL file
        jsonl_file.write(rec + '\n')
        
        # Write to individual JSON file
        filename = mansafe
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w') as individual_file:
            individual_file.write(rec)

        # brans under this man
        brans = thisman.bran.loc[thisman.bran.notnull()].unique()
        brans = [item for item in brans if item != '[Indeterminate]']

        for bran in brans:
            thisbran = thisman.loc[thisman.bran == bran]

            bransafes = thisbran.bransafe.unique()
            assert len(bransafes) == 1
            bransafe = f'BRAN_{bransafes[0]}_MAN_{mansafes[0]}.json'

            brand = model.Type(ident=f'https://paperbase.xyz/records/{bransafe}', label=bran)
            brand.identified_by = vocab.PrimaryName(content=bran)
            brand.broader = model.Type(ident="http://vocab.getty.edu/aat/300375551", label="Brand Name Materials")
            brand.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300028776", label="Trademark")

            cre = model.Creation()
            cre.carried_out_by = manufacturer
            brand.created_by = cre

            equivs = thisbran.branid.unique()
            assert len(equivs) == 1
            equiv = equivs[0]

            if not pd.isna(equiv):
                brand.equivalent = model.Group(ident=equiv, label=bran)

            # Convert to JSON
            js = model.factory.toJSON(brand)
            add_record_to_jsonl(js, bran_file_path)

            # Write to individual JSON file
            filename = bransafe
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w') as individual_file:
                rec = json.dumps(js)
                individual_file.write(rec)