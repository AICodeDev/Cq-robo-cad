import cadquery as cq

outer_box_length = 122      # = 142
outer_box_width = 72
outer_box_thickness = 22

outer_box = (
    cq.Workplane("XY")
    .box(outer_box_length, outer_box_width, outer_box_thickness)
)
#holses 64  112
# Cutting tool box (slightly smaller)
outer_box_length_cut1 = 122 - 8 - 2 -8   # = 62
outer_box_width_cut1  = 72 - 3               # = 69
outer_box_thickness_cut1 = 22 - 1            # = 20

outer_box_cut1 = (
    cq.Workplane("XY")
    .box(outer_box_length_cut1, outer_box_width_cut1, outer_box_thickness_cut1).translate((0,0,1))
)


outer_box_length_cut2 = 122 - 4 +3   # = 62
outer_box_width_cut2  = 72 - 12-1.5              # = 69
outer_box_thickness_cut2 = 22 - 1            # = 20

outer_box_cut2 = (
    cq.Workplane("XY")
    .box(outer_box_length_cut2, outer_box_width_cut2, outer_box_thickness_cut2).translate((1,0,1))
)
part1 = outer_box.cut(outer_box_cut1)
# Boolean cut: subtract inner box from outer box
part2 = part1.cut(outer_box_cut2)

holes_y= 64/2 #96/2
holes_x= (96+16)/2 #112/2

holes_x2= (96)/2 #112/2
holes_x3= (64)/2 #112/2
holes_y3= 32/2 #96/2
holes_x4= (32)/2 #112/2
holes_y4= 24/2 #96/2
holes_x5= (16)/2 #112/2
holes_y5= 64/2 #96/2

holes_x6= (64+12)/2 #112/2
holes_y6= 32/2 #96/2

holes_x7= (64+24)/2 #112/2
holes_y7= 32/2 #96/2

 

part3 = (
    part2
    .faces("<Z")                      # work on the top face
    .workplane()                      # set workplane on that face
    .pushPoints([                     # 4 corner positions
        ( holes_x,  holes_y),         # front-right
        (-holes_x,  holes_y),         # front-left
        ( holes_x, -holes_y),         # back-right
        (-holes_x, -holes_y),         # back-left
        ( holes_x2,  holes_y),         # front-right
        (-holes_x2,  holes_y),         # front-left
        ( holes_x2, -holes_y),         # back-right
        (-holes_x2, -holes_y),         # back-left
        ( holes_x3,  holes_y3),         # front-right
        (-holes_x3,  holes_y3),         # front-left
        ( holes_x3, -holes_y3),         # back-right
        (-holes_x3, -holes_y3),         # back-left    
        ( holes_x4,  holes_y4),         # front-right
        (-holes_x4,  holes_y4),         # front-left
        ( holes_x4, -holes_y4),         # back-right
        (-holes_x4, -holes_y4),         # back-left 
        ( holes_x5,  holes_y5),         # front-right
        (-holes_x5,  holes_y5),         # front-left
        ( holes_x5, -holes_y5),         # back-right
        (-holes_x5, -holes_y5),         # back-left   

 ( holes_x6,  holes_y6),         # front-right
        (-holes_x6,  holes_y6),         # front-left
        ( holes_x6, -holes_y6),         # back-right
        (-holes_x6, -holes_y6),         # back-left  


 ( holes_x7,  holes_y7),         # front-right
        (-holes_x7,  holes_y7),         # front-left
        ( holes_x7, -holes_y7),         # back-right
        (-holes_x7, -holes_y7),         # back-left  
  


    ])
    .hole(4)              # ⌀ 3.2mm through the full thickness
)

# ── Show ─────────────────────────────────────────────────────────────────────
#show_object(part3, name="part3", options={"color": (50, 150, 100), "alpha": 1.0})

part4 = (
    part3
    .faces("<Z")                    # select the bottom face
    .workplane(invert=True)         # flip normal to point UPWARD (+Z)
    .pushPoints([                   # 2 positions
        (0,  32),
        (0, -32),
    ])
    .rect(3, 7)                   # 10 x 10 mm rectangle at each point
    .extrude(22, combine=True)      # extrude 22mm upward, merge into part
)

# ── Show ─────────────────────────────────────────────────────────────────────
show_object(part4, name="part4", options={"color": (50, 150, 100), "alpha": 1.0})


# ── Show objects with different colors ──────────────────────────────────────
#show_object(outer_box,   name="outer_box",   options={"color": (0, 0, 255),   "alpha": 0.4})  # blue,  semi-transparent
#show_object(outer_box_cut1, name="cut_box",  options={"color": (255, 0, 0),   "alpha": 0.4})  # red,   semi-transparent
#show_object(part1,        name="part1",      options={"color": (0, 200, 100), "alpha": 1.0})  # green, solid
#show_object(part2,        name="part2",      options={"color": (50, 150, 100), "alpha": 1.0})  # green, solid

