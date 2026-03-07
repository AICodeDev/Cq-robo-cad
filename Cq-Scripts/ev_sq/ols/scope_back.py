import cadquery as cq

outer_box_length = 160      # = 142
outer_box_width = 24
outer_box_thickness = 16

outer_box = (
    cq.Workplane("XY")
    .box(outer_box_length, outer_box_width, outer_box_thickness)
)
#holses 64  112
# Cutting tool box (slightly smaller)
outer_box_length_cut1 = outer_box_length -0  # = 62
outer_box_width_cut1  = outer_box_width -0              # = 69
outer_box_thickness_cut1 = outer_box_thickness -0            # = 20

outer_box_cut1 = (
    cq.Workplane("XY")
    .box(outer_box_length_cut1, outer_box_width_cut1, outer_box_thickness_cut1).translate((2,0,1))
)


outer_box_length_cut2 = outer_box_length - 4 +3   # = 62
outer_box_width_cut2  = outer_box_width - 12-1.5              # = 69
outer_box_thickness_cut2 = outer_box_thickness - 1            # = 20

outer_box_cut2 = (
    cq.Workplane("XY")
    .box(outer_box_length_cut2, outer_box_width_cut2, outer_box_thickness_cut2).translate((1,0,1))
)
part1 = outer_box.cut(outer_box_cut1)
# Boolean cut: subtract inner box from outer box
part2 = part1

holes_y= 0 #96/2
holes_x= 0

holes_x2= 72
holes_x3= 64
holes_y3= 0
holes_x4= 8
holes_y4= 0
holes_x5= 32
holes_y5= 0

holes_x6= 40
holes_y6= 0

holes_x7= 48
holes_y7= 0

 

bracket = (
    part2
    .faces("<Z")                      # work on the top face
    .workplane()                      # set workplane on that face
    .pushPoints([                     # 4 corner positions
        ( holes_x,  holes_y),         # front-right
        ( holes_x2,  holes_y),         # front-right
        ( holes_x3,  holes_y3),         # front-right
        ( holes_x4,  holes_y4),         # front-right
        ( holes_x5,  holes_y5),         # front-right        
        ( holes_x6,  holes_y6),         # front-right
        ( holes_x7,  holes_y7),         # front-right
    ])
    .hole(2.5)              # ⌀ 3.2mm through the full thickness
)

# ── Show ─────────────────────────────────────────────────────────────────────
#show_object(bracket, name="bracket", options={"color": (50, 150, 100), "alpha": 1.0})

bracket2 = (
    bracket
    .faces(">X")                      # work on the top face
    .workplane()                      # set workplane on that face
    .pushPoints([                     # 4 corner positions
        ( 8,  8),         # front-right
        ( -8,  8),         # front-right    
        
    ])
    .hole(4)              # ⌀ 3.2mm through the full thickness
)

# ── Show ─────────────────────────────────────────────────────────────────────
show_object(bracket2, name="bracket2", options={"color": (11, 255, 100), "alpha": 1.0})

# ── Show ─────────────────────────────────────────────────────────────────────
#show_object(part4, name="part4", options={"color": (50, 150, 100), "alpha": 1.0})


# ── Show objects with different colors ──────────────────────────────────────
#show_object(outer_box,   name="outer_box",   options={"color": (0, 0, 255),   "alpha": 0.4})  # blue,  semi-transparent
#show_object(outer_box_cut1, name="cut_box",  options={"color": (255, 0, 0),   "alpha": 0.4})  # red,   semi-transparent
#show_object(part1,        name="part1",      options={"color": (0, 200, 100), "alpha": 1.0})  # green, solid
#show_object(part2,        name="part2",      options={"color": (50, 150, 100), "alpha": 1.0})  # green, solid


