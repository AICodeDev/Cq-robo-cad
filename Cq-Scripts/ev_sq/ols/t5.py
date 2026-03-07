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

cut_length = 84
cut_width = 52
cut_depth = 3



# Dimensions (mm)
length = 120
width = 88
base_thickness = 8

def modify_grid_thickness(
    plate,
    grid_x,
    grid_y,
    cell=8,
    base_thickness=8,
    factor=1.0
):
    """
    Modify thickness of a single 8x8 grid cell
    factor < 1.0  -> intrude (cut)
    factor > 1.0  -> extrude (add)
    """

    delta = base_thickness * (factor - 1.0)

    wp = (
        plate
        .faces(">Z")
        .workplane()
        .transformed(offset=(grid_x * cell, grid_y * cell, 0))
        .rect(cell, cell)
    )

    if delta > 0:
        return wp.extrude(delta)
    elif delta < 0:
        return wp.cutBlind(delta)
    else:
        return plate



# Base plate
plate = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(base_thickness)
)

#plate = modify_grid_thickness(plate, grid_x=2, grid_y=3, factor=2.0)

plateV = modify_grid_thickness(plate, grid_x=2, grid_y=2, factor=0.5)


show_object(plateV)
"""
plateCut = (
    plate
    .faces(">Z")
    .workplane()
    .rect(84, 52)
    .cutThruAll()
)
show_object(plateCut)





plateHole = (
    plateCut
    .faces(">Z")
    .workplane()
    .rarray(spacing, spacing, x_count, y_count)
    .hole(hole_dia)
)

show_object(plateHole)
"""