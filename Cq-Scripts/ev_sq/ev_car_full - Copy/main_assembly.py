import cadquery as cq
from parts.wheel import make_wheel
from parts.chassis import make_chassis

# 1. Initialize Assembly
assy = cq.Assembly(name="Car")

# 2. Add the Chassis
chassis_obj = make_chassis()
assy.add(chassis_obj, name="chassis", color=cq.Color("gray"))

# 3. Add and Position Wheels
# You can add the same part multiple times as reusable components
wheel_obj = make_wheel(diameter=35)
assy.add(wheel_obj, name="front_left", loc=cq.Location(cq.Vector(100, 50, 0)))
assy.add(wheel_obj, name="front_right", loc=cq.Location(cq.Vector(100, -50, 0)))

# 4. Display or Export
# If using CQ-editor, use show_object(assy)
# To save: assy.save("complete_car.step")
