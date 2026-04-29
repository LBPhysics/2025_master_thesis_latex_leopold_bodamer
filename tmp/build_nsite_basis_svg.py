import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
INKSCAPE_NS = "http://www.inkscape.org/namespaces/inkscape"
SODIPODI_NS = "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
TEXTEXT_NS = "http://www.iki.fi/pav/software/textext/"
XLINK_NS = "http://www.w3.org/1999/xlink"

ET.register_namespace("", SVG_NS)
ET.register_namespace("svg", SVG_NS)
ET.register_namespace("inkscape", INKSCAPE_NS)
ET.register_namespace("sodipodi", SODIPODI_NS)
ET.register_namespace("textext", TEXTEXT_NS)
ET.register_namespace("xlink", XLINK_NS)

repo = Path(r"c:\Users\leopo\.vscode\Master_thesis-1")
svg_path = repo / "latex" / "figures" / "svgs" / "rslts_nsite_site_vs_exciton_basis.svg"
preamble = repo / "latex" / "figures" / "svgs" / "textext_preamble.tex"

inkscape_py = Path(r"C:\Program Files\Inkscape\bin\python.exe")
textext_main = Path(r"C:\Users\leopo\AppData\Roaming\inkscape\extensions\textext\__main__.py")

env = dict(**__import__("os").environ)
env["PYTHONPATH"] = r"C:\Program Files\Inkscape\share\inkscape\extensions;C:\Users\leopo\AppData\Roaming\inkscape\extensions"

labels = [
    (r"$\mathbf{Site\ basis}$", 102, 55, 1.00),
    (r"$\{\,|g\rangle,\ |n\rangle,\ |mn\rangle\,\}$", 60, 93, 0.88),
    (r"$|g\rangle$", 145, 438, 0.95),
    (r"$\{|n\rangle\}_{n=1}^{N_{\mathrm{sites}}}$", 78, 322, 0.78),
    (r"$\{|mn\rangle\}_{1\le m<n\le N_{\mathrm{sites}}}$", 64, 188, 0.70),

    (r"$\mathbf{Truncation\ and\ bookkeeping}$", 362, 55, 0.82),
    (r"$\mathcal{B}_{1\mathrm{ex}}=\{|g\rangle,|1\rangle,\ldots,|N_{\mathrm{sites}}\rangle\}$", 360, 146, 0.58),
    (r"$\mathcal{B}_{2\mathrm{ex}}=\mathcal{B}_{1\mathrm{ex}}\cup\{|mn\rangle\}_{1\le m<n\le N_{\mathrm{sites}}}$", 347, 206, 0.54),
    (r"$\dim\mathcal{H}=1+N_{\mathrm{sites}}+\binom{N_{\mathrm{sites}}}{2}$", 392, 274, 0.72),
    (r"$\hat N|g\rangle=0,\ \hat N|n\rangle=1,\ \hat N|mn\rangle=2$", 390, 333, 0.70),

    (r"$\mathbf{One\mbox{-}exciton\ basis}$", 726, 55, 0.92),
    (r"$|\alpha\rangle=\sum_{n=1}^{N_{\mathrm{sites}}} c_{\alpha n}|n\rangle$", 706, 167, 0.80),
    (r"$\hat H_{1\mathrm{ex}}|\alpha\rangle=\omega_{\alpha}|\alpha\rangle$", 720, 228, 0.78),
    (r"$|mn\rangle\ \mathrm{kept\ for\ ESA}$", 724, 188, 0.70),
    (r"$\mu_{g\alpha},\ \mu_{\alpha,mn}$", 770, 258, 0.78),
    (r"$|g\rangle\ \mathrm{unchanged}$", 765, 438, 0.82),

    (r"$\mathrm{diagonalise}\ \hat H_{1\mathrm{ex}}$", 438, 300, 0.70),
    (r"$\mathrm{project\ to\ one\text{-}exciton\ block}$", 438, 340, 0.56),
]


def find_textext_groups(root):
    out = []
    for el in root.iter():
        if not el.tag.endswith("g"):
            continue
        if any(key == f"{{{TEXTEXT_NS}}}text" for key in el.attrib):
            out.append(el)
    return out


def collect_existing_texts(root):
    texts = set()
    for g in find_textext_groups(root):
        key = f"{{{TEXTEXT_NS}}}text"
        if key in g.attrib:
            texts.add(g.attrib[key])
    return texts


root0 = ET.fromstring(svg_path.read_bytes())
existing_texts = collect_existing_texts(root0)

for latex_text, x, y, scale in labels:
    if latex_text in existing_texts:
        continue

    svg_bytes = svg_path.read_bytes()
    cmd = [
        str(inkscape_py),
        str(textext_main),
        "--text",
        latex_text,
        "--preamble-file",
        str(preamble),
        "--scale-factor",
        str(scale),
        "--tex_command",
        "lualatex",
    ]
    proc = subprocess.run(
        cmd,
        input=svg_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        check=True,
        timeout=180,
    )

    root = ET.fromstring(proc.stdout)
    groups = find_textext_groups(root)
    if not groups:
        raise RuntimeError(f"No TexText group found after adding {latex_text}")

    g = groups[-1]
    old_transform = g.get("transform", "")
    g.set("transform", f"translate({x} {y}) {old_transform}".strip())

    svg_path.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))
    existing_texts.add(latex_text)

print(f"Updated {svg_path}")
