import cadquery as cq
from parts.cap import make_cap
from params import CarParams

# Generate the model
cap_model = make_cap()

# Optional: Export using the [CadQuery Exporters](https://cadquery.readthedocs.io)
# cq.exporters.export(cap_model, "my_part.step")

# Show in CQ-editor

show_object(cap_model, name="CapPipe")