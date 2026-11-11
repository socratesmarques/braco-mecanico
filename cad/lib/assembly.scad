module link_pair(length,offset,distal=false,spread=0) {
    color([0.12,0.48,0.64]) for(s=[-1,1]) translate([0,0,s*(offset+spread)-plate_thickness/2]) link_plate(length,distal);
    color([0.9,0.56,0.16]) for(x=[0.3*length,0.7*length]) translate([x,0,-offset+plate_thickness/2]) spacer(offset);
}
module gripper(spread=0) {
    color([0.9,0.56,0.16]) palm();
    color([0.22,0.27,0.32]) translate([finger_pivot_x,-finger_offset,plate_thickness+spread]) finger(true);
    color([0.22,0.27,0.32]) translate([finger_pivot_x,finger_offset,plate_thickness+spread]) rotate([0,0,gripper_angle]) finger();
}
// Pinos ilustrativos: sem ajuste, fornecedor ou transmissão definidos.
module reference_pin(length) {
    color([0.7,0.7,0.72,0.65]) cylinder(d=pin_nominal_d,h=length,center=true);
}
module arm_assembly(exploded=false,hardware=true) {
    e=exploded ? explosion : 0;
    shoulder_z=base_thickness+base_support_gap+turntable_thickness+shoulder_height;
    color([0.22,0.27,0.32]) base_plate();
    rotate([0,0,base_angle]) {
        color([0.9,0.56,0.16]) translate([0,0,base_thickness+base_support_gap+e]) turntable();
        color([0.22,0.27,0.32]) for(s=[-1,1]) translate([0,s*(pedestal_offset+e),base_thickness+base_support_gap+turntable_thickness+e]) pedestal();
        if(hardware) translate([0,0,base_thickness+base_support_gap/2]) reference_pin(2*base_thickness+base_support_gap);
        // X ao longo do elo; Y na largura; Z no eixo da junta.
        translate([0,0,shoulder_z+e]) rotate([0,-shoulder_angle,0]) rotate([90,0,0]) {
            link_pair(upper_length,upper_offset,false,e);
            if(hardware) reference_pin(2*pedestal_offset+plate_thickness+4);
            translate([upper_length,0,0]) rotate([0,0,elbow_angle]) {
                link_pair(fore_length,fore_offset,true,e);
                if(hardware) reference_pin(2*upper_offset+plate_thickness+4);
                translate([fore_length,0,fore_offset+plate_thickness/2+axial_clearance+e]) gripper(e);
            }
        }
    }
}
