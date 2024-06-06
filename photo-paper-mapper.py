
from cromulent import model, vocab
import json

# PhotoID to URI
paper = model.HumanMadeObject(ident="m538136167", label="Kodak Solio 1890")

# Year, DateUncertain to Prod/Date
prod = model.Production()
paper.produced_by = prod
ts = model.TimeSpan()
ts.begin_of_the_begin = "1890-01-01T00:00:00Z"
ts.end_of_the_end = "1890-12-31T23:59:59Z"
dn = vocab.DisplayName(content="circa 1890")
ts.identified_by = dn
prod.timespan = ts

# Catalog Number, Secondary Catalog Number
# No information about the thing with this number
# Smush it in as call number by merging
paper.identified_by = model.Identifier(content="996a")

# Manufacturer = Group that made this thing
# There needs to be a separate record with a Name
prod.carried_out_by = model.Group(ident="kodak", label="kodak")

# But ... We need a name
# Construct it from multiple fields?
paper.identified_by = vocab.PrimaryName(content="Kodak Solio Paper from circa 1890")

# Format = Description
paper.referred_to_by = vocab.Description(content="Not exposed - package open")

# metatype: http://vocab.getty.edu/aat/300248479
paper.referred_to_by = model.LinguisticObject(content="Box 21, Bag A")

# Not sure what to do about surface designation -- statement? Not comprehensible by itself
# TODO: add a custom display label "Manufacturer Surface Designation" (or something)
paper.referred_to_by = vocab.Note(content="VV")

# Texture, Reflectance, Color, Weight -- classifications
# TODO - these need metatypes to convey the sort of classification
paper.classified_as = model.Type(ident="texture/velvet")
paper.classified_as = model.Type(ident="reflectance/glossy")
paper.classified_as = model.Type(ident="color/pearly-white")
paper.classified_as = model.Type(ident="weight/cardboard")

# TODO: Brand -- yet another classification?
js = model.factory.toJSON(paper)
rec = json.dumps(js, indent=2)
print(rec)
