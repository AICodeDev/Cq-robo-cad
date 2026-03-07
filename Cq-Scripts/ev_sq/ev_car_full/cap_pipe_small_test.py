import cadquery as cq
from parts.cap_small_pipe import make_cap_small_pipe
from params import CarParams

# Generate the model
model = make_cap_small_pipe()

# Optional: Export using the [CadQuery Exporters](https://cadquery.readthedocs.io)
# cq.exporters.export(cap_model, "my_part.step")

# Show in CQ-editor

show_object(model, name="small_long_pipe")