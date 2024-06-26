import pandas as pd
from cromulent import model, vocab
import json
import os

df = pd.read_pickle('notebooks/reconc.pkl')

# Prevent serializer from crossing between records
vocab.add_linked_art_boundary_check()

output_dir = '/Users/damoncrockett/paperbase/lux/'
os.makedirs(output_dir, exist_ok=True)  

xd_file_path = 'JSONL/texture_descriptors.jsonl'
gd_file_path = 'JSONL/gloss_descriptors.jsonl'
cd_file_path = 'JSONL/color_descriptors.jsonl'
td_file_path = 'JSONL/thickness_descriptors.jsonl'

# texture descriptors 
xds = df.xd.loc[df.xd.notnull()].unique()
xds = [item for item in xds if item != '[texture unspecified]']

with open(xd_file_path, 'w') as jsonl_file:
    for xd in xds:
        thisxd = df.loc[df.xd == xd]

        xdsafes = thisxd.xdsafe.unique()
        assert len(xdsafes) == 1
        xdsafe = f'XD_{xdsafes[0]}.json'

        texture_descriptor = model.Type(ident=f'https://paperbase.xyz/records/{xdsafe}', label=xd)
        texture_descriptor.identified_by = vocab.PrimaryName(content=xd)
        texture_descriptor.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300056362", label="Texture")

        # cre = model.Creation()
        # cre.carried_out_by = manufacturer
        # texture_descriptor.created_by = cre

        # Convert to JSON
        js = model.factory.toJSON(texture_descriptor)
        rec = json.dumps(js)
        jsonl_file.write(rec + "\n")
        
        # Write to individual JSON file
        filename = xdsafe
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w') as individual_file:
            rec = json.dumps(js)
            individual_file.write(rec)

# gloss descriptors 
gds = df.gd.loc[df.gd.notnull()].unique()
gds = [item for item in gds if item != '[gloss unspecified]']

with open(gd_file_path, 'w') as jsonl_file:
    for gd in gds:
        thisgd = df.loc[df.gd == gd]

        gdsafes = thisgd.gdsafe.unique()
        assert len(gdsafes) == 1
        gdsafe = f'GD_{gdsafes[0]}.json'

        gloss_descriptor = model.Type(ident=f'https://paperbase.xyz/records/{gdsafe}', label=gd)
        gloss_descriptor.identified_by = vocab.PrimaryName(content=gd)
        gloss_descriptor.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300179475", label="Reflectance")

        # cre = model.Creation()
        # cre.carried_out_by = manufacturer
        # gloss_descriptor.created_by = cre

        # Convert to JSON
        js = model.factory.toJSON(gloss_descriptor)
        rec = json.dumps(js)
        jsonl_file.write(rec + "\n")

        # Write to individual JSON file
        filename = gdsafe
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w') as individual_file:
            rec = json.dumps(js)
            individual_file.write(rec)

# color descriptors 
cds = df.cd.loc[df.cd.notnull()].unique()
cds = [item for item in cds if item != '[base color unspecified]']

with open(cd_file_path, 'w') as jsonl_file:
    for cd in cds:
        thiscd = df.loc[df.cd == cd]

        cdsafes = thiscd.cdsafe.unique()
        assert len(cdsafes) == 1
        cdsafe = f'CD_{cdsafes[0]}.json'

        color_descriptor = model.Type(ident=f'https://paperbase.xyz/records/{cdsafe}', label=cd)
        color_descriptor.identified_by = vocab.PrimaryName(content=cd)
        color_descriptor.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300080438", label="Color")

        # cre = model.Creation()
        # cre.carried_out_by = manufacturer
        # color_descriptor.created_by = cre

        # Convert to JSON
        js = model.factory.toJSON(color_descriptor)
        rec = json.dumps(js)
        jsonl_file.write(rec + "\n")

        # Write to individual JSON file
        filename = cdsafe
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w') as individual_file:
            rec = json.dumps(js)
            individual_file.write(rec)

# thickness descriptors 
tds = df.td.loc[df.td.notnull()].unique()
tds = [item for item in tds if item != '[weight unspecified]']

with open(td_file_path, 'w') as jsonl_file:
    for td in tds:
        thistd = df.loc[df.td == td]

        tdsafes = thistd.tdsafe.unique()
        assert len(tdsafes) == 1
        tdsafe = f'TD_{tdsafes[0]}.json'

        thickness_descriptor = model.Type(ident=f'https://paperbase.xyz/records/{tdsafe}', label=td)
        thickness_descriptor.identified_by = vocab.PrimaryName(content=td)
        thickness_descriptor.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300056240", label="Weight")

        # cre = model.Creation()
        # cre.carried_out_by = manufacturer
        # thickness_descriptor.created_by = cre

        # Convert to JSON
        js = model.factory.toJSON(thickness_descriptor)
        rec = json.dumps(js)
        jsonl_file.write(rec + "\n")

        # Write to individual JSON file
        filename = tdsafe
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w') as individual_file:
            rec = json.dumps(js)
            individual_file.write(rec)