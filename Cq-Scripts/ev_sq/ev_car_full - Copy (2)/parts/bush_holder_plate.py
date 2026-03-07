import cadquery as cq
from params import CarParams as p

def make_bush_holder_plate():
    full_y = 96
    half_y = 64/2	
    half_x = 64/2
    locy = 56
    	
    plate = (
        cq.Workplane("XY")
        .box(p.BUSH_HOLDER_PLATE_L, p.BUSH_HOLDER_PLATE_W, p.BUSH_HOLDER_PLATE_T)
        .translate((0,20,0))
        .faces(">Z").workplane()      
        .pushPoints([(0,0)
		,(-49,-locy ) ,(49,-locy )
		,(-49,-locy-8 ) ,(49,-locy-8 )
		,(-49,-locy-16 ) ,(49,-locy-16 )
		,(-49,-locy-24 ) ,(49,-locy-24 )

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
    plate = (
        plate.faces(">Z").workplane()
        .center(cut_x, cut_y)
        .rect(16, 64)
        .cutThruAll()
        #.center(-cut_x, -cut_y) # Reset center to plate middle for holes
    )
    cut_x = -16
    cut_y = 24
    
    plate = (
        plate.faces(">Z").workplane()
        .center(cut_x, cut_y)
        .rect(8, 24)
        .extrude(8).faces(">Z").workplane()
	.pushPoints([(0, 8),(0,-8)]).hole(4)

        #.center(-cut_x, -cut_y) # Reset center to plate middle for holes
    )
    		
	
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
