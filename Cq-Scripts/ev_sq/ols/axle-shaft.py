import cadquery as cq

# ============================================
# PARAMETERS
# ============================================

adapter_dia = 10.0
axle_len=30

motor_side_len = 9.0
wheel_side_len = 9.0
middle_plate_len = 2.0

# D-shaft sizes
motor_d_radius = 3+0.1     # FEMALE D (motor shaft Ø6 mm)
wheel_d_radius = 2.5+0.1     # MALE D (wheel Ø5 mm)

wheel_clearance_dia = 10.0-0.75

# ============================================
# MOTOR SIDE — FEMALE D (CUT)
# ============================================


axle = (
    cq.Workplane("XZ")
    .moveTo(-motor_d_radius, 0)
    .radiusArc((0, motor_d_radius), motor_d_radius)
    .radiusArc((motor_d_radius, 0), motor_d_radius)
    .radiusArc((0, -motor_d_radius), motor_d_radius)
    .lineTo(-motor_d_radius, 0)
    .close()
    .extrude(axle_len)
)
show_object(axle)





# ============================================
# WHEEL SIDE — MALE D (UNION)
# ============================================

wheel_base = axle
shaft_adapter = axle

# ============================================
# SIDE SET-SCREW HOLES (M2)
# ============================================

m2_clearance_dia = 2.2      # M2 clearance
set_screw_depth = adapter_dia

# --- Motor side set screw (female D side) ---
motor_set_screw = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    #//.center( -axle_len / 2,0)
    .circle(m2_clearance_dia / 2)
    .extrude(set_screw_depth/2)
)

show_object(motor_set_screw)



motor_set_screw = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    #//.center( -axle_len / 2,0)
    .circle(m2_clearance_dia / 2)
    .extrude(set_screw_depth/2)
)

show_object(motor_set_screw)


motor_set_screw2 = (
    cq.Workplane("XZ")
    .workplane(offset=axle_len)
    #//.center( -axle_len / 2,0)
    .circle(m2_clearance_dia / 2)
    .extrude(-set_screw_depth/2)
)

show_object(motor_set_screw2)



# --- Cut both holes ---
shaft_with_hole = shaft_adapter.cut(motor_set_screw)

show_object(shaft_with_hole, options={"color": "gray", "alpha": 0.95})

