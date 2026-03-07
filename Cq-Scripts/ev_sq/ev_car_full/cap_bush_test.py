import cadquery as cq
from parts.cap_bush import make_cap_bush
from params import CarParams

# Generate the model
cap_bush_model = make_cap_bush()

# Optional: Export using the [CadQuery Exporters](https://cadquery.readthedocs.io)
# cq.exporters.export(cap_model, "my_part.step")

# Show in CQ-editor

show_object(cap_bush_model, name="cap_bush_model")