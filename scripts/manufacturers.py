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

man_file_path = 'JSONL/manufacturers.jsonl'
bran_file_path = 'JSONL/brands.jsonl'
surf_file_path = 'JSONL/surfaces.jsonl'
backp_file_path = 'JSONL/backprints.jsonl'

# clear out the JSONL files
open(bran_file_path, 'w').close()
open(surf_file_path, 'w').close()
open(backp_file_path, 'w').close()

with open(man_file_path, 'w') as jsonl_file:
    for man in mans:
 
        thisman = df.loc[df.man == man]

        equivs = thisman.manid.unique()
        assert len(equivs) == 1
        equiv = equivs[0]
        
        if not pd.isna(equiv):
            continue

        mansafes = thisman.mansafe.unique()
        assert len(mansafes) == 1
        mansafe = f'MAN_{mansafes[0]}.json'

        manufacturer = model.Group(ident=f'https://paperbase.xyz/records/{mansafe}', label=man)
        manufacturer.identified_by = vocab.PrimaryName(content=man)
        manufacturer.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300160084", 
                                        label="Company")

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

            equivs = thisbran.branid.unique()
            assert len(equivs) == 1
            equiv = equivs[0]

            if not pd.isna(equiv):
                continue

            bransafes = thisbran.bransafe.unique()
            assert len(bransafes) == 1
            bransafe = f'BRAN_{bransafes[0]}_MAN_{mansafes[0]}.json'

            brand = model.Type(ident=f'https://paperbase.xyz/records/{bransafe}', label=f'{man} {bran}')
            brand.identified_by = vocab.PrimaryName(content=f'{man} {bran}')
            brand.broader = model.Type(ident="http://vocab.getty.edu/aat/300389735", label="Brand Name Materials")
            brand.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300028776", label="Trademark")

            cre = model.Creation()
            cre.carried_out_by = manufacturer
            brand.created_by = cre

            # Convert to JSON
            js = model.factory.toJSON(brand)
            add_record_to_jsonl(js, bran_file_path)

            # Write to individual JSON file
            filename = bransafe
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w') as individual_file:
                rec = json.dumps(js)
                individual_file.write(rec)

        # surfaces under this man
        surfs = thisman.s.loc[thisman.s.notnull()].unique()
        surfs = [item for item in surfs if item != '[not specified]']

        for surf in surfs:
            thissurf = thisman.loc[thisman.s == surf]

            surfsafes = thissurf.ssafe.unique()
            assert len(surfsafes) == 1
            surfsafe = f'SURF_{surfsafes[0]}_MAN_{mansafes[0]}.json'

            surface = model.Type(ident=f'https://paperbase.xyz/records/{surfsafe}', label=f'{man} {surf}')
            surface.identified_by = vocab.PrimaryName(content=f'{man} {surf}')
            surface.broader = model.Type(ident="http://vocab.getty.edu/aat/300375551", label="Brand Name Materials")

            cre = model.Creation()
            cre.carried_out_by = manufacturer
            surface.created_by = cre

            # Convert to JSON
            js = model.factory.toJSON(surface)
            add_record_to_jsonl(js, surf_file_path)

            # Write to individual JSON file
            filename = surfsafe
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w') as individual_file:
                rec = json.dumps(js)
                individual_file.write(rec)

        # backprints under this man
        backps = thisman.backp.loc[thisman.backp.notnull()].unique()

        for backp in backps:
            thisbackp = thisman.loc[thisman.backp == backp]

            backpsafes = thisbackp.backpsafe.unique()
            assert len(backpsafes) == 1
            backpsafe = f'BACKP_{backpsafes[0]}_MAN_{mansafes[0]}.json'

            backprint = model.VisualItem(ident=f'https://paperbase.xyz/records/{backpsafe}', label=f'{man} {backp} Backprint')
            backprint.identified_by = vocab.PrimaryName(content=f'{man} {backp} Backprint')
            backprint.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300438445", label="Wordmark")

            cre = model.Creation()
            cre.carried_out_by = manufacturer
            backprint.created_by = cre

            # Convert to JSON
            js = model.factory.toJSON(backprint)
            add_record_to_jsonl(js, backp_file_path)

            # Write to individual JSON file
            filename = backpsafe
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w') as individual_file:
                rec = json.dumps(js)
                individual_file.write(rec)