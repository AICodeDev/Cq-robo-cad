import cadquery as cq
from params import CarParams as p

def make_big_wheel_hard():
    # Pre-calculated values based on your logic
    root_radius = p.BWHEEL_HARD_OUTER_RIM_RADIUS - p.BWHEEL_HARD_RIM_THICKNESS
    hub_radius = p.BWHEEL_HARD_HUB_DIAMETER / 2
    spoke_length = root_radius - hub_radius +1.5

    base_height = p.BWHEEL_HARD_SPOKE_HEIGHT
    cy_height = p.BWHEEL_HARD_RIM_HEIGHT 
    
    # 1. Create the Hub
    hub = (
        cq.Workplane("XY")
        .circle(hub_radius)
        .extrude(
            #p.BWHEEL_HARD_HUB_HEIGHT
            cy_height
            
        )
        #.faces(">Z")
        #.workplane()
        #.circle(hub_radius - 2)
        #.extrude(p.BWHEEL_HARD_HUB_EXTRUDE_ADD)
    )

    # 2. Create a Single Spoke
    single_spoke_shape = (
        cq.Workplane("XY")
        .rect(spoke_length, p.BWHEEL_HARD_SPOKE_THICKNESS)
        .extrude(base_height)
        .translate([(spoke_length / 2) + hub_radius - 1, 0, 0])
        .val()
    )


    # 3. Create the Spoke Pattern
    spokes = (
        cq.Workplane("XY")
        .polarArray(radius=0, startAngle=0, angle=360, count=p.BWHEEL_HARD_SPOKE_COUNT)
        .eachpoint(lambda loc: single_spoke_shape.located(loc))
    )

    # 4. Create the Rim
    rim = (
        cq.Workplane("XY")
        .circle(p.BWHEEL_HARD_OUTER_RIM_RADIUS)
        .circle(root_radius)
        .extrude(p.BWHEEL_HARD_RIM_HEIGHT)
    )

    # 5. Combine and Apply Final Cuts
    wheel = rim.union(hub).union(spokes)

    w=6.7
    wheel_hard = (
        wheel
        .faces("<Z")
        .workplane()
        .circle(1)
        .cutThruAll()        
        .polygon(6, 7.9 )
        .cutBlind(-19)
        #.center(0, -10)
        #.circle(10)
        #.cutBlind(2)
       
        
    )

    wheel_hard2 = (
        wheel_hard
        .faces("<Z")
        .workplane()
        .circle( 4 )
        .cutBlind(-p.BWHEEL_HARD_SPOKE_HEIGHT+4+3)
    )
    
    wheel_hard2 = (
        wheel_hard2
        .faces(">Z")
        .workplane(offset=-2.5) 
        #.workplane(.workplane(offset=-2.0) )
        .circle( (8/2) )
        .cutBlind(2.1+1)
    )
    
    return wheel_hard2

# For testing in CQ-editor
if __name__ == "__main__":
    from parts.wheel_hard import make_wheel_hard
    show_object(make_wheel_hard(), name="wheel_hard")
