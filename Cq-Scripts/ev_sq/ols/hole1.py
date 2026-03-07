import cadquery as cq
import math    



# ============================================
# PARAMETERS
# ============================================
#wheel_radius = 35.0    # Radius of the wheel (mm)
#wheel_width = 16.0     # Width/height of the wheel (mm)

reduce_wheel_rad = 3.5
reduce_wheel_width = 3
reduce_hug_rad = 0
reduce_hug_wall = 0.8

reduce_shaft_height =6
common_height= 6-2

wheel_radius = 10 - reduce_wheel_rad   # Radius of the wheel (mm)
wheel_width = 6 - reduce_wheel_width     # Width/height of the wheel (mm)
hub_wall=2-reduce_hug_wall

shaft_height = 16 - reduce_shaft_height ;
shaft_dia = 6.5
hole_dia = shaft_dia - 0.5

total_height= shaft_height - common_height + wheel_width # 6 is common

hub_radius = shaft_dia/2 +hub_wall       # Radius of the hub (mm)
hub_height = total_height - wheel_width     # Height of the hub (mm)

print("hub",hub_radius,hub_height )



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

# to pass the screw
hole_height= total_height - shaft_height+2
hole_radius = shaft_dia/2
# CREATE HOLE THROUGH ENTIRE WHEEL AND HUB
hole = (
    cq.Workplane("XY")
    .circle(hole_radius)
    .extrude(hole_height)
)
show_object(hole, options={"color": "blue", "alpha": 0.7})


# Cut hole from hub
final_wheel = final_wheel.cut(hole)
show_object(final_wheel,"with hole", options={"color": "red", "alpha": 0.7})




# CREATE D-SHAPED CUT FOR MOTOR SHAFT
motor_shaft_radius = shaft_dia/2  # Adjust to match your motor shaft
d_cut_depth = 0.5         # Depth of the flat cut
d_cut_radius =  motor_shaft_radius  # Screw hole radius + 3mm = 4.2mm

d_shape = (
    cq.Workplane("XY")
    .workplane(offset=hole_height-2)
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
    .extrude(total_height-hole_height + 4)
)



show_object(d_shape, options={"d_shape": "green", "alpha": 0.7})


final_wheel = final_wheel.cut(d_shape)

# CREATE O-SHAPED (CIRCULAR) CUT - Half height of D-shape
o_cut_radius = d_cut_radius  # Same radius as D-shape (4.2mm)
o_cut_height = 2  # Half the height of D-shape

# Create circular O-shape cut
o_shape = (
    cq.Workplane("XY")
    .workplane(offset=total_height-2 )
    .circle(o_cut_radius)
    .extrude(o_cut_height*2)
)
show_object(o_shape,  options={"color": "black", "alpha": 0.7} )

# Cut O-shape from wheel
final_wheel2 = final_wheel.cut(o_shape)

show_object(final_wheel2, options={"color": "orange", "alpha": 0.7})


# ============================================
# SPOKES (ARC-BASED CUT)
# ============================================
# ============================================
# SPOKES (8 COUNT, INWARD-FACING ARC)
# ============================================
# ============================================
# SPOKES (12 COUNT, INWARD-FACING ARC)
# ============================================


# -------- Spoke Parameters --------
spoke_count = 1
spoke_angle = 36          # reduced angle to avoid overlap
rim_thickness = 2.0      # outer rim wall thickness (mm)

outer_radius = wheel_radius
rim_inner_radius = outer_radius - rim_thickness
inner_radius = hub_radius + 1.5   # clearance from hub

half_angle = spoke_angle / 2

# Polar helper
def polar(r, deg):
    return (
        r * math.cos(math.radians(deg)),
        r * math.sin(math.radians(deg))
    )

# -------- Single spoke cut (inward curve) --------
single_spoke_cut = (
    cq.Workplane("XY")
    # start on inner rim
    .moveTo(*polar(rim_inner_radius, -half_angle))

    # OUTER ARC — inward-facing
    .radiusArc(
        polar(rim_inner_radius, half_angle),
        -rim_inner_radius
    )

    # line toward hub
    .lineTo(*polar(inner_radius, half_angle))

    # INNER ARC — hub side
    .radiusArc(
        polar(inner_radius, -half_angle),
        inner_radius
    )

    .close()
    .extrude(wheel_width + hub_height)
)

# -------- Polar pattern and cut --------
spokes_cut = (
    cq.Workplane("XY")
    .polarArray(
        radius=1,
        startAngle=0,
        angle=360,
        count=spoke_count
    )
    .eachpoint(lambda loc: single_spoke_cut.val().located(loc), combine=True)
)

final_wheel5 = final_wheel2.cut(spokes_cut)

# -------- Display --------
show_object(final_wheel5, options={"color": "lightgray", "alpha": 0.9})
