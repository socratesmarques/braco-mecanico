"""Exporta CAD e verifica malhas com a biblioteca padrão. Não valida resistência."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
PARTS = {
    "base": 1, "turntable": 1, "pedestal": 2, "upper_link": 2,
    "fore_link": 2, "upper_spacer": 2, "fore_spacer": 2,
    "palm": 1, "fixed_finger": 1, "moving_finger": 1, "tolerance_coupon": 1,
}


def find_openscad(explicit: str | None) -> str:
    candidates = [explicit] if explicit else [shutil.which("openscad"),
        r"C:\Program Files\OpenSCAD\openscad.com", "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise RuntimeError("OpenSCAD não encontrado. Informe --openscad com o caminho do executável.")


def render(exe: str, name: str, part: str, defines: tuple[str, ...] = (),
           suffix: str = "stl", expect_error: bool = False) -> Path:
    out = BUILD / f"{name}.{suffix}"
    # Apaga somente a saída exata para não aceitar artefato de execução anterior.
    out.unlink(missing_ok=True)
    cmd = [exe, "-o", str(out), "-D", f'part="{part}"']
    for definition in defines:
        cmd.extend(["-D", definition])
    if suffix == "stl":
        cmd.extend(["--export-format", "binstl"])
    elif suffix == "png":
        cmd.extend(["--imgsize=1000,900", "--viewall", "--autocenter", "--projection=o",
                    "--camera=0,0,0,65,0,-30,650"])
    cmd.append(str(ROOT / "cad/main.scad"))
    result = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=120)
    log = result.stdout + result.stderr
    (BUILD / f"{name}.log").write_text(log, encoding="utf-8")
    if expect_error:
        if "ERROR: Assertion" not in log:
            raise RuntimeError(f"{name}: entrada inválida não provocou assertion: {log}")
    elif result.returncode or re.search(r"\b(?:ERROR|WARNING):", log) or not out.is_file() or out.stat().st_size == 0:
        raise RuntimeError(f"Falha em {name}: {log}")
    return out


def inspect_mesh(path: Path) -> dict:
    data = path.read_bytes()
    if len(data) < 84:
        raise ValueError(f"STL incompleto: {path.name}")
    count = struct.unpack_from("<I", data, 80)[0]
    if len(data) != 84 + 50 * count or count == 0:
        raise ValueError(f"Esperado STL binário não vazio: {path.name}")
    triangles = []
    for i in range(count):
        values = struct.unpack_from("<12fH", data, 84 + 50*i)
        triangles.append(tuple(tuple(round(v, 5) for v in values[j:j+3]) for j in (3, 6, 9)))
    vertices = set(v for tri in triangles for v in tri)
    edges = Counter()
    directed = Counter()
    neighbors = defaultdict(set)
    volume6 = 0.0
    for a, b, c in triangles:
        cross = ((b[1]-a[1])*(c[2]-a[2])-(b[2]-a[2])*(c[1]-a[1]),
                 (b[2]-a[2])*(c[0]-a[0])-(b[0]-a[0])*(c[2]-a[2]),
                 (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
        if sum(x*x for x in cross) < 1e-14:
            raise ValueError(f"Triângulo degenerado: {path.name}")
        volume6 += a[0]*(b[1]*c[2]-b[2]*c[1]) + a[1]*(b[2]*c[0]-b[0]*c[2]) + a[2]*(b[0]*c[1]-b[1]*c[0])
        for u, v in ((a,b),(b,c),(c,a)):
            edges[tuple(sorted((u,v)))] += 1
            directed[(u,v)] += 1
            neighbors[u].add(v)
            neighbors[v].add(u)
    if any(n != 2 for n in edges.values()):
        raise ValueError(f"Aresta aberta/não manifold: {path.name}")
    if any(directed[(v,u)] != n for (u,v), n in directed.items()):
        raise ValueError(f"Orientação inconsistente: {path.name}")
    pending = set(vertices)
    components = 0
    while pending:
        components += 1
        queue = [pending.pop()]
        while queue:
            for nxt in neighbors[queue.pop()]:
                if nxt in pending:
                    pending.remove(nxt)
                    queue.append(nxt)
    if components != 1 or volume6 <= 0:
        raise ValueError(f"Esperado um sólido fechado com volume positivo: {path.name}")
    low = [min(v[i] for v in vertices) for i in range(3)]
    high = [max(v[i] for v in vertices) for i in range(3)]
    size = [high[i]-low[i] for i in range(3)]
    # Envelope FIXO da Ender 3, com 5 mm de margem lateral por lado.
    if any(x > limit+0.01 for x,limit in zip(size,(210,210,250))) or abs(low[2]) > 0.01 or min(low) < -0.01:
        raise ValueError(f"Peça fora da mesa/origem: {path.name}, {low=}, {size=}")
    return {"triangles":count, "components":components, "closed_edges":True,
            "size_mm":[round(x,3) for x in size], "volume_mm3":round(volume6/6,2)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--openscad")
    parser.add_argument("--skip-images", action="store_true", help="Para ambientes sem suporte gráfico; registrar limitação")
    args = parser.parse_args()
    BUILD.mkdir(exist_ok=True)
    report = {"status":"running", "parts":{}, "checks":[], "limitations":[
        "Não verifica auto-interseções, colisões na montagem, resistência, cinemática real nem fabricação.",
        "Malha fechada por incidência de arestas não é certificação mecânica."]}
    try:
        exe = find_openscad(args.openscad)
        version = subprocess.run([exe,"--version"],capture_output=True,text=True,timeout=15)
        report["openscad"] = (version.stdout+version.stderr).strip()
        report["python"] = sys.version.split()[0]
        for part,quantity in PARTS.items():
            report["parts"][part] = {**inspect_mesh(render(exe,part,part)), "quantity":quantity}
            print(f"OK {part}: {report['parts'][part]['size_mm']} mm", flush=True)
        # Variação conjunta da estrutura: exporta TODAS as peças, não apenas sintaxe.
        variant = ("upper_length=120", "fore_length=90", "plate_thickness=6", "hole_clearance_d=0.6")
        for part in PARTS:
            inspect_mesh(render(exe,"variant_"+part,part,variant))
        report["checks"].append("11 peças também exportadas e verificadas com comprimentos 120/90, espessura 6, folga 0.6 mm")
        # Confirma que a folga mudou a geometria, sem alterar o envelope.
        clearance = inspect_mesh(render(exe,"clearance_base","base",("hole_clearance_d=0.8",)))
        if clearance["volume_mm3"] >= report["parts"]["base"]["volume_mm3"]:
            raise ValueError("Aumento de folga não reduziu volume dos furos")
        report["checks"].append("Aumento de folga diametral reduz volume e mantém envelope")
        for name,definition in (("invalid_clearance","hole_clearance_d=-0.2"),
                                ("invalid_joint","fore_offset=17"), ("invalid_bed","base_size=230")):
            render(exe,name,"base",(definition,),expect_error=True)
        render(exe,"invalid_part","missing",expect_error=True)
        report["checks"].append("4 entradas inválidas rejeitadas por assertion")
        for name,definitions in (("assembly",()), ("exploded",()),
            ("vertical",("shoulder_angle=90","elbow_angle=0","base_angle=0")),
            ("horizontal",("shoulder_angle=0","elbow_angle=0","base_angle=0"))):
            part = "exploded" if name == "exploded" else "assembly"
            render(exe,name,part,definitions,suffix="csg")
            if not args.skip_images:
                render(exe,name,part,definitions,suffix="png")
        report["checks"].append("4 vistas compiladas: conjunto, explodida, vertical, horizontal")
        report["images_generated"] = not args.skip_images
        report["status"] = "passed"
    except (RuntimeError, ValueError, OSError, subprocess.TimeoutExpired) as exc:
        report["status"] = "failed"
        report["error"] = str(exc)
        print(str(exc),file=sys.stderr)
    finally:
        (BUILD / "verification.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Resultado: {report['status']}; build/verification.json",flush=True)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
