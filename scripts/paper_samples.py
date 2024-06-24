import pandas as pd
from cromulent import model, vocab
import json
import os

def record_label(rec):
    man = rec.man
    bran = rec.bran
    year = str(rec.year)

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
    man = smp.man
    bran = smp.bran

    return f'{man} {bran} Paper from {create_timespan(smp)[2]}'

#---------------------------------------------

df = pd.read_pickle('notebooks/reconc.pkl')

# Prevent serializer from crossing between records
vocab.add_linked_art_boundary_check()

with open('JSONL/paper_samples.jsonl', 'w') as f:
    for i in df.index:

        smp = df.iloc[i]

        # PhotoID to URI
        paper = model.HumanMadeObject(ident=smp['cat'], label=record_label(smp))

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

        # Catalog Number, Secondary Catalog Number
        # No information about the thing with this number
        # Smush it in as call number by merging
        paper.identified_by = model.Identifier(content=smp['cat'])

        # Manufacturer = Group that made this thing
        # There needs to be a separate record with a Name
        prod.carried_out_by = model.Group(ident=f'https://paperbase.xyz/records/MAN_{smp.mansafe}.json', label=smp.man)

        # But ... We need a name
        # Construct it from multiple fields?
        paper.identified_by = vocab.PrimaryName(content=name_constructor(smp))

        # Format = Description
        # paper.referred_to_by = vocab.Description(content=smp.Format)
        if smp.storfor == 'Package only':
            paper.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300055100", label="Packaging")
        else:
            paper.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300014190", label="Photographic Paper")

        if smp.storfor != 'Sample book':
            # metatype: http://vocab.getty.edu/aat/300248479
            paper.referred_to_by = model.LinguisticObject(content=f'Box {smp.locbox}, Bag {smp.locbag}')

        # Not sure what to do about surface designation -- statement? Not comprehensible by itself
        # TODO: add a custom display label "Manufacturer Surface Designation" (or something)
        #paper.referred_to_by = vocab.Note(content=smp.SurfaceDesignation2)

        # Texture, Reflectance, Color, Weight -- classifications
        # TODO - these need metatypes to convey the sort of classification
        paper.classified_as = model.Type(ident=f'https://paperbase.xyz/records/BRAN_{smp.bransafe}_MAN_{smp.mansafe}.json', label=f'{smp.man} {smp.bran}')
        paper.classified_as = model.Type(ident=f'https://paperbase.xyz/records/SURF_{smp.ssafe}_MAN_{smp.mansafe}.json', label=f'{smp.man} {smp.s}')
        paper.classified_as = model.Type(ident=f'https://paperbase.xyz/records/XD_{smp.xdsafe}_MAN_{smp.mansafe}.json', label=f'{smp.man} {smp.xd}')
        paper.classified_as = model.Type(ident=f'https://paperbase.xyz/records/GD_{smp.gdsafe}_MAN_{smp.mansafe}.json', label=f'{smp.man} {smp.gd}')
        paper.classified_as = model.Type(ident=f'https://paperbase.xyz/records/CD_{smp.cdsafe}_MAN_{smp.mansafe}.json', label=f'{smp.man} {smp.cd}')
        paper.classified_as = model.Type(ident=f'https://paperbase.xyz/records/TD_{smp.tdsafe}_MAN_{smp.mansafe}.json', label=f'{smp.man} {smp.td}')

        paper.classified_as = model.Type(ident=smp.processlink, label=smp.processname)

        paper.shows = model.VisualItem(ident=f'https://paperbase.xyz/records/BACKP_{smp.backpsafe}_MAN_{smp.mansafe}.json', label=f'{smp.man} {smp.backp}')
        
        js = model.factory.toJSON(paper)
        rec = json.dumps(js)
        f.write(rec + '\n')