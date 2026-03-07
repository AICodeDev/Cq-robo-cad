import cadquery as cq

# ============================================
# SIMPLE MODULAR FUNCTIONS
# ============================================

def create_base_plate(length, width, thickness, cutout_length, cutout_width):
    
    # Create the plate
    plate = cq.Workplane("XY").box(length, width, thickness)
    
    # Add center cutout
    plate = (plate.faces(">Z").workplane()
             .rect(cutout_length, cutout_width)
             .cutThruAll())
    
    return plate


def add_holes(plate, plate_length, plate_width, plate_thickness,
              hole_center_from_edge, hole_diameter, hole_spacing):
    
    # Calculate hole positions
    hole_positions = []
    
    # Starting position (first hole center)
    start_x = -plate_length/2 + hole_center_from_edge
    start_y = -plate_width/2 + hole_center_from_edge
    
    # Ending position (last hole center)
    end_x = plate_length/2 - hole_center_from_edge
    end_y = plate_width/2 - hole_center_from_edge
    
    # Generate grid
    x = start_x
    while x <= end_x:
        y = start_y
        while y <= end_y:
            hole_positions.append((x, y))
            y += hole_spacing
        x += hole_spacing
    
    # Drill holes
    result = plate.faces(">Z").workplane()
    for pos in hole_positions:
        result = result.pushPoints([pos]).hole(hole_diameter -0.2, plate_thickness)
    
    return result


# ============================================
# CONFIGURATION
# ============================================

# Plate dimensions
PLATE_LENGTH = 120          # mm
PLATE_WIDTH = 88            # mm
PLATE_THICKNESS = 9         # mm

# Center cutout
CUTOUT_LENGTH = 68 +16         # mm
CUTOUT_WIDTH = 52           # mm

# Holes
HOLE_CENTER_FROM_EDGE = 4   # mm - pin center is 4mm from edge
HOLE_DIAMETER = 4           # mm
HOLE_SPACING = 8            # mm - distance between hole centers

# ============================================
# BUILD
# ============================================

# Step 1: Create base plate with cutout
chassis = create_base_plate(
    PLATE_LENGTH, 
    PLATE_WIDTH, 
    PLATE_THICKNESS,
    CUTOUT_LENGTH,
    CUTOUT_WIDTH
)

# Step 2: Add holes
chassis = add_holes(
    chassis,
    PLATE_LENGTH,
    PLATE_WIDTH,
    PLATE_THICKNESS,
    HOLE_CENTER_FROM_EDGE,
    HOLE_DIAMETER,
    HOLE_SPACING
)

# Display
show_object(chassis, name="chassis")

# Export (uncomment to use)
# cq.exporters.export(chassis, "chassis.stl")