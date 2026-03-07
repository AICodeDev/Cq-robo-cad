import cadquery as cq

# ============================================
# CUSTOMIZABLE PARAMETERS
# ============================================

# Wheel dimensions
outer_radius = 35.0          # Outer radius of the wheel (mm)
inner_radius = 12.0          # Inner hub radius (mm)
wheel_thickness = 2.0        # Wall thickness of outer wheel rim (mm) - start with 2mm for testing
wheel_width = 10.0           # Width of the wheel (mm)

# Hub (center cylinder) dimensions
hub_height = 10.0            # Height of inner cylinder (>8mm as required)
hub_diameter = 8.0           # Diameter of the hub/center cylinder (mm)

# Motor shaft specifications (550 motor typically has 3.17mm or 4mm shaft)
motor_shaft_diameter = 3.2   # Diameter of motor shaft hole (mm)
d_cut_depth = 0.8            # Depth of D-cut flat (mm) - creates flat side for motor shaft
d_cut_offset = -0.4          # Offset from center to create D-cut

# M2 screw hole (for set screw to secure to motor shaft)
m2_screw_diameter = 2.2      # M2 screw hole diameter (mm) - slightly larger for tap/clearance
m2_screw_offset_height = 5.0 # Height from base where M2 screw hole is located (mm)

# Spokes/supports between hub and rim
number_of_spokes = 6         # Number of spokes in circular pattern
spoke_width = 3.0            # Width of each spoke (mm)
spoke_thickness = 2.0        # Thickness of spoke (mm)

# ============================================
# WHEEL CONSTRUCTION
# ============================================

# Create the main outer wheel rim
wheel = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(outer_radius - wheel_thickness)
    .extrude(wheel_width)
)

# Create the center hub (inner cylinder)
hub = (
    cq.Workplane("XY")
    .circle(hub_diameter / 2)
    .extrude(hub_height)
)

# Create motor shaft hole with D-cut
shaft_hole = (
    cq.Workplane("XY")
    .circle(motor_shaft_diameter / 2)
    .extrude(hub_height)
)

# Create D-cut (flat side) for motor shaft
d_cut = (
    cq.Workplane("YZ")
    .workplane(offset=motor_shaft_diameter / 2 - d_cut_depth)
    .rect(motor_shaft_diameter * 2, hub_height * 2)
    .extrude(motor_shaft_diameter)
)

# Create M2 screw hole (perpendicular to shaft)
m2_hole = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(0, m2_screw_offset_height)
    .circle(m2_screw_diameter / 2)
    .extrude(hub_diameter)
)

# Combine hub with holes
hub = hub.cut(shaft_hole).cut(d_cut).cut(m2_hole)

# Create spokes connecting hub to rim
spokes = cq.Workplane("XY")
for i in range(number_of_spokes):
    angle = i * 360 / number_of_spokes
    spoke = (
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, angle))
        .center(0, (hub_diameter / 2 + inner_radius) / 2)
        .rect(spoke_width, inner_radius - hub_diameter / 2)
        .extrude(spoke_thickness)
    )
    spokes = spokes.union(spoke)

# Combine all components
final_wheel = wheel.union(hub).union(spokes)

# ============================================
# EXPORT
# ============================================

# Show the result
show_object(final_wheel)

# To export as STL for 3D printing, uncomment the line below:
# cq.exporters.export(final_wheel, "robot_wheel.stl")

# ============================================
# PRINTING NOTES FOR CARBON FIBER
# ============================================
# 1. Print with wheel flat on bed (XY plane) for best strength
# 2. Use 100% infill for spokes and hub
# 3. Carbon fiber requires hardened nozzle (steel/ruby)
# 4. Print temperature: typically 240-260°C for CF-filled filaments
# 5. Bed temperature: 80-100°C
# 6. First layer: slow speed (20-30mm/s)
# 7. Consider printing multiple wheels to test fitment
# 8. Increase wall_thickness gradually (2mm → 3mm → 4mm) after testing