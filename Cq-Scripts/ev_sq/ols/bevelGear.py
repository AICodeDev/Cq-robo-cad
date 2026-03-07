import cadquery as cq
from cq_gears import BevelGear
depth = 8 
length = 100 
width = 8
result = cq.Workplane("front").box(width, length, depth)
height = width 
cdiameter = 8 

gear = BevelGear(
    module=2.0,          # tooth size
    teeth_number=20,     # number of teeth
    cone_angle=45,       # pitch cone angle (degrees)
    face_width=10,       # thickness of gear
    pressure_angle=20,   # standard
    helix_angle=0        # straight bevel
)

cylinder = cq.Workplane("front").circle(cdiameter/2).extrude(-height*5)
# Build CADQuery solid
gear_solid = gear.build()




# Show in CQ-editor

gear_with_hole = (
    cq.Workplane(obj=gear_solid)
    .workplane(origin=(0, 0, 0))
    .circle(6 / 2)
    .cutThruAll()
)

show_object(gear_with_hole)

cylinder_with_hole = (
    cylinder
    .faces(">Z")          # pick the flat face
    .workplane()
    .hole(6)         # through hole
)

show_object(cylinder_with_hole)