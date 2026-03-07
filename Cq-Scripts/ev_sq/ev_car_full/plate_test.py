import cadquery as cq

from parts.wheel_hard import make_wheel_hard

from parts.wheel_hard import make_wheel_hard
from parts.axle import make_axle, show_axle

from parts.bush_holder_plate import make_bush_holder_plate
from parts.bush_holder_bracket import make_bush_holder_bracket
from params import CarParams as p

plate = make_bush_holder_plate().translate((0,60,0))

plate = plate.rotate((0, 0, 0), (0, 0, 1), 90)

show_object(plate)