import cadquery as cq
from params import CarParams as CapParams

def make_cap_pipe():
  
    outer_dia= ( CapParams.CAP_PIPE_BASE_DIA) + 0.2
    inner_dia= ( CapParams.CAP_PIPE_TOP_DIA) + 1
    height=6
    
    result = (
        cq.Workplane("XY")
        .circle(outer_dia/ 2)
        .extrude(height)
        .circle(inner_dia / 2).cutThruAll()
    )
    
    return result

if __name__ == "__main__":
    shape = make_cap()
    if "show_object" in globals():
        show_object(shape)
