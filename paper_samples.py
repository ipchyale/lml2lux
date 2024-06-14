import pandas as pd
from cromulent import model, vocab
import json

def record_label(rec):
    man = rec.Manufacturer
    bran = rec.Brand
    year = str(rec.Year)

    return f'{man} {bran} {year}'

def create_timespan(smp):
    year = smp.Year
    uncertain = smp.DateUncertain

    assert len(str(year))==4
    try:
        int(year)
    except:
        return None

    year = str(year)
    if uncertain:
        botb = f'{year - 5}-01-01T00:00:00Z'
        eote = f'{year + 5}-12-31T23:59:59Z'
    else:
        botb = f'{year}-01-01T00:00:00Z'
        eote = f'{year}-12-31T23:59:59Z'

    if uncertain:
        dns = f'circa {year}'
    else:
        dns = year

    return botb, eote, dns

def get_catalog_number(smp):
    pcn = str(smp['Catalog Number'])
    scn = smp.fillna('')['Secondary Catalog Number']

    return pcn + scn

def name_constructor(smp):
    man = smp.Manufacturer
    bran = smp.Brand
    year = str(smp.Year)

    return f'{man} {bran} Paper from {create_timespan(smp)[2]}'
    

#---------------------------------------------

df = pd.read_csv("export_06_05_24.csv", encoding='latin-1')
df = df.fillna('')

with open('lml.jsonl', 'w') as f:
    for i in df.index:

        smp = df.iloc[i]

        # PhotoID to URI
        paper = model.HumanMadeObject(ident=get_catalog_number(smp), label=record_label(smp))

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
        paper.identified_by = model.Identifier(content=get_catalog_number(smp))

        # Manufacturer = Group that made this thing
        # There needs to be a separate record with a Name
        prod.carried_out_by = model.Group(ident=smp.Manufacturer.lower(), label=smp.Manufacturer.lower())

        # But ... We need a name
        # Construct it from multiple fields?
        paper.identified_by = vocab.PrimaryName(content=name_constructor(smp))

        # Format = Description
        paper.referred_to_by = vocab.Description(content=smp.Format)

        # metatype: http://vocab.getty.edu/aat/300248479
        paper.referred_to_by = model.LinguisticObject(content=f'Box {smp.LocationBox}, Bag {smp.LocationBag}')

        # Not sure what to do about surface designation -- statement? Not comprehensible by itself
        # TODO: add a custom display label "Manufacturer Surface Designation" (or something)
        paper.referred_to_by = vocab.Note(content=smp.SurfaceDesignation2)

        # Texture, Reflectance, Color, Weight -- classifications
        # TODO - these need metatypes to convey the sort of classification
        paper.classified_as = model.Type(ident=f'texture/{smp.Texture2}')
        paper.classified_as = model.Type(ident=f'gloss/{smp.Reflectance2}')
        paper.classified_as = model.Type(ident=f'color/{smp.BaseColor2}')
        paper.classified_as = model.Type(ident=f'weight/{smp.Weight2}')

        # TODO: Brand -- yet another classification?
        js = model.factory.toJSON(paper)
        rec = json.dumps(js, indent=2)
        
        f.write(json.dumps(rec) + '\n')