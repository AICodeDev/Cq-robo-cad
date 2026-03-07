import cadquery as cq
import math
from cq_gears  import BevelGear, SpurGear
from cq_gears import RingGear



import cadquery as cq
radius_hw = 4
radius_rod = math.sqrt(16+16)

# Parameters matching your gear
module = 1.0
teeth = 32
width = 8.0
rim_width = 4

spoke_count = 6
spoke_thickness = 4 # Thickness of each spoke
rim_height=10
rim_thickness=3
outer_rim_radius = 84/2
root_radius = outer_rim_radius - rim_thickness


# Root diameter is roughly pitch - 2.5*module
root_diameter = root_radius*2
inner_rim_radius = (root_diameter / 2) - rim_width
hub_diameter = 10.5+4
hub_radius = hub_diameter / 2

hub_height = 16

# 1. Create the Hub
hub = cq.Workplane("XY").circle(hub_radius).extrude(hub_height)

# 2. Create a Single Spoke
# We calculate the length to span from the hub to the inner rim
spoke_length = root_radius - hub_radius +2

# Build one spoke centered on the X-axis
single_spoke = (
    cq.Workplane("XY")
    .rect(spoke_length, spoke_thickness)
    .extrude(5)
    .translate([(spoke_length/2) + hub_radius-1, 0, 0])
)
spoke_shape = single_spoke.val()
# 3. Create the Spoke Pattern
# Use polarArray to place the spoke 6 times
spokes = (
    cq.Workplane("XY")
    .polarArray(radius=0, startAngle=0, angle=360, count=spoke_count)
    # Use loc for the location provided by polarArray
    .eachpoint(lambda loc: spoke_shape.located(loc))
)

# 4. Combine everything
# You would union this with your RingGear object
spoke_system = hub.union(spokes)

# Display result
show_object(spoke_system)



# Create the Rim
# We use cicle().circle() to create a hollow ring in one operation
rim = (
    cq.Workplane("XY")
    .circle(outer_rim_radius)   # Outer edge
    .circle(root_radius)        # Inner hole
    .extrude(rim_height, combine=True)
)


wheel = rim.union(spoke_system)
show_object(rim)



# ------------------------
# Cut hex hole
# ------------------------

after_hole = (
    wheel
    .faces(">Z")
    .workplane()
    .rect(8,8)
    .cutThruAll()
)
show_object(after_hole)







