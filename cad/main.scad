// F5 prévia; F6 renderização. Conjunto não imprimível.
part = "assembly"; // [assembly,exploded,base,turntable,pedestal,upper_link,fore_link,upper_spacer,fore_spacer,palm,fixed_finger,moving_finger,tolerance_coupon]
show_hardware = true;
include <parameters.scad>
include <lib/parts.scad>
include <lib/assembly.scad>
validate_parameters() {
    if(part=="assembly") arm_assembly(false,show_hardware);
    else if(part=="exploded") arm_assembly(true,show_hardware);
    else printable_part(part);
}
