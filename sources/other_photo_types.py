from cromulent import model, vocab
import json

# Prevent serializer from crossing between records
vocab.add_linked_art_boundary_check()

## Kodak

kodak = model.Group(ident="company/kodak", label="Kodak")
kodak.identified_by = vocab.PrimaryName(content="Kodak")
kodak.classified_as = model.Type(id="http://vocab.getty.edu/aat/300160084", label="Company")
# Other fields could go here too, like formation/dissolution, description etc.

# aat:300025969  = Corporation
# aat:300160084  = Company

## Velox Brand
velox = model.Type(ident="brand/velox", label="Velox")
velox.identified_by = vocab.PrimaryName(content="Velox")
velox.broader = model.Type(ident="http://vocab.getty.edu/aat/300375551", label="Brand Name Materials")
velox.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300028776", label="Trademark")
cre = model.Creation()
cre.carried_out_by = kodak
velox.created_by = cre
# dates and places could go here too


## Reflectance
sg = model.Type(ident="reflectance/semi_glossy", label="Semi Glossy")
sg.identified_by = vocab.PrimaryName(content="Semi Glossy")
sg.classified_as = model.Type(ident="http://vocab.getty.edu/aat/300179475", label="Reflectance")

# reflectance: http://vocab.getty.edu/aat/300179475
# texture: http://vocab.getty.edu/aat/300056362
# density:  http://vocab.getty.edu/aat/300056237 = weight?
# weight: http://vocab.getty.edu/aat/300056240 = weight?
# color: http://vocab.getty.edu/aat/300080438

# photographic paper: http://vocab.getty.edu/aat/300014190
# packaging: http://vocab.getty.edu/aat/300055100


## Visual Item of Logo

a01 = model.VisualItem(ident="logo/a01", label="Agfa Logo 01")
a01.identified_by = vocab.PrimaryName(content="Agfa Logo 01")
cre = model.Creation()
cre.carried_out_by = model.Group(ident="company/agfa", label="Agfa")
a01.created_by = cre
# dates and places

# and images

# and descriptions
