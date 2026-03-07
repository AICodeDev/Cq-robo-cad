import cadquery as cq
import math
# ============================================
# PARAMETERS
# ============================================
wheel_radius = 35.0    # Radius of the wheel (mm)
wheel_width = 10.0     # Width/height of the wheel (mm)

# ============================================
# CREATE SOLID CYLINDER
# ============================================
wheel = (
    cq.Workplane("XY")
    .circle(wheel_radius)
    .extrude(wheel_width)
)

# ============================================
# DISPLAY WITH COLOR AND TRANSPARENCY
# ============================================
show_object(wheel, options={"color": "blue", "alpha": 0.7})

import cadquery as cq

# ============================================
# PARAMETERS
# ============================================
wheel_radius = 35.0    # Radius of the wheel (mm)
wheel_width = 10.0     # Width/height of the wheel (mm)

hub_radius = 3.5       # Radius of the hub (mm)
hub_height = 10.0      # Height of the hub (mm)

# ============================================
# CREATE SOLID CYLINDER
# ============================================
wheel = (
    cq.Workplane("XY")
    .circle(wheel_radius)
    .extrude(wheel_width)
)

# ============================================
# CREATE HUB ON TOP
# ============================================
hub = (
    cq.Workplane("XY")
    .workplane(offset=wheel_width)
    .circle(hub_radius)
    .extrude(hub_height)
)

# Combine wheel and hub
final_wheel = wheel.union(hub)

# ============================================
# DISPLAY WITH COLOR AND TRANSPARENCY
# ============================================
show_object(final_wheel, options={"color": "red", "alpha": 0.7})

# CREATE HOLE THROUGH ENTIRE WHEEL AND HUB
hole = (
    cq.Workplane("XY")
    .circle(1.2)
    .extrude(wheel_width + hub_height)
)


# Cut hole from hub
final_wheel = final_wheel.cut(hole)
show_object(final_wheel, options={"color": "red", "alpha": 0.7})

# CREATE D-SHAPED CUT FOR MOTOR SHAFT
motor_shaft_radius = 1.6  # Adjust to match your motor shaft
d_cut_depth = 0.5         # Depth of the flat cut



d_cut_radius =  3.0  # Screw hole radius + 3mm = 4.2mm

# Create D-shape: 240-degree arc closed with straight line


# Calculate points for 240-degree arc
start_angle = -120  # Start at -120 degrees
end_angle = 120     # End at 120 degrees (total 240 degrees)

# CREATE D-SHAPED CUT FOR MOTOR SHAFT (semicircle)
d_cut_radius = 2  # Screw hole radius + 3mm = 4.2mm

arc_angle = 180           # Arc angle in degrees (90, 180, 270, 300, etc.)
end_x = d_cut_radius * math.cos(math.radians(arc_angle))
end_y = d_cut_radius * math.sin(math.radians(arc_angle))

# CREATE D-SHAPED CUT FOR MOTOR SHAFT (semicircle)
d_cut_radius = 2.4  # Screw hole radius + 3mm = 4.2mm
r = d_cut_radius

# Create semicircle D-shape centered at hub center
#.moveTo(-d_cut_radius, 0)
#    .radiusArc((d_cut_radius, 0), d_cut_radius)
#    .lineTo(-d_cut_radius, 0)


d_shape = (
    cq.Workplane("XY")
    .workplane(offset=wheel_width)
    .moveTo(-d_cut_radius, 0)
    # 1st arc (90°)
    .radiusArc((0, d_cut_radius), d_cut_radius)
    # 2nd arc (90°)
    .radiusArc((d_cut_radius, 0), d_cut_radius)
    # 3rd arc (90°)
    .radiusArc((0, -d_cut_radius), d_cut_radius)
    # flat side
    .lineTo(-d_cut_radius, 0)
    .close()
    .extrude(hub_height + 2)
)



show_object(d_shape, options={"d_shape": "green", "alpha": 0.7})
final_wheel = final_wheel.cut(d_shape)

# CREATE O-SHAPED (CIRCULAR) CUT - Half height of D-shape
o_cut_radius = d_cut_radius  # Same radius as D-shape (4.2mm)
o_cut_height = (hub_height + 8) / 2  # Half the height of D-shape

# Create circular O-shape cut
o_shape = (
    cq.Workplane("XY")
    .workplane(offset=wheel_width + hub_height/2)
    .circle(o_cut_radius)
    .extrude(o_cut_height)
)
show_object(o_shape,  options={"color": "black", "alpha": 0.7} )

# Cut O-shape from wheel
final_wheel2 = final_wheel.cut(o_shape)

show_object(final_wheel2, options={"color": "orange", "alpha": 0.7})

