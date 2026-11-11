"""Estimativa estática com hipóteses declaradas, não especificação de servo."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def calculate(s):
    g = 9.80665
    l1, l2 = s["upper_length_m"], s["fore_length_m"]
    tip = l1+l2
    masses = [(s["upper_mass_kg"],l1/2),
              (s["elbow_actuator_mass_kg"],l1),
              (s["fore_mass_kg"],l1+l2/2),
              (s["gripper_mass_kg"],tip+s["gripper_com_m"]),
              (s["payload_kg"],tip+s["payload_offset_m"])]
    shoulder = g*sum(m*r for m,r in masses)
    elbow = g*(s["fore_mass_kg"]*l2/2+s["gripper_mass_kg"]*(l2+s["gripper_com_m"])
               +s["payload_kg"]*(l2+s["payload_offset_m"]))
    edge = s["base_half_width_m"]
    overturning = g*sum(m*max(r-edge,0) for m,r in masses)
    restoring = g*(s["centered_mass_kg"]*edge+sum(m*max(edge-r,0) for m,r in masses))
    required_centered = max(0,(s["stability_factor"]*overturning/g
        -sum(m*max(edge-r,0) for m,r in masses))/edge)
    return {"scenario":s,"shoulder_static_Nm":round(shoulder,6),
            "elbow_static_Nm":round(elbow,6),
            "shoulder_design_Nm":round(shoulder*s["torque_factor"],6),
            "elbow_design_Nm":round(elbow*s["torque_factor"],6),
            "shoulder_design_kgf_cm":round(shoulder*s["torque_factor"]/(g*0.01),3),
            "elbow_design_kgf_cm":round(elbow*s["torque_factor"]/(g*0.01),3),
            "overturning_Nm":round(overturning,6),"restoring_Nm":round(restoring,6),
            "stability_ratio":round(restoring/overturning,3) if overturning else None,
            "required_total_centered_mass_kg":round(required_centered,3)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario",type=Path,default=ROOT/"docs/load_scenario.json")
    args = parser.parse_args()
    scenario = json.loads(args.scenario.read_text(encoding="utf-8"))
    if any(not isinstance(v,(float,int)) or v < 0 for v in scenario.values()):
        raise ValueError("Hipóteses devem ser números não negativos")
    if scenario["base_half_width_m"] <= 0 or min(scenario["torque_factor"],scenario["stability_factor"]) < 1:
        raise ValueError("Base positiva e fatores >= 1 são necessários")
    report = calculate(scenario)
    # Relações físicas simples: carga adicional deve aumentar ambas as demandas.
    heavier = calculate({**scenario,"payload_kg":scenario["payload_kg"]+0.1})
    assert heavier["shoulder_static_Nm"] > report["shoulder_static_Nm"]
    assert heavier["elbow_static_Nm"] > report["elbow_static_Nm"]
    build = ROOT/"build"
    build.mkdir(exist_ok=True)
    output = json.dumps(report,ensure_ascii=False,indent=2)+"\n"
    (build/"torque.json").write_text(output,encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
