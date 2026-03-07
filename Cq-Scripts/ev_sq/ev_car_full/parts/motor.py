import cadquery as cq
from params import CarParams as p



def make_motor():
    # 1. Create the Gearbox (Left Part)
    # We build it centered, then translate as per your original logic
    gearbox = (
        cq.Workplane("XY")
        .box(p.MOTOR_GB_W, p.MOTOR_GB_L, p.MOTOR_GB_H)
        .translate((0, 0, 0))
    )
    
    # 2. Create the Motor Cylinder (Right Part)
    # Positioning it to the "Right" (assuming +X or -X based on your assembly)
    # Based on your gearbox width of 16, we offset it by 8 + (Cyl_H / 2)
    cyl_offset_x = (p.MOTOR_GB_W / 2) + (p.MOTOR_CYL_H / 2)
    motor_cyl = (
        cq.Workplane("YZ") # Cylinder points out the side
        .circle(p.MOTOR_CYL_D / 2)
        .extrude(p.MOTOR_CYL_H)
        .translate((-36,12,0))
        #//.translate((cyl_offset_x, 20, 0)) # Aligned with gearbox center
    )
    
    # 3. Combine and Drill Holes
    # Using your exact point logic from the prompt
    full_y = 96
    half_y = 64/2	
    half_x = 64/2
    locy = 56
    locx = 50
    
    hole_points = [
        (0,0), (-locx,-locy), (locx,-locy),
        (-locx,-locy-8), (locx,-locy-8),
        (-locx,-locy-16), (locx,-locy-16),
        (-locx,-locy-24), (locx,-locy-24),
        (half_x,0), (-half_x,0),
        (half_x,-8), (-half_x,-8),
        (half_x,full_y), (-half_x,full_y),
        (half_x,full_y+24), (-half_x,full_y+24),
        (half_x,full_y+16), (-half_x,full_y+16),
        (half_x,full_y+8), (-half_x,full_y+8),
        (8,0), (-8,0),
        (8,-locy-24), (-8,-locy-24),
        (16,-locy-24), (-16,-locy-24)
    ]
    
    motor_unit = (
        gearbox.union(motor_cyl)
        .faces(">Z").workplane()
        .pushPoints(hole_points)
        .hole(p.MOTOR_HOLE_D)
    )
    
    return motor_unit

if __name__ == "__main__":
    show_object(make_motor(), name="motor_assembly")


def make_motor1():
    full_y = 96
    half_y = 64/2	
    half_x = 64/2
    locy = 56
    locx = 50	
    plate = (
        cq.Workplane("XY")
        .box(16 , 56 , 24)
        .translate((0,20,0))
        .faces(">Z").workplane()      
        .pushPoints([(0,0)
		,(-locx,-locy ) ,(locx,-locy )
		,(-locx,-locy-8 ) ,(locx,-locy-8 )
		,(-locx,-locy-16 ) ,(locx,-locy-16 )
		,(-locx,-locy-24 ) ,(locx,-locy-24 )

		,(half_x,0) , (-half_x,0)
		,(half_x,-8) , (-half_x,-8)

		,(half_x,full_y) , (-half_x,full_y)
		,(half_x,full_y+24) , (-half_x,full_y+24)
		,(half_x,full_y+16) , (-half_x,full_y+16)
		,(half_x,full_y+8) , (-half_x,full_y+8)

		#,(half_x,-full_y) , (-half_x,-full_y)

                ,(8,0) , (-8,0)
        	 ,(8,-locy-24) , (-8,-locy-24)
        	 ,(16,-locy-24) , (-16,-locy-24)
		
	])
        .hole(4)
        
    )
    cut_x = 36
    cut_y = -44    
    
	
    return plate



def show_bush_holder_plate(obj=None, color="lightgray", alpha=1.0):
    """Utility to display the plate with custom visuals."""
    if obj is None:
        # If no object is passed, create and translate it using defaults
        obj = make_bush_holder_plate().translate(
            (p.BUSH_HOLDER_X_OFFSET, 0, p.BUSH_HOLDER_Z_HEIGHT)
        )
    
    if "show_object" in globals():
        show_object(obj, options={"color": color, "alpha": alpha})
