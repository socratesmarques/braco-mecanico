module hole(d,h) { translate([0,0,-epsilon]) cylinder(d=d,h=h+2*epsilon); }
module capsule(length,width,height) {
    hull() for(x=[0,length]) translate([x,0,0]) cylinder(d=width,h=height);
}
module base_plate() {
    difference() {
        translate([-base_size/2,-base_size/2,0]) cube([base_size,base_size,base_thickness]);
        hole(pin_hole_d,base_thickness);
        for(x=[-1,1],y=[-1,1]) translate([x*(base_size/2-anchor_inset),y*(base_size/2-anchor_inset),0])
            hole(anchor_nominal_d+hole_clearance_d,base_thickness);
    }
}
module turntable() {
    difference() {
        cylinder(d=turntable_d,h=turntable_thickness);
        hole(pin_hole_d,turntable_thickness);
        for(s=[-1,1],x=[-1,1]) translate([x*pedestal_bolt_x,s*pedestal_offset+pedestal_bolt_y,0])
            hole(bolt_hole_d,turntable_thickness);
    }
}
// Suporte em L: pé aparafusado, parede com passagem do eixo horizontal.
module pedestal() {
    difference() {
        union() {
            translate([-pedestal_width/2,-pedestal_foot_depth/2,0]) cube([pedestal_width,pedestal_foot_depth,pedestal_foot_thickness]);
            translate([0,plate_thickness/2,0]) rotate([90,0,0]) linear_extrude(plate_thickness) hull() {
                translate([-pedestal_width/2,0]) square([pedestal_width,pedestal_foot_thickness]);
                translate([0,shoulder_height]) circle(d=plate_width);
            }
        }
        translate([0,plate_thickness,shoulder_height]) rotate([90,0,0]) cylinder(d=pin_hole_d,h=2*plate_thickness);
        for(x=[-1,1]) translate([x*pedestal_bolt_x,pedestal_bolt_y,0]) hole(bolt_hole_d,pedestal_foot_thickness);
    }
}
module link_plate(length,distal_mount=false) {
    difference() {
        capsule(length,plate_width,plate_thickness);
        for(x=[0,length]) translate([x,0,0]) hole(pin_hole_d,plate_thickness);
        for(x=[length*0.3,length*0.7]) translate([x,0,0]) hole(bolt_hole_d,plate_thickness);
        if(distal_mount) translate([length-gripper_mount_pitch,0,0]) hole(bolt_hole_d,plate_thickness);
    }
}
module spacer(offset) {
    difference() {
        translate([-spacer_width/2,-spacer_depth/2,0]) cube([spacer_width,spacer_depth,2*offset-plate_thickness]);
        hole(bolt_hole_d,2*offset-plate_thickness);
    }
}
module palm() {
    difference() {
        translate([-palm_back,-palm_width/2,0]) cube([palm_back+palm_front,palm_width,plate_thickness]);
        // Dois pontos impedem uma articulação de punho livre.
        hole(pin_hole_d,plate_thickness);
        translate([-gripper_mount_pitch,0,0]) hole(bolt_hole_d,plate_thickness);
        for(y=[-finger_offset,finger_offset]) translate([finger_pivot_x,y,0]) hole(bolt_hole_d,plate_thickness);
        translate([finger_pivot_x+finger_lock_pitch,-finger_offset,0]) hole(bolt_hole_d,plate_thickness);
    }
}
module finger(fixed=false) {
    difference() {
        capsule(finger_length,finger_width,plate_thickness);
        hole(bolt_hole_d,plate_thickness);
        if(fixed) translate([finger_lock_pitch,0,0]) hole(bolt_hole_d,plate_thickness);
    }
}
module tolerance_coupon() {
    difference() {
        cube([60,20,plate_thickness]);
        for(i=[0:3]) translate([9+14*i,10,0]) hole(pin_nominal_d+0.2*i,plate_thickness);
    }
}
// Peças isoladas apoiadas em Z=0, sem hardware de referência.
module printable_part(name) {
    if(name=="base") translate([base_size/2,base_size/2,0]) base_plate();
    else if(name=="turntable") translate([turntable_d/2,turntable_d/2,0]) turntable();
    else if(name=="pedestal") translate([pedestal_width/2,pedestal_foot_depth/2,0]) pedestal();
    else if(name=="upper_link") translate([plate_width/2,plate_width/2,0]) link_plate(upper_length);
    else if(name=="fore_link") translate([plate_width/2,plate_width/2,0]) link_plate(fore_length,true);
    else if(name=="upper_spacer") translate([spacer_width/2,spacer_depth/2,0]) spacer(upper_offset);
    else if(name=="fore_spacer") translate([spacer_width/2,spacer_depth/2,0]) spacer(fore_offset);
    else if(name=="palm") translate([palm_back,palm_width/2,0]) palm();
    else if(name=="fixed_finger") translate([finger_width/2,finger_width/2,0]) finger(true);
    else if(name=="moving_finger") translate([finger_width/2,finger_width/2,0]) finger();
    else if(name=="tolerance_coupon") tolerance_coupon();
    else assert(false,str("Peça desconhecida: ",name));
}
