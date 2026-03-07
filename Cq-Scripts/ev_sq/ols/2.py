import cadquery as cq
from math import pi

# ============================================
# REUSABLE MODULAR FUNCTIONS
# ============================================

def create_threaded_hole_grid(
    workplane,
    length,
    width,
    edge_padding,
    hole_spacing_h,
    hole_spacing_v,
    thread_diameter=3.0,  # M3 thread
    thread_pitch=0.5,     # M3 pitch is 0.5mm
    depth=3
):
    """
    Create a grid of M3 threaded holes on a workplane.
    For 3D printing, use 2.5mm hole for M3 thread self-tapping.
    """
    # For 3D printed threads, use slightly smaller hole
    # M3 threads work best with 2.5mm hole in plastic
    tap_hole_diameter = 2.5  # For self-tapping M3 screws in plastic
    
    # Calculate the usable area for holes
    usable_length = length - (2 * edge_padding)
    usable_width = width - (2 * edge_padding)
    
    # Calculate number of holes
    num_holes_x = int(usable_length / hole_spacing_h) + 1
    num_holes_y = int(usable_width / hole_spacing_v) + 1
    
    # Calculate starting positions
    actual_grid_length = (num_holes_x - 1) * hole_spacing_h
    actual_grid_width = (num_holes_y - 1) * hole_spacing_v
    
    start_x = -length/2 + edge_padding + (usable_length - actual_grid_length) / 2
    start_y = -width/2 + edge_padding + (usable_width - actual_grid_width) / 2
    
    # Create hole positions
    hole_positions = []
    for i in range(num_holes_x):
        for j in range(num_holes_y):
            x = start_x + i * hole_spacing_h
            y = start_y + j * hole_spacing_v
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
    base_thickness=3,
    hole_diameter=3.2,
    hole_offset=10
):
    """
    Create an L-shaped motor mounting bracket.
    Returns a CadQuery object.
    """
    # Create base plate
    base = cq.Workplane("XY").box(length, width, base_thickness)
    
    # Create vertical wall
    wall = (cq.Workplane("XY")
            .workplane(offset=base_thickness/2)
            .box(length, thickness, width)
            .translate((0, -width/2 + thickness/2, width/2)))
    
    # Combine base and wall
    bracket = base.union(wall)
    
    # Add mounting holes in base
    bracket = (bracket.faces("<Z").workplane()
               .pushPoints([(-length/4, 0), (length/4, 0)])
               .hole(2.5))  # M3 tap holes for screws
    
    # Add motor mounting holes in vertical wall
    bracket = (bracket.faces(">Y").workplane()
               .pushPoints([(-length/4, width/3), (length/4, width/3)])
               .hole(hole_diameter))
    
    return bracket


def create_pencil_holder(
    holder_height=40,
    holder_diameter=10,
    wall_thickness=2,
    base_width=25,
    base_length=30,
    base_thickness=3
):
    """
    Create a pencil/dowel holder with mounting base.
    Returns a CadQuery object.
    """
    # Create mounting base
    base = cq.Workplane("XY").box(base_length, base_width, base_thickness)
    
    # Create cylindrical holder
    outer_radius = holder_diameter/2 + wall_thickness
    inner_radius = holder_diameter/2
    
    holder = (cq.Workplane("XY")
              .workplane(offset=base_thickness/2)
              .circle(outer_radius)
              .extrude(holder_height)
              .faces(">Z")
              .workplane()
              .circle(inner_radius)
              .cutThruAll())
    
    # Add mounting holes to base
    holder = (holder.faces("<Z").workplane()
              .pushPoints([(-base_length/3, 0), (base_length/3, 0)])
              .hole(2.5))  # M3 tap holes
    
    # Combine base and holder
    result = base.union(holder)
    
    return result


def create_chassis_assembly(
    chassis_length=200,
    chassis_width=100,
    chassis_depth=3,
    edge_padding=10,
    hole_spacing_h=20,
    hole_spacing_v=20,
    add_brackets=True,
    add_pencil_holder=True
):
    """
    Create complete chassis assembly with brackets and pencil holder.
    """
    # Create main chassis plate
    chassis = cq.Workplane("XY").box(chassis_length, chassis_width, chassis_depth)
    
    # Add threaded hole grid
    chassis = create_threaded_hole_grid(
        chassis.faces(">Z").workplane(),
        chassis_length,
        chassis_width,
        edge_padding,
        hole_spacing_h,
        hole_spacing_v,
        depth=chassis_depth
    )
    
    # Add L-brackets to all four corners for motors
    if add_brackets:
        bracket = create_l_bracket(
            length=30,
            width=20,
            thickness=3,
            base_thickness=chassis_depth
        )
        
        # Front-left bracket
        bracket_fl = bracket.translate((
            -chassis_length/2 + 15,
            -chassis_width/2 + 10,
            0
        ))
        
        # Front-right bracket
        bracket_fr = bracket.rotate((0, 0, 0), (0, 0, 1), 90).translate((
            chassis_length/2 - 10,
            -chassis_width/2 + 15,
            0
        ))
        
        # Back-left bracket
        bracket_bl = bracket.rotate((0, 0, 0), (0, 0, 1), -90).translate((
            -chassis_length/2 + 10,
            chassis_width/2 - 15,
            0
        ))
        
        # Back-right bracket
        bracket_br = bracket.rotate((0, 0, 0), (0, 0, 1), 180).translate((
            chassis_length/2 - 15,
            chassis_width/2 - 10,
            0
        ))
        
        # Union all brackets with chassis
        chassis = chassis.union(bracket_fl).union(bracket_fr).union(bracket_bl).union(bracket_br)
    
    # Add pencil holder at front center
    if add_pencil_holder:
        holder = create_pencil_holder(
            holder_height=40,
            holder_diameter=10,
            wall_thickness=2,
            base_width=25,
            base_length=30,
            base_thickness=chassis_depth
        )
        
        # Position at front center, slightly outside the main plate
        holder_positioned = holder.translate((
            -chassis_length/2 - 15,  # Outside the front edge
            0,
            0
        ))
        
        chassis = chassis.union(holder_positioned)
    
    return chassis


# ============================================
# CONFIGURATION PARAMETERS
# ============================================

# Chassis dimensions
CHASSIS_LENGTH = 200
CHASSIS_WIDTH = 100
CHASSIS_DEPTH = 3

# Hole grid parameters
EDGE_PADDING = 15
HOLE_SPACING_H = 25
HOLE_SPACING_V = 25

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
    chassis_depth=CHASSIS_DEPTH,
    edge_padding=EDGE_PADDING,
    hole_spacing_h=HOLE_SPACING_H,
    hole_spacing_v=HOLE_SPACING_V,
    add_brackets=ADD_BRACKETS,
    add_pencil_holder=ADD_PENCIL_HOLDER
)

# Display in CQ-editor
show_object(assembly, name="chassis_assembly")

# Optional: Create individual components for testing
# show_object(create_l_bracket(), name="bracket", options={"alpha": 0.5})
# show_object(create_pencil_holder(), name="holder", options={"alpha": 0.5})

# Export to STL for 3D printing (uncomment to use)
# cq.exporters.export(assembly, "science_olympiad_chassis.stl")
# cq.exporters.export(assembly, "science_olympiad_chassis.step")22q22