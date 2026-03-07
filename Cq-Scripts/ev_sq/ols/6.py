import cadquery as cq

# ============================================
# MODULAR FUNCTIONS
# ============================================

def create_base_plate(length, width, thickness, cutout_length, cutout_width):
    """
    Create base plate with center rectangular cutout.
    Start with full thickness, we'll reduce sections later.
    """
    # Create the plate
    plate = cq.Workplane("XY").box(length, width, thickness)
    
    # Add center cutout
    plate = (plate.faces(">Z").workplane()
             .rect(cutout_length, cutout_width)
             .cutThruAll())
    
    return plate


def reduce_section_thickness(plate, section_x, section_y, section_length, 
                             section_width, original_thickness, new_thickness):
    """
    Reduce the thickness of a specific section by cutting from the top.
    
    Parameters:
    -----------
    plate : CadQuery object
    section_x : float - X position of section center
    section_y : float - Y position of section center
    section_length : float - length of section
    section_width : float - width of section
    original_thickness : float - starting thickness
    new_thickness : float - desired final thickness
    """
    # Calculate how much to cut
    cut_depth = original_thickness - new_thickness
    
    if cut_depth <= 0:
        return plate  # No cutting needed
    
    # Create a box to cut from the top
    cut_box = (cq.Workplane("XY")
               .workplane(offset=original_thickness/2)
               .center(section_x, section_y)
               .rect(section_length, section_width)
               .extrude(cut_depth))
    
    # Subtract from plate
    result = plate.cut(cut_box)
    
    return result


def add_holes(plate, plate_length, plate_width, max_thickness,
              hole_center_from_edge, hole_diameter, hole_spacing):
    """
    Add simple grid of holes through the maximum thickness.
    Holes go all the way through regardless of section thickness.
    """
    hole_positions = []
    
    start_x = -plate_length/2 + hole_center_from_edge
    start_y = -plate_width/2 + hole_center_from_edge
    end_x = plate_length/2 - hole_center_from_edge
    end_y = plate_width/2 - hole_center_from_edge
    
    x = start_x
    while x <= end_x:
        y = start_y
        while y <= end_y:
            hole_positions.append((x, y))
            y += hole_spacing
        x += hole_spacing
    
    # Drill holes from top
    result = plate.faces(">Z").workplane()
    for pos in hole_positions:
        result = result.pushPoints([pos]).hole(hole_diameter, max_thickness)
    
    return result


# ============================================
# CONFIGURATION
# ============================================

# Plate dimensions
PLATE_LENGTH = 120          # mm
PLATE_WIDTH = 88            # mm
BASE_THICKNESS = 20         # mm - start with 20mm for all sections

# Center cutout
CUTOUT_LENGTH = 68          # mm
CUTOUT_WIDTH = 52           # mm

# Holes
HOLE_CENTER_FROM_EDGE = 4   # mm
HOLE_DIAMETER = 4           # mm
HOLE_SPACING = 8            # mm

# Section thicknesses (8 sections total)
# 4 corners + 4 middles (front, back, left, right)
CORNER_THICKNESS = 8        # mm - 4 corner sections
FRONT_MIDDLE_THICKNESS = 20 # mm - front middle (keep full)
BACK_MIDDLE_THICKNESS = 8   # mm - back middle
LEFT_MIDDLE_THICKNESS = 4   # mm - left middle (half thickness)
RIGHT_MIDDLE_THICKNESS = 8  # mm - right middle

# ============================================
# BUILD STEP BY STEP
# ============================================

# Calculate section dimensions
# Divide plate into 3x3 grid (corners and middles)
section_length = PLATE_LENGTH / 3
section_width = PLATE_WIDTH / 3

# STEP 1: Create base plate with full thickness
print("STEP 1: Creating base plate with cutout...")
chassis = create_base_plate(
    PLATE_LENGTH, 
    PLATE_WIDTH, 
    BASE_THICKNESS,
    CUTOUT_LENGTH,
    CUTOUT_WIDTH
)
show_object(chassis, name="step1_base_plate")

# STEP 2: Reduce corner thicknesses
print("STEP 2: Reducing corner thicknesses...")

# Front-left corner
chassis = reduce_section_thickness(
    chassis,
    -PLATE_LENGTH/3,    # X position
    -PLATE_WIDTH/3,     # Y position
    section_length,
    section_width,
    BASE_THICKNESS,
    CORNER_THICKNESS
)

# Front-right corner
chassis = reduce_section_thickness(
    chassis,
    -PLATE_LENGTH/3,
    PLATE_WIDTH/3,
    section_length,
    section_width,
    BASE_THICKNESS,
    CORNER_THICKNESS
)

# Back-left corner
chassis = reduce_section_thickness(
    chassis,
    PLATE_LENGTH/3,
    -PLATE_WIDTH/3,
    section_length,
    section_width,
    BASE_THICKNESS,
    CORNER_THICKNESS
)

# Back-right corner
chassis = reduce_section_thickness(
    chassis,
    PLATE_LENGTH/3,
    PLATE_WIDTH/3,
    section_length,
    section_width,
    BASE_THICKNESS,
    CORNER_THICKNESS
)

show_object(chassis, name="step2_corners_reduced")

# STEP 3: Reduce front middle section (keep at 20mm - no reduction)
print("STEP 3: Front middle (keeping full thickness 20mm)...")
# No reduction needed for front middle
show_object(chassis, name="step3_front_middle")

# STEP 4: Reduce back middle section
print("STEP 4: Reducing back middle thickness...")
chassis = reduce_section_thickness(
    chassis,
    PLATE_LENGTH/3,
    0,
    section_length,
    section_width,
    BASE_THICKNESS,
    BACK_MIDDLE_THICKNESS
)
show_object(chassis, name="step4_back_middle")

# STEP 5: Reduce left middle section (to 4mm)
print("STEP 5: Reducing left middle thickness to 4mm...")
chassis = reduce_section_thickness(
    chassis,
    0,
    -PLATE_WIDTH/3,
    section_length,
    section_width,
    BASE_THICKNESS,
    LEFT_MIDDLE_THICKNESS
)
show_object(chassis, name="step5_left_middle")

# STEP 6: Reduce right middle section
print("STEP 6: Reducing right middle thickness...")
chassis = reduce_section_thickness(
    chassis,
    0,
    PLATE_WIDTH/3,
    section_length,
    section_width,
    BASE_THICKNESS,
    RIGHT_MIDDLE_THICKNESS
)
show_object(chassis, name="step6_right_middle")

# STEP 7: Add holes AFTER all thickness reductions
print("STEP 7: Adding holes through all sections...")
chassis = add_holes(
    chassis,
    PLATE_LENGTH,
    PLATE_WIDTH,
    BASE_THICKNESS,
    HOLE_CENTER_FROM_EDGE,
    HOLE_DIAMETER,
    HOLE_SPACING
)
show_object(chassis, name="step7_final_with_holes")

# Final result
show_object(chassis, name="FINAL_CHASSIS", options={"color": "lightblue"})

print("\n8 SECTIONS:")
print("- 4 Corners: {}mm thick".format(CORNER_THICKNESS))
print("- Front Middle: {}mm thick (full)".format(FRONT_MIDDLE_THICKNESS))
print("- Back Middle: {}mm thick".format(BACK_MIDDLE_THICKNESS))
print("- Left Middle: {}mm thick (half)".format(LEFT_MIDDLE_THICKNESS))
print("- Right Middle: {}mm thick".format(RIGHT_MIDDLE_THICKNESS))

# Export (uncomment to use)
# cq.exporters.export(chassis, "chassis.stl")