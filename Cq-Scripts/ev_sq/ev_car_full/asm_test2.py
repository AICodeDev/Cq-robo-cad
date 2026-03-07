import cadquery as cq

from parts.wheel_hard import make_wheel_hard

from parts.wheel_hard import make_wheel_hard

from parts.motor import make_motor

motor = make_motor()
motor= motor.translate((10,36,21.5))
show_object(motor, options={"color": "green", "alpha": 0.5})



wheel_print = make_wheel_hard()
#show_object(wheel_geometry)
# Wheel Left (Positioned at +Y, rotated 180 around X to face inward)
wheel_L = wheel_print.rotate((0,0,0), (0,1,0), 90).translate((-80,0,16))
# Wheel Right (Positioned at -Y, standard orientation)
wheel_R =  wheel_L.mirror(mirrorPlane="YZ")
show_object(wheel_L, options={"color": "grey", "alpha": 0.5} )
show_object(wheel_R , options={"color": "grey", "alpha": 0.5})
from parts.axle import make_axle, show_axle

from parts.bush_holder_plate import make_bush_holder_plate
from parts.bush_holder_bracket import make_bush_holder_bracket
from params import CarParams as p

axle_rod = make_axle().translate( (0,0,16))
#show_axle(axle_rod)
show_object(
        axle_rod, 
        options={"color": "blue", "alpha": 0.5}
    )


# Initialize Assembly
assy = cq.Assembly()

# 1. Add Plate as the fixed base
plate = make_bush_holder_plate().translate((0,60,0))
assy.add(plate, name="base_plate", color=cq.Color("gray"))
#b=make_bush_holder_bracket().rotate((0,0,0), (0,1,0), 90);
#show_object(b)

# 2. Add Brackets
bracket_L = make_bush_holder_bracket().translate((+47+7,0,1.5))
show_object(bracket_L , options={"color": "pink", "alpha": 0.5} )
bracket_R = bracket_L.mirror(mirrorPlane="YZ")
show_object(bracket_R , options={"color": "pink", "alpha": 0.5} )

show_object(plate)

"""
assy.add(bracket_L, name="bracket_left", color=cq.Color("orange"))
assy.add(bracket_R, name="bracket_right", color=cq.Color("orange"))

# 3. Constraint: Snap Bracket Left to Plate Holes
# We use 'Plane' constraint to align the bottom of bracket to top of plate
assy.constrain("base_plate@faces@>Z", "bracket_left@faces@<Z", "Plane")
assy.constrain("base_plate@faces@>Z", "bracket_right@faces@<Z", "Plane")

# Use 'Axis' constraints on the holes to align them perfectly
# assy.constrain("base_plate?hole1", "bracket_left?hole1", "Axis")

# 4. Solve the assembly to apply the snaps
assy.solve()
show_object(assy)
"""
