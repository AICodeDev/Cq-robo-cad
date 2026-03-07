import cadquery as cq
from params import CarParams as p

def make_hub():
    # Pre-calculated values based on your logic
    
    hub_radius = (9.25) -1.8   -1+3
    cy_height = 8+6    
    # 1. Create the Hub
    hub = (
        cq.Workplane("XY")
        .circle(hub_radius)
        .extrude(cy_height)
       
    )
    #return hub
    #WHEEL_HARD_RECT_CUT_SIZE = 8.5
    h2 = (
        hub
        .faces(">Z")
        .workplane().tag("top_base")
        .rect(p.WHEEL_HARD_RECT_CUT_SIZE_CLEAR , p.WHEEL_HARD_RECT_CUT_SIZE_CLEAR )        
        .cutBlind(-1)    
        .workplaneFromTagged("top_base")     
        .rect(p.WHEEL_HARD_RECT_CUT_SIZE , p.WHEEL_HARD_RECT_CUT_SIZE )        
        .cutBlind(-(cy_height-2))        
        .circle(p.WHEEL_HARD_AXLE_HOLE_D / 2)
        .cutThruAll()
        
    )

    return h2


def make_wheel_hard():
    # Pre-calculated values based on your logic
    root_radius = p.WHEEL_HARD_OUTER_RIM_RADIUS - p.WHEEL_HARD_RIM_THICKNESS
    hub_radius = p.WHEEL_HARD_HUB_DIAMETER / 2
    spoke_length = root_radius - hub_radius + 2

    base_height = p.WHEEL_HARD_SPOKE_HEIGHT #
    cy_height = base_height+8
    
    # 1. Create the Hub
    hub = (
        cq.Workplane("XY")
        .circle(hub_radius)
        .extrude(
            #p.WHEEL_HARD_HUB_HEIGHT
            cy_height
            
        )
        #.faces(">Z")
        #.workplane()
        #.circle(hub_radius - 2)
        #.extrude(p.WHEEL_HARD_HUB_EXTRUDE_ADD)
    )

    # 2. Create a Single Spoke
    single_spoke_shape = (
        cq.Workplane("XY")
        .rect(spoke_length, p.WHEEL_HARD_SPOKE_THICKNESS)
        .extrude(base_height)
        .translate([(spoke_length / 2) + hub_radius - 1, 0, 0])
        .val()
    )

    # 3. Create the Spoke Pattern
    spokes = (
        cq.Workplane("XY")
        .polarArray(radius=0, startAngle=0, angle=360, count=p.WHEEL_HARD_SPOKE_COUNT)
        .eachpoint(lambda loc: single_spoke_shape.located(loc))
    )

    # 4. Create the Rim
    rim = (
        cq.Workplane("XY")
        .circle(p.WHEEL_HARD_OUTER_RIM_RADIUS)
        .circle(root_radius)
        .extrude(p.WHEEL_HARD_RIM_HEIGHT)
    )

    # 5. Combine and Apply Final Cuts
    wheel = rim.union(hub).union(spokes)

    wheel_hard = (
        wheel
        .faces("<Z")
        .workplane()
        .circle(p.WHEEL_HARD_AXLE_HOLE_D / 2)
        .cutThruAll()
        .rect(p.WHEEL_HARD_RECT_CUT_SIZE , p.WHEEL_HARD_RECT_CUT_SIZE )
        # Your specific deep cut logic
        .cutBlind(-(p.WHEEL_HARD_HUB_HEIGHT + p.WHEEL_HARD_HUB_EXTRUDE_ADD + 10))
    )

    return wheel_hard

# For testing in CQ-editor
if __name__ == "__main__":
    from parts.wheel_hard import make_wheel_hard
    show_object(make_wheel_hard(), name="wheel_hard")
