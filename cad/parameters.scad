// mm/graus. Valores escolhidos para CONCEITO; não são medições de componentes.
$fn = 48;
epsilon = 0.02;
bed = [220,220,250];
bed_margin = 5; // por lado XY; confirmar brim
base_size = 120;
base_thickness = 6;
turntable_d = 88;
turntable_thickness = 6;
base_support_gap = 4; // reserva para apoio axial/radial NÃO projetado
shoulder_height = 30;
upper_length = 110; // entre eixos
fore_length = 100;
plate_width = 24;
plate_thickness = 5;
upper_offset = 18; // metade da distância entre centros das placas
fore_offset = 10;
pedestal_offset = 26;
pedestal_width = 36;
pedestal_foot_depth = 22;
pedestal_foot_thickness = 5;
spacer_width = 12;
spacer_depth = 8;
pin_nominal_d = 5; // candidato genérico, não alojamento de rolamento
bolt_nominal_d = 3; // candidato, sem rosca impressa
hole_clearance_d = 0.4; // acréscimo DIAMETRAL experimental
axial_clearance = 0.5;
pin_hole_d = pin_nominal_d + hole_clearance_d;
bolt_hole_d = bolt_nominal_d + hole_clearance_d;
anchor_nominal_d = 4;
anchor_inset = 12;
pedestal_bolt_x = 12;
pedestal_bolt_y = 7;
gripper_mount_pitch = 18;
palm_back = 24;
palm_front = 22;
palm_width = 48;
finger_length = 40;
finger_width = 8;
finger_pivot_x = 8;
finger_offset = 16;
finger_lock_pitch = 10;
// Poses visuais, NÃO limites seguros de servo.
base_angle = 20;
shoulder_angle = 75; // 0 horizontal, 90 vertical
elbow_angle = -35; // relativo ao elo superior
gripper_angle = -10;
explosion = 24;
// Sem substitutos fictícios para dados desconhecidos.
servo_body_xyz = undef;
servo_mount_pitch_xy = undef;
servo_shaft_offset_xyz = undef;
servo_horn_holes = undef;
bearing_od = undef;
bearing_id = undef;
bearing_width = undef;

module validate_parameters() {
    assert(base_size > turntable_d && base_size <= bed[0]-2*bed_margin,"Base incompatível com prato/mesa");
    assert(min(base_thickness,turntable_thickness,plate_thickness) >= 3,"Espessura abaixo do mínimo conceitual");
    assert(upper_length > 4*plate_width && fore_length > 3*plate_width,"Elos curtos para esta topologia");
    assert(hole_clearance_d >= 0 && hole_clearance_d <= 1,"Folga diametral fora da faixa exploratória");
    assert(pin_nominal_d > 0 && bolt_nominal_d > 0);
    assert(pin_hole_d < plate_width/2 && bolt_hole_d < spacer_depth-2,"Parede insuficiente junto ao furo");
    assert(upper_offset-fore_offset > plate_thickness+axial_clearance,"Colisão de placas no cotovelo");
    assert(pedestal_offset-upper_offset > plate_thickness+axial_clearance,"Colisão de placas no ombro");
    assert(fore_offset > plate_thickness && shoulder_height > plate_width);
    assert(gripper_mount_pitch > pin_hole_d+bolt_hole_d);
    assert(finger_lock_pitch > bolt_hole_d+2);
    assert(2*finger_offset+finger_width < palm_width);
    assert(pedestal_foot_depth/2-pedestal_bolt_y-bolt_hole_d/2 >= 2,"Borda insuficiente no pé do pedestal");
    assert(pedestal_bolt_y-bolt_hole_d/2 > plate_thickness/2,"Fixador dentro da parede do pedestal");
    assert(sqrt(pow(pedestal_width/2,2)+pow(pedestal_offset+pedestal_foot_depth/2,2)) < turntable_d/2,"Pé ultrapassa o prato");
    assert(palm_back-gripper_mount_pitch-bolt_hole_d/2 >= 2,"Borda insuficiente na palma");
    children();
}
