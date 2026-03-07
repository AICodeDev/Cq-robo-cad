import cadquery as cq
from params import CarParams as CapParams # Matching your snippet variable

# --- Top Level Variables ---
PLATE_X = 24
PLATE_Y = 6
PLATE_Z = 3+3

ROD_SIZE = 12
ROD_SIZE_H = 12
ROD_SIZE_W = 12+6
ROD_SIZE_T = PLATE_Z
ROD_SIZE_Z = PLATE_Z

ROD_LENGTH = 12+6
SCREW_HOLE_DIA = 3.0

def make_cap_bush():
    # 1. Define Ring Parameters as requested
    outer_dia = (CapParams.CAP_PIPE_BASE_DIA) + 0.2
    inner_dia = (CapParams.CAP_PIPE_TOP_DIA) + 1
    height = 6
    
    # 2. Create the Left Plate (Planar)
    # Positioned at the start of the assembly
    plate = (
        cq.Workplane("YZ")
        .box(PLATE_X, PLATE_Y, PLATE_Z)
        .faces("<X").workplane()
        .pushPoints([(8, 0), (-8, 0)]) # Screw holes 6mm deep
        .hole(SCREW_HOLE_DIA, depth=6)
    )
    
    # 3. Create the Center Connector (SR Rod)
    # Extruded from the inner face of the plate
    connector = (
        plate.faces(">X")
        .workplane()
        .rect(ROD_SIZE_W, ROD_SIZE_T)
        .extrude(ROD_LENGTH+1)
    )
    
    # 4. Create the Vertical Pipe/Cylinder
    # We place the center of the ring at the end of the rod
    # Using your specific logic: Circle -> Extrude -> Hole
    result = (
        connector.faces(">Z")
        .workplane()
        .center(10, 0) # Adjusting center based on rod end
        .circle(outer_dia / 2)
        .cutThruAll()
    )
    
    return result
