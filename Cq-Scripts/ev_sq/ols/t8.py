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


def modify_grid_block_thickness(
    plate,
    grid_x,
    grid_y,
    cells_x=1,
    cells_y=1,
    plate_x=120,
    plate_y=88,
    cell=8,
    base_thickness=8,
    factor=1.0
):
    """
    Grid origin: TOP-LEFT corner of plate
    grid_x=0, grid_y=0 -> top-left cell
    """

    delta = base_thickness * (factor - 1.0)

    block_w = cells_x * cell
    block_h = cells_y * cell

    # 🔑 Convert top-left grid to CadQuery center coordinates
    x_center = (
        -plate_x / 2
        + grid_x * cell
        + block_w / 2
    )

    y_center = (
        plate_y / 2
        - grid_y * cell
        - block_h / 2
    )

    wp = (
        plate
        .faces(">Z")
        .workplane()
        .transformed(offset=(x_center, y_center, 0))
        .rect(block_w, block_h)
    )

    if delta > 0:
        plate = wp.extrude(delta)
        plate= plate.transformed(offset=(-x_center, -y_center, 0))

        return plate
    elif delta < 0:
        plate = wp.cutBlind(delta)
        return plate  
    else:
        return plate






# Base plate
plate = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(base_thickness)
)

#plate = modify_grid_thickness(plate, grid_x=2, grid_y=3, factor=2.0)
show_object(plate)

plateCut = (
    plate
    .faces(">Z")
    .workplane()
    .rect(84, 52)
    .cutThruAll()
)
show_object(plateCut)


plateT = modify_grid_block_thickness(plateCut, grid_x=0, grid_y=3, cells_x=2,cells_y=5, factor=2.5)
show_object(plateT)


def move_to_origin(solid, mode="center"):
    bb = solid.val().BoundingBox()

    if mode == "center":
        return solid.translate((
            -(bb.xmin + bb.xmax)/2,
            -(bb.ymin + bb.ymax)/2,
            -bb.zmin
        ))

    if mode == "topleft":
        return solid.translate((-bb.xmin, -bb.ymax, -bb.zmin))

plateT2 = plateT #move_to_origin(plateT)
show_object(plateT2)
plateHole2 = (
    plateT2    
  
    .faces("<Z")                  
    .workplane()
    
    .rarray(spacing, spacing, x_count, y_count)
    .hole(hole_dia)
)

show_object(plateHole2)



"""
plateHole = (
    plateT
    .workplane("XY")              
    .faces("<Z")      
    .workplane()
    .rarray(spacing, spacing, x_count, y_count)
    .hole(hole_dia)
)

show_object(plateHole)
"""