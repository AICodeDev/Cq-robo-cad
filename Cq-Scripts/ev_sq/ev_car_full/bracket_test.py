import cadquery as cq

from parts.wheel_hard import make_wheel_hard

wheel_print = make_wheel_hard()
#show_object(wheel_geometry)
# Wheel Left (Positioned at +Y, rotated 180 around X to face inward)
wheel_L = wheel_print.rotate((0,0,0), (0,1,0), 90).translate((-80,0,16))
# Wheel Right (Positioned at -Y, standard orientation)
wheel_R =  wheel_L.mirror(mirrorPlane="YZ")
#show_object(wheel_L)
#show_object(wheel_R)
from parts.axle import make_axle, show_axle

from parts.bush_holder_plate import make_bush_holder_plate
from parts.bush_holder_bracket import make_bush_holder_bracket
from params import CarParams as p

axle_rod = make_axle().translate( (0,0,16))
#show_object(axle_rod)

# Initialize Assembly
assy = cq.Assembly()

# 1. Add Plate as the fixed base
plate = make_bush_holder_plate().translate((0,60,0))
assy.add(plate, name="base_plate", color=cq.Color("gray"))
b=make_bush_holder_bracket().rotate((0,0,0), (0,1,0), 90);
show_object(b)