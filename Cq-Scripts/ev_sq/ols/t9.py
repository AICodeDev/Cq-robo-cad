import cadquery as cq

# Plate size
plate_x = 120
plate_y = 88
thickness = 8

# Hole specs
hole_dia = 4
padding = 2
spacing = hole_dia + padding + padding   # 8 mm (not 6)

x_count = 15
y_count = 11

cut_length = 84
cut_width = 52

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
    
    FIXED: Returns plate centered at origin after extrusion
    """

    delta = base_thickness * (factor - 1.0)

    block_w = cells_x * cell
    block_h = cells_y * cell

    # Convert top-left grid to CadQuery center coordinates
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

    if delta > 0:
        # EXTRUDE: Create a new solid above the section
        extruded = (
            plate
            .faces(">Z")
            .workplane()
            .center(x_center, y_center)  # Move to the block center
            .rect(block_w, block_h)
            .extrude(delta)
        )
        return extruded
        
    elif delta < 0:
        # CUT: Remove material from the section
        cut = (
            plate
            .faces(">Z")
            .workplane()
            .center(x_center, y_center)  # Move to the block center
            .rect(block_w, block_h)
            .cutBlind(abs(delta))
        )
        return cut
        
    else:
        return plate


# ============================================
# BUILD STEP BY STEP
# ============================================

# STEP 1: Base plate
print("Creating base plate...")
plate = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(base_thickness)
)
show_object(plate, name="step1_base_plate")

# STEP 2: Add center cutout
print("Adding center cutout...")
plateCut = (
    plate
    .faces(">Z")
    .workplane()
    .rect(84, 52)
    .cutThruAll()
)
show_object(plateCut, name="step2_with_cutout")

# STEP 3: Increase thickness of front-left section
print("Increasing front-left section thickness...")
plateT = modify_grid_block_thickness(
    plateCut, 
    grid_x=0, 
    grid_y=3, 
    cells_x=2,
    cells_y=5, 
    factor=2.5,
    plate_x=plate_x,
    plate_y=plate_y,
    cell=8,
    base_thickness=base_thickness
)
show_object(plateT, name="step3_thick_section")

# STEP 4: Add holes (now properly centered)
print("Adding holes...")
plateHole = (
    plateT    
    .faces("<Z")  # Select BOTTOM face for drilling from below
    .workplane()
    .rarray(spacing, spacing, x_count, y_count)
    .hole(hole_dia)
)
show_object(plateHole, name="step4_final_with_holes")

# Show final result
show_object(plateHole, name="FINAL", options={"color": "lightblue"})

print("\nDone! Holes should now be properly centered.")
print(f"Spacing: {spacing}mm")
print(f"Grid: {x_count} x {y_count} holes")