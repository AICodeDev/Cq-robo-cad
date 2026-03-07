import cadquery as cq

# Plate size
plate_x = 120
plate_y = 88
thickness = 8

# Hole specs
hole_dia = 4
padding = 2
spacing = hole_dia + padding + padding   # 6 mm

x_count = 15
y_count = 11

cut_length = 40
cut_width = 20
cut_depth = 3

plate = (
    cq.Workplane("XY")
    .rect(100, 60)
    .extrude(5)
    .faces(">Z")
    .workplane()
    .rect(cut_length, cut_width)
    .cutBlind(cut_depth)
)

#show_object(plate)

"""
plate = (
    cq.Workplane("XY")
    .rect(100, 60)
    .extrude(5)
    .faces(">Z")
    .workplane()
    .rect(40, 20)
    .vertices()
    .fillet(3)
    .cutThruAll()
)
"""

"""
plate = (
    plate
    .faces(">Z")
    .workplane()
    .rarray(spacing, spacing, x_count, y_count)
    .hole(hole_dia)
)
"""

show_object(plate)
