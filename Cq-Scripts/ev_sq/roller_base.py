import cadquery as cq
import math
from cq_gears  import BevelGear, SpurGear

# ------------------------
# Parameters
# ------------------------
motor_shaft_d = 6        # motor shaft diameter
hub_d = 11+3  #(math.sqrt(32) *2) +3                # hub cylinder outer diameter


gear_module = 1.25
teeth_number = 18
cone_angle = 45
face_width = 6
pressure_angle = 20
helix_angle = 0
set_screw_d = 3          # optional radial screw
module = 2              # gear module




# --- Desired pitch radius ---


# --- Gear parameters ---

teeth_number = 12 # int(pitch_diameter / module)  # teeth = 22/2 = 11
pressure_angle = 24
face_width = 20-10
total_height =25.8

# --- Create the spur gear ---


hub_height = 15.6 +2         # hub height
hub_height = 5
hub_height = 16*4

# ------------------------
# Create Hub Cylinder
# ------------------------
hub = cq.Workplane("XY").circle(hub_d/2).extrude(hub_height)
show_object(hub)

hub = (
    hub
    .faces(">Z")              # Start at the top face
    .workplane(offset=-6) # Move to the vertical middle of the hub
    .transformed(rotate=(0, 90, 0))  # Rotate to face the side wall
    .circle(2)                # 4mm diameter hole
     .cutThruAll()  # T
)

show_object(hub)

# ------------------------
# Combine Gear + Hub


# ------------------------
# Parameters
# ------------------------
outer_d = 7.0 #

outer_d = 7.2 #

length = 60



# ------------------------
# Cut hex hole
# ------------------------
roller_with_hole = (
    hub
    .faces(">Z")
    .workplane()
    .rect(8.1,8.1)
    .cutThruAll()
)
show_object(roller_with_hole)


cq.exporters.export(roller_with_hole, 'pipe.stl', tolerance=0.01, angularTolerance=0.05)



