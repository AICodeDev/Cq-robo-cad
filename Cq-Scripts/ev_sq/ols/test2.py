import cadquery as cq

# Dimensions (mm)
length = 120
width = 88
base_thickness = 8


# Base plate
plate = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(base_thickness)
)

show_object(plate)

plate2 = (
    plate
    .faces(">Z")
    .workplane()
    .rect(84, 52)
    .cutThruAll()
)
show_object(plate2)
