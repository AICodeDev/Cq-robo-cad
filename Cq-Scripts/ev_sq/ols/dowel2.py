import cadquery as cq

def create_chassis_with_holes(
    length=200,
    width=100,
    depth=3,
    edge_padding=10,
    hole_spacing_horizontal=20,
    hole_spacing_vertical=20,
    hole_diameter=3.2  # M3 clearance hole (3mm + 0.2mm clearance)
):
    """
    Create a parametric chassis plate with a grid of M3 mounting holes.
    
    Parameters:
    -----------
    length : float
        Length of the chassis in mm
    width : float
        Width of the chassis in mm
    depth : float
        Thickness of the chassis plate in mm (default 3mm)
    edge_padding : float
        Distance from edge to first hole in mm
    hole_spacing_horizontal : float
        Horizontal distance between hole centers in mm
    hole_spacing_vertical : float
        Vertical distance between hole centers in mm
    hole_diameter : float
        Diameter of holes in mm (default 3.2mm for M3 clearance)
    """
    
    # Create the base chassis plate
    chassis = cq.Workplane("XY").box(length, width, depth)
    
    # Calculate the usable area for holes
    usable_length = length - (2 * edge_padding)
    usable_width = width - (2 * edge_padding)
    
    # Calculate number of holes in each direction
    num_holes_x = int(usable_length / hole_spacing_horizontal) + 1
    num_holes_y = int(usable_width / hole_spacing_vertical) + 1
    
    # Calculate starting positions (centered in usable area)
    actual_grid_length = (num_holes_x - 1) * hole_spacing_horizontal
    actual_grid_width = (num_holes_y - 1) * hole_spacing_vertical
    
    start_x = -length/2 + edge_padding + (usable_length - actual_grid_length) / 2
    start_y = -width/2 + edge_padding + (usable_width - actual_grid_width) / 2
    
    # Create hole positions
    hole_positions = []
    for i in range(num_holes_x):
        for j in range(num_holes_y):
            x = start_x + i * hole_spacing_horizontal
            y = start_y + j * hole_spacing_vertical
            hole_positions.append((x, y))
    
    # Create holes through the chassis
    chassis = chassis.faces(">Z").workplane()
    for pos in hole_positions:
        chassis = chassis.pushPoints([pos]).hole(hole_diameter)
    
    return chassis


# ============================================
# EDIT THESE PARAMETERS FOR YOUR CHASSIS
# ============================================

LENGTH = 200              # Chassis length in mm
WIDTH = 100               # Chassis width in mm
DEPTH = 3                 # Chassis thickness in mm
EDGE_PADDING = 10         # Distance from edge to first hole
HOLE_SPACING_H = 20       # Horizontal spacing between holes
HOLE_SPACING_V = 20       # Vertical spacing between holes
HOLE_DIAMETER = 3.2       # M3 clearance hole diameter

# ============================================
# CREATE AND DISPLAY THE CHASSIS
# ============================================

chassis = create_chassis_with_holes(
    length=LENGTH,
    width=WIDTH,
    depth=DEPTH,
    edge_padding=EDGE_PADDING,
    hole_spacing_horizontal=HOLE_SPACING_H,
    hole_spacing_vertical=HOLE_SPACING_V,
    hole_diameter=HOLE_DIAMETER
)

# Display in CQ-editor
show_object(chassis, name="chassis")

# Optional: Export to STEP file (uncomment to use)
# cq.exporters.export(chassis, "chassis.step")