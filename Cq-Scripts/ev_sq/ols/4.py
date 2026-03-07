import cadquery as cq

# ============================================
# MODULAR FUNCTIONS - STEP BY STEP
# ============================================

def create_base_plate(length, width, thickness):
    """
    Create a simple rectangular base plate.
    This is called a rectangular prism or box.
    
    Parameters:
    -----------
    length : float (X direction)
    width : float (Y direction)
    thickness : float (Z direction - height)
    """
    plate = cq.Workplane("XY").box(length, width, thickness)
    return plate


def create_center_cutout(plate, cutout_length, cutout_width):
    """
    Create a rectangular hole (cutout) in the center of the plate.
    This shape is called a "picture frame" or "rectangular frame".
    
    Parameters:
    -----------
    plate : CadQuery Workplane
    cutout_length : float (X direction)
    cutout_width : float (Y direction)
    """
    # Create the cutout rectangle at center
    result = (plate.faces(">Z").workplane()
              .rect(cutout_length, cutout_width)
              .cutThruAll())
    return result


def add_threaded_holes(plate, plate_length, plate_width, plate_thickness, 
                      edge_padding, hole_diameter, hole_spacing,
                      cutout_length=None, cutout_width=None):
    """
    Add a grid of threaded holes to the plate.
    Holes are placed every 'hole_spacing' mm starting from edge_padding.
    Holes inside the center cutout area are automatically excluded.
    
    For M3/M4 threads in 3D printed plastic:
    - Use tap drill diameter slightly smaller than nominal
    - M4 threads: use 3.3mm hole for self-tapping
    
    Parameters:
    -----------
    plate : CadQuery Workplane
    plate_length : float - total length of plate
    plate_width : float - total width of plate
    plate_thickness : float - thickness to drill through
    edge_padding : float - distance from edge to first hole
    hole_diameter : float - diameter of holes
    hole_spacing : float - distance between hole centers
    cutout_length : float - length of center cutout (optional)
    cutout_width : float - width of center cutout (optional)
    """
    # Calculate hole positions
    hole_positions = []
    
    # Start position (from edge)
    start_x = -plate_length/2 + edge_padding
    start_y = -plate_width/2 + edge_padding
    
    # End position
    end_x = plate_length/2 - edge_padding
    end_y = plate_width/2 - edge_padding
    
    # Generate grid of holes
    x = start_x
    while x <= end_x:
        y = start_y
        while y <= end_y:
            # Check if hole is inside cutout area
            skip_hole = False
            if cutout_length and cutout_width:
                if abs(x) < cutout_length/2 and abs(y) < cutout_width/2:
                    skip_hole = True
            
            if not skip_hole:
                hole_positions.append((x, y))
            
            y += hole_spacing
        x += hole_spacing
    
    # Add holes to the plate
    result = plate.faces(">Z").workplane()
    for pos in hole_positions:
        result = result.pushPoints([pos]).hole(hole_diameter, plate_thickness)
    
    return result


def create_l_bracket(base_length, base_width, base_thickness,
                    wall_height, wall_thickness):
    """
    Create an L-shaped bracket for motor mounting.
    
    Parameters:
    -----------
    base_length : float - length of base plate
    base_width : float - width of base plate  
    base_thickness : float - thickness of base
    wall_height : float - height of vertical wall
    wall_thickness : float - thickness of vertical wall
    """
    # Create horizontal base
    base = cq.Workplane("XY").box(base_length, base_width, base_thickness)
    
    # Create vertical wall
    wall = (cq.Workplane("XY")
            .workplane(offset=base_thickness/2)
            .box(base_length, wall_thickness, wall_height)
            .translate((0, -base_width/2 + wall_thickness/2, wall_height/2)))
    
    # Combine
    bracket = base.union(wall)
    
    # Add mounting holes in base
    bracket = (bracket.faces("<Z").workplane()
               .pushPoints([(-base_length/3, 0), (base_length/3, 0)])
               .hole(3.3, base_thickness))
    
    # Add motor mounting holes in vertical wall
    bracket = (bracket.faces(">Y").workplane()
               .pushPoints([(-base_length/3, wall_height/2), 
                           (base_length/3, wall_height/2)])
               .hole(3.2, wall_thickness))
    
    return bracket


def create_pencil_holder(base_length, base_width, base_thickness,
                        holder_height, holder_inner_diameter, wall_thickness):
    """
    Create a cylindrical pencil/dowel holder with through hole.
    
    Parameters:
    -----------
    base_length : float - mounting base length
    base_width : float - mounting base width
    base_thickness : float - base thickness
    holder_height : float - height of cylinder
    holder_inner_diameter : float - inner diameter for pencil
    wall_thickness : float - wall thickness of cylinder
    """
    # Create mounting base
    base = cq.Workplane("XY").box(base_length, base_width, base_thickness)
    
    # Create cylindrical holder
    outer_diameter = holder_inner_diameter + 2 * wall_thickness
    
    cylinder = (cq.Workplane("XY")
               .workplane(offset=base_thickness/2)
               .circle(outer_diameter/2)
               .extrude(holder_height))
    
    # Create through hole
    cylinder = (cylinder.faces(">Z").workplane()
               .circle(holder_inner_diameter/2)
               .cutThruAll())
    
    # Combine
    holder = base.union(cylinder)
    
    # Add mounting holes
    holder = (holder.faces("<Z").workplane()
             .pushPoints([(-base_length/3, 0), (base_length/3, 0)])
             .hole(3.3, base_thickness))
    
    return holder


def create_raised_front_section(length, width, height):
    """
    Create a raised section for the front of chassis.
    
    Parameters:
    -----------
    length : float - length of raised section
    width : float - width (usually same as chassis width)
    height : float - how much to raise (additional height)
    """
    raised = cq.Workplane("XY").box(length, width, height)
    return raised


# ============================================
# CONFIGURATION PARAMETERS
# ============================================

# Main chassis plate
PLATE_LENGTH = 120          # mm (X direction)
PLATE_WIDTH = 88            # mm (Y direction)  
PLATE_THICKNESS = 8         # mm (Z direction)

# Center rectangular cutout
CUTOUT_LENGTH = 68+16          # mm (X direction)
CUTOUT_WIDTH = 36+16           # mm (Y direction)

# Hole pattern
EDGE_PADDING = 2            # mm from edge to first hole
HOLE_DIAMETER = 4           # mm (use 3.3mm for M4 threading in plastic)
HOLE_SPACING = 8            # mm between hole centers

# Front raised section
FRONT_RAISED_WIDTH = 40     # mm (4 cm in middle)
MOTOR_HEIGHT = 36           # mm
CASTER_DIAMETER = 12        # mm
FRONT_RAISED_HEIGHT = MOTOR_HEIGHT - CASTER_DIAMETER - PLATE_THICKNESS  # = 16mm

# Brackets
BRACKET_BASE_LENGTH = 35
BRACKET_BASE_WIDTH = 25
BRACKET_WALL_HEIGHT = 25
BRACKET_WALL_THICKNESS = 4

# Pencil holder
HOLDER_BASE_LENGTH = 20
HOLDER_BASE_WIDTH = 20
HOLDER_HEIGHT = 50
HOLDER_INNER_DIAMETER = 10
HOLDER_WALL_THICKNESS = 2.5

# ============================================
# BUILD THE CHASSIS STEP BY STEP
# ============================================

# Step 1: Create base plate (this is a rectangular prism/box shape)
chassis = create_base_plate(PLATE_LENGTH, PLATE_WIDTH, PLATE_THICKNESS)
show_object(chassis, name="step1_base_plate", options={"alpha": 0.3})

# Step 2: Add center rectangular cutout (makes it a "picture frame" shape)
#chassis = create_center_cutout(chassis, CUTOUT_LENGTH, CUTOUT_WIDTH)
#show_object(chassis, name="step2_with_cutout", options={"alpha": 0.3})

# Step 3: Add threaded holes (excluding cutout area)
chassis = add_threaded_holes(
    chassis, 
    PLATE_LENGTH, 
    PLATE_WIDTH, 
    PLATE_THICKNESS,
    EDGE_PADDING, 
    HOLE_DIAMETER,  # Use 3.3 for M4 threading
    HOLE_SPACING,
    CUTOUT_LENGTH,
    CUTOUT_WIDTH
)
show_object(chassis, name="step3_with_holes", options={"alpha": 0.5})

# Step 4: Add raised front section
front_raised = create_raised_front_section(
    FRONT_RAISED_WIDTH, 
    PLATE_WIDTH, 
    FRONT_RAISED_HEIGHT
)
front_raised = front_raised.translate((
    -PLATE_LENGTH/2 + FRONT_RAISED_WIDTH/2,
    0,
    PLATE_THICKNESS/2 + FRONT_RAISED_HEIGHT/2
))
chassis = chassis.union(front_raised)
show_object(chassis, name="step4_with_raised_front", options={"alpha": 0.5})

# Step 5: Add L-brackets (2 front, 2 back - mirrored)
bracket = create_l_bracket(
    BRACKET_BASE_LENGTH,
    BRACKET_BASE_WIDTH,
    PLATE_THICKNESS,
    BRACKET_WALL_HEIGHT,
    BRACKET_WALL_THICKNESS
)

# Front left bracket
bracket_fl = bracket.rotate((0, 0, 0), (0, 0, 1), 180).translate((
    -PLATE_LENGTH/2 + BRACKET_BASE_LENGTH/2 + 5,
    -PLATE_WIDTH/2 + BRACKET_BASE_WIDTH/2 + 5,
    0
))

# Front right bracket (mirror)
bracket_fr = bracket.rotate((0, 0, 0), (0, 0, 1), 180).translate((
    -PLATE_LENGTH/2 + BRACKET_BASE_LENGTH/2 + 5,
    PLATE_WIDTH/2 - BRACKET_BASE_WIDTH/2 - 5,
    0
))

# Back left bracket
bracket_bl = bracket.translate((
    PLATE_LENGTH/2 - BRACKET_BASE_LENGTH/2 - 5,
    -PLATE_WIDTH/2 + BRACKET_BASE_WIDTH/2 + 5,
    0
))

# Back right bracket (mirror)
bracket_br = bracket.translate((
    PLATE_LENGTH/2 - BRACKET_BASE_LENGTH/2 - 5,
    PLATE_WIDTH/2 - BRACKET_BASE_WIDTH/2 - 5,
    0
))

chassis = chassis.union(bracket_fl).union(bracket_fr).union(bracket_bl).union(bracket_br)
show_object(chassis, name="step5_with_brackets", options={"alpha": 0.7})

# Step 6: Add pencil holder at front center
holder = create_pencil_holder(
    HOLDER_BASE_LENGTH,
    HOLDER_BASE_WIDTH,
    PLATE_THICKNESS + FRONT_RAISED_HEIGHT,
    HOLDER_HEIGHT,
    HOLDER_INNER_DIAMETER,
    HOLDER_WALL_THICKNESS
)
holder = holder.translate((
    -PLATE_LENGTH/2 + 10,
    0,
    FRONT_RAISED_HEIGHT/2
))
chassis = chassis.union(holder)

# Final assembly
show_object(chassis, name="FINAL_ASSEMBLY")

# Export (uncomment to use)
# cq.exporters.export(chassis, "chassis.stl")
# cq.exporters.export(chassis, "chassis.step")