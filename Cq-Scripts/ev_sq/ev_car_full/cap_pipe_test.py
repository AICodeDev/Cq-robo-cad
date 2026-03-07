import cadquery as cq
from parts.cap_pipe import make_cap_pipe
from params import CarParams

# Generate the model
cap_pipe_model = make_cap_pipe()

# Optional: Export using the [CadQuery Exporters](https://cadquery.readthedocs.io)
# cq.exporters.export(cap_model, "my_part.step")

# Show in CQ-editor

show_object(cap_pipe_model, name="cap_pipe_model")