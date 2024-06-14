import pandas as pd
from cromulent import model, vocab
import json

# df = pd.read_csv("sources/export_06_05_24.csv", encoding='latin-1')
# df = df.fillna('')

# Prevent serializer from crossing between records
vocab.add_linked_art_boundary_check()


# mans = df.Manufacturer.unique()

## Kodak
with open ('manufacturers.json', 'w') as f:
    kodak = model.Group(ident="company/kodak", label="Kodak")
    kodak.identified_by = vocab.PrimaryName(content="Kodak")
    kodak.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300160084", label="Company")
    # Other fields could go here too, like formation/dissolution, description etc.

    kodak.equivalent = model.Group(ident="<URI>", label="Kodak")

    # aat:300025969  = Corporation
    # aat:300160084  = Company

    js = model.factory.toJSON(kodak)
    rec = json.dumps(js, indent=2)
    f.write(rec)