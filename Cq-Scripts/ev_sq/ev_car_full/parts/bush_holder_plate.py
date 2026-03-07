import cadquery as cq
from params import CarParams as p

def make_bush_holder_plate():
    full_y = 96
    half_y = 40	
    top_y = 64+52 # oppsitin to motor
    half_x = 64/2
    locy = 64-10
    locx = 50	
    plate = (
        cq.Workplane("XY")
        .box(p.BUSH_HOLDER_PLATE_L, p.BUSH_HOLDER_PLATE_W, p.BUSH_HOLDER_PLATE_T)
        .translate((0,20,0))
        .faces(">Z").workplane()
        .tag("plate_top_face")    
        .pushPoints([(0,0)
		,(-locx,-locy ) ,(locx,-locy )
		,(-locx,-locy-12 ) ,(locx,-locy-12 )
		#//,(-locx,-locy-16 ) ,(locx,-locy-16 )
		,(-locx,-locy-24 ) ,(locx,-locy-24 )

		#,(half_x,0) , (-half_x,0)
     # //  ,(half_x,-16) , (-half_x,-16)
        #,(half_x,-24) , (-half_x,-24)
		#,(half_x,-12) , (-half_x,-12)
        ,(half_x,12) , (-half_x,12)
       #// ,(half_x,16) , (-half_x,16)
        ,(half_x,24) , (-half_x,24)
       
        #,(half_x,40) , (-half_x,40)
         #,(half_x,48) , (-half_x,48)

		,(half_x,full_y) , (-half_x,full_y)
        ,(half_x,full_y+32) , (-half_x,full_y+32)
         
		,(half_x,full_y+24) , (-half_x,full_y+24)
		,(half_x,full_y+16) , (-half_x,full_y+16)
		,(half_x,full_y+8) , (-half_x,full_y+8)
        
        ,(16,top_y) , (-16,top_y)
        ,(8,top_y) , (-8,top_y)
        

		#,(half_x,-full_y) , (-half_x,-full_y)

                ,(8,0) , (-8,0)
        	 ,(8,-locy-24) , (-8,-locy-24)
        	 ,(16,-locy-24) , (-16,-locy-24)
		
	])
        .hole(4)
        
    )
    cut_x = 36-6
    cut_y = -36-16  
    plate = (
        plate.faces(">Z").workplane()
        .center(cut_x, cut_y)
        .rect(24-4, 48)
        .cutThruAll()
        #.center(-cut_x, -cut_y) # Reset center to plate middle for holes
    )
       
    cut_x = -16
    cut_y = 8
    
    
    plate = (
        plate.faces(">Z").workplane()
        .center(cut_x, cut_y)
        .rect(12, 60)
        .extrude(8).faces(">Z").workplane()
	.pushPoints([(0,0),(0, 12),(0,-12), (0, 24),(0,-24) ]).hole(4)

        #.center(-cut_x, -cut_y) # Reset center to plate middle for holes
    )

    plate = (
        plate.workplaneFromTagged("plate_top_face")
        .center(-16, -24)
        .rect(40, 56)
        .cutThruAll()
        #.center(-cut_x, -cut_y) # Reset center to plate middle for holes
    )
    
    
    plate = (
        plate.workplaneFromTagged("plate_top_face")
        .center(0, 64)
        .rect(80, 70)
        .cutThruAll()
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
