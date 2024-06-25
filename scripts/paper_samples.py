import pandas as pd
from cromulent import model, vocab
import json
import os

def record_label(smp):
    man = smp.fillna('[Indeterminate]').man
    bran = smp.bran
    year = str(smp.year)

    return f'{man} {bran} {year}'

def create_timespan(smp):
    year = smp.year
    uncertain = smp.circa

    assert len(str(year))==4
    try:
        int(year)
    except:
        return None

    if uncertain:
        botb = f'{year - 5}-01-01T00:00:00Z'
        eote = f'{year + 5}-12-31T23:59:59Z'
    else:
        botb = f'{year}-01-01T00:00:00Z'
        eote = f'{year}-12-31T23:59:59Z'

    if uncertain:
        dns = f'circa {year}'
    else:
        dns = str(year)

    return botb, eote, dns

def name_constructor(smp):
    man = smp.fillna('[Indeterminate]').man
    bran = smp.bran

    return f'{man} {bran} Paper from {create_timespan(smp)[2]}'

#---------------------------------------------

df = pd.read_pickle('notebooks/reconc.pkl')

# Prevent serializer from crossing between records
vocab.add_linked_art_boundary_check()

with open('JSONL/paper_samples.jsonl', 'w') as f:
    for i in df.index:

        smp = df.iloc[i]
        catalog = smp['cat']

        # PhotoID to URI
        paper = model.HumanMadeObject(ident=f'https://paperbase.xyz/records/PS_{catalog}', label=record_label(smp))

        # Year, DateUncertain to Prod/Date
        prod = model.Production()
        paper.produced_by = prod
        ts = model.TimeSpan()
        botb, eote, dns = create_timespan(smp)
        ts.begin_of_the_begin = botb
        ts.end_of_the_end = eote
        dn = vocab.DisplayName(content=dns)
        ts.identified_by = dn
        prod.timespan = ts

        # paper.classified_as = model.Type(ident=smp.processlink, label=smp.processname)

        # Catalog Number, Secondary Catalog Number
        # No information about the thing with this number
        # Smush it in as call number by merging
        paper.identified_by = model.Identifier(content=catalog)

        # Manufacturer = Group that made this thing
        # There needs to be a separate record with a Name
        if smp.fillna('[Indeterminate]').man != '[Indeterminate]':
            if pd.isna(smp.manid):
                prod.carried_out_by = model.Group(ident=f'https://paperbase.xyz/records/MAN_{smp.mansafe}.json', label=smp.man)
            else:
                prod.carried_out_by = model.Group(ident=smp.manid, label=smp.man)

        # But ... We need a name
        # Construct it from multiple fields?
        paper.identified_by = vocab.PrimaryName(content=name_constructor(smp))

        # Format = Description
        # paper.referred_to_by = vocab.Description(content=smp.Format)
        if not pd.isna(smp.storfor):
            if smp.storfor == 'Package only':
                paper.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300055100", label="Packaging")
            else:
                paper.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300014190", label="Photographic Paper")

            if all([smp.storfor != 'Sample book', not pd.isna(smp.locbox), not pd.isna(smp.locbag)]):
                # metatype: http://vocab.getty.edu/aat/300248479
                paper.referred_to_by = model.LinguisticObject(content=f'Box {smp.locbox}, Bag {smp.locbag}')

        # TODO: add a custom display label "Manufacturer Surface Designation" (or something)

        # Texture, Reflectance, Color, Weight -- classifications
        # TODO - these need metatypes to convey the sort of classification
        
        if smp.bran != '[Indeterminate]':
            if pd.isna(smp.branid):
                paper.classified_as = model.Type(ident=f'https://paperbase.xyz/records/BRAN_{smp.bransafe}_MAN_{smp.mansafe}.json', label=f'{smp.man} {smp.bran}')
            else:
                paper.classified_as = model.Type(ident=smp.branid, label=smp.bran)
        
        if smp.fillna('[not specified]').s != '[not specified]':
            paper.classified_as = model.Type(ident=f'https://paperbase.xyz/records/SURF_{smp.ssafe}_MAN_{smp.mansafe}.json', label=f'{smp.man} {smp.s}')
        
        if smp.xd != '[texture unspecified]':
            paper.classified_as = model.Type(ident=f'https://paperbase.xyz/records/XD_{smp.xdsafe}.json', label=f'{smp.xd}')

        if smp.gd != '[gloss unspecified]':
            paper.classified_as = model.Type(ident=f'https://paperbase.xyz/records/GD_{smp.gdsafe}.json', label=f'{smp.gd}')

        if smp.cd != '[base color unspecified]':
            paper.classified_as = model.Type(ident=f'https://paperbase.xyz/records/CD_{smp.cdsafe}.json', label=f'{smp.cd}')

        if smp.td != '[weight unspecified]':
            paper.classified_as = model.Type(ident=f'https://paperbase.xyz/records/WD_{smp.tdsafe}.json', label=f'{smp.td}')

        if not pd.isna(smp.backp):
            paper.shows = model.VisualItem(ident=f'https://paperbase.xyz/records/BACKP_{smp.backpsafe}_MAN_{smp.mansafe}.json', label=f'{smp.man} {smp.backp}')
        
        js = model.factory.toJSON(paper)
        rec = json.dumps(js)
        f.write(rec + '\n')

        # TODO: still need individual files for each record