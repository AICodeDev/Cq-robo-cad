import cadquery as cq

# ============================================
# REUSABLE MODULAR FUNCTIONS
# ============================================

def create_threaded_hole_grid(
    workplane,
    length,
    width,
    edge_padding,
    hole_diameter,
    hole_spacing,
    depth,
    exclude_rect=None
):
    """
    Create a grid of threaded holes on a workplane.
    For M4 screws in plastic, use 3.3mm tap hole diameter.
    
    exclude_rect: (center_x, center_y, rect_width, rect_height) to exclude holes in that area
    """
    # For 4mm holes with threads, use slightly smaller for self-tapping
    # But since you specified 4mm, we'll use that
    tap_hole_diameter = hole_diameter
    
    # Calculate the usable area for holes
    usable_length = length - (2 * edge_padding)
    usable_width = width - (2 * edge_padding)
    
    # Calculate number of holes based on spacing
    num_holes_x = int(usable_length / hole_spacing) + 1
    num_holes_y = int(usable_width / hole_spacing) + 1
    
    # Calculate starting positions
    start_x = -length/2 + edge_padding
    start_y = -width/2 + edge_padding
    
    # Create hole positions
    hole_positions = []
    for i in range(num_holes_x):
        for j in range(num_holes_y):
            x = start_x + i * hole_spacing
            y = start_y + j * hole_spacing
            
            # Check if hole is in exclude rectangle
            if exclude_rect:
                cx, cy, rw, rh = exclude_rect
                if (abs(x - cx) < rw/2 and abs(y - cy) < rh/2):
                    continue  # Skip this hole
            
            hole_positions.append((x, y))
    
    # Create threaded holes
    result = workplane
    for pos in hole_positions:
        result = result.pushPoints([pos]).hole(tap_hole_diameter, depth)
    
    return result


def create_l_bracket(
    length=30,
    width=20,
    thickness=3,
    base_thickness=8,
    hole_diameter=3.2,
    vertical_height=20
):
    """
    Create an L-shaped motor mounting bracket.
    """
    # Create base plate
    base = cq.Workplane("XY").box(length, width, base_thickness)
    
    # Create vertical wall
    wall = (cq.Workplane("XY")
            .workplane(offset=base_thickness/2)
            .box(length, thickness, vertical_height)
            .translate((0, -width/2 + thickness/2, vertical_height/2)))
    
    # Combine base and wall
    bracket = base.union(wall)
    
    # Add mounting holes in base (for chassis attachment)
    bracket = (bracket.faces("<Z").workplane()
               .pushPoints([(-length/3, 0), (length/3, 0)])
               .hole(3.3))  # Slightly smaller for threading
    
    # Add motor mounting holes in vertical wall
    bracket = (bracket.faces(">Y").workplane()
               .pushPoints([(-length/3, vertical_height/2), (length/3, vertical_height/2)])
               .hole(hole_diameter))
    
    return bracket


def create_pencil_holder(
    holder_height=50,
    holder_diameter=10,
    wall_thickness=2,
    base_width=20,
    base_length=20,
    base_thickness=8
):
    """
    Create a complete pencil/dowel holder (hole goes all the way through).
    """
    # Create mounting base
    base = cq.Workplane("XY").box(base_length, base_width, base_thickness)
    
    # Create cylindrical holder with through hole
    outer_radius = holder_diameter/2 + wall_thickness
    inner_radius = holder_diameter/2
    
    holder = (cq.Workplane("XY")
              .workplane(offset=base_thickness/2)
              .circle(outer_radius)
              .extrude(holder_height)
              .faces(">Z")
              .circle(inner_radius)
              .cutThruAll())  # Complete through hole
    
    # Add mounting holes to base
    holder = (holder.faces("<Z").workplane()
              .pushPoints([(-base_length/3, 0), (base_length/3, 0)])
              .hole(3.3))
    
    result = base.union(holder)
    
    return result


def create_chassis_assembly(
    chassis_length=120,
    chassis_width=88,
    chassis_thickness=8,
    front_thickness=24,
    front_width=40,
    edge_padding=2,
    hole_diameter=4,
    hole_spacing=8,
    center_rect_width=52,
    center_rect_length=68,
    motor_height=36,
    caster_wheel_diameter=12,
    add_brackets=True,
    add_pencil_holder=True,
    bracket_length=35,
    bracket_width=25,
    bracket_thickness=4,
    bracket_height=25
):
    """
    Create complete chassis assembly.
    """
    # Calculate front raised section height
    # Motor height - caster wheel diameter = how much extra thickness needed
    front_raised_height = motor_height - caster_wheel_diameter - chassis_thickness
    
    # Create main chassis plate
    chassis = cq.Workplane("XY").box(chassis_length, chassis_width, chassis_thickness)
    
    # Create raised front section (middle 4cm wide)
    front_raised = (cq.Workplane("XY")
                   .workplane(offset=chassis_thickness/2)
                   .box(front_width, chassis_width, front_raised_height)
                   .translate((-chassis_length/2 + front_width/2, 0, front_raised_height/2)))
    
    chassis = chassis.union(front_raised)
    
    # Add center rectangular cutout
    center_cutout = (cq.Workplane("XY")
                    .box(center_rect_length, center_rect_width, chassis_thickness)
                    .translate((0, 0, 0)))
    
    chassis = chassis.cut(center_cutout)
    
    # Add threaded hole grid (excluding center rectangle area)
    chassis = create_threaded_hole_grid(
        chassis.faces(">Z").workplane(),
        chassis_length,
        chassis_width,
        edge_padding,
        hole_diameter,
        hole_spacing,
        chassis_thickness,
        exclude_rect=(0, 0, center_rect_length, center_rect_width)
    )
    
    # Add L-brackets - 2 in front, 2 in back (mirrored pairs)
    if add_brackets:
        bracket = create_l_bracket(
            length=bracket_length,
            width=bracket_width,
            thickness=bracket_thickness,
            base_thickness=chassis_thickness,
            hole_diameter=3.2,
            vertical_height=bracket_height
        )
        
        # FRONT brackets (mirrored pair)
        # Front-left bracket
        bracket_fl = bracket.rotate((0, 0, 0), (0, 0, 1), 180).translate((
            -chassis_length/2 + bracket_length/2 + 5,
            -chassis_width/2 + bracket_width/2 + 5,
            0
        ))
        
        # Front-right bracket (mirror of front-left)
        bracket_fr = bracket.rotate((0, 0, 0), (0, 0, 1), 180).translate((
            -chassis_length/2 + bracket_length/2 + 5,
            chassis_width/2 - bracket_width/2 - 5,
            0
        ))
        
        # BACK brackets (mirrored pair)
        # Back-left bracket
        bracket_bl = bracket.translate((
            chassis_length/2 - bracket_length/2 - 5,
            -chassis_width/2 + bracket_width/2 + 5,
            0
        ))
        
        # Back-right bracket (mirror of back-left)
        bracket_br = bracket.translate((
            chassis_length/2 - bracket_length/2 - 5,
            chassis_width/2 - bracket_width/2 - 5,
            0
        ))
        
        # Union all brackets with chassis
        chassis = chassis.union(bracket_fl).union(bracket_fr).union(bracket_bl).union(bracket_br)
    
    # Add pencil holder at front center
    if add_pencil_holder:
        holder = create_pencil_holder(
            holder_height=50,
            holder_diameter=10,
            wall_thickness=2.5,
            base_width=20,
            base_length=20,
            base_thickness=chassis_thickness + front_raised_height
        )
        
        # Position at front center, integrated with raised section
        holder_positioned = holder.translate((
            -chassis_length/2 + 10,
            0,
            front_raised_height/2
        ))
        
        chassis = chassis.union(holder_positioned)
    
    return chassis


# ============================================
# CONFIGURATION PARAMETERS
# ============================================

# Chassis dimensions
CHASSIS_LENGTH = 120        # mm
CHASSIS_WIDTH = 88          # mm
CHASSIS_THICKNESS = 8       # mm
FRONT_THICKNESS = 24        # Total thickness at front (8mm base + 16mm raised)
FRONT_WIDTH = 40            # Width of raised front section (4 cm)

# Hole grid parameters
EDGE_PADDING = 2            # mm from edge
HOLE_DIAMETER = 4           # mm
HOLE_SPACING = 8            # mm between centers

# Center rectangular cutout
CENTER_RECT_WIDTH = 52      # mm
CENTER_RECT_LENGTH = 68     # mm

# Motor and wheel parameters
MOTOR_HEIGHT = 36           # mm
CASTER_WHEEL_DIAMETER = 12  # mm

# Bracket parameters
BRACKET_LENGTH = 35         # mm
BRACKET_WIDTH = 25          # mm
BRACKET_THICKNESS = 4       # mm
BRACKET_HEIGHT = 25         # mm vertical wall height

# Pencil/Dowel holder
DOWEL_DIAMETER = 10         # mm
DOWEL_HOLDER_HEIGHT = 50    # mm

# Feature flags
ADD_BRACKETS = True
ADD_PENCIL_HOLDER = True

# ============================================
# CREATE AND DISPLAY THE ASSEMBLY
# ============================================

# Create complete assembly
assembly = create_chassis_assembly(
    chassis_length=CHASSIS_LENGTH,
    chassis_width=CHASSIS_WIDTH,
    chassis_thickness=CHASSIS_THICKNESS,
    front_thickness=FRONT_THICKNESS,
    front_width=FRONT_WIDTH,
    edge_padding=EDGE_PADDING,
    hole_diameter=HOLE_DIAMETER,
    hole_spacing=HOLE_SPACING,
    center_rect_width=CENTER_RECT_WIDTH,
    center_rect_length=CENTER_RECT_LENGTH,
    motor_height=MOTOR_HEIGHT,
    caster_wheel_diameter=CASTER_WHEEL_DIAMETER,
    add_brackets=ADD_BRACKETS,
    add_pencil_holder=ADD_PENCIL_HOLDER,
    bracket_length=BRACKET_LENGTH,
    bracket_width=BRACKET_WIDTH,
    bracket_thickness=BRACKET_THICKNESS,
    bracket_height=BRACKET_HEIGHT
)

# Display in CQ-editor
show_object(assembly, name="chassis_assembly")

# Export to STL for 3D printing (uncomment to use)
# cq.exporters.export(assembly, "science_olympiad_chassis.stl")
# cq.exporters.export(assembly, "science_olympiad_chassis.step")