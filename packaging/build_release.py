"""Build the Windows release: Pyxel.exe (one-folder) -> zip -> SHA-256.

    python packaging/build_release.py            # build dist/Pyxel-v<version>-win64.zip
    python packaging/build_release.py --verify   # ...then run the exe's UI self-test

Output in dist/: the Pyxel/ folder, the zip, and a .sha256 file.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "visual_engine"))
from desktop.paths import APP_VERSION  # noqa: E402

DIST = ROOT / "dist"
APP_DIR = DIST / "Pyxel"
ZIP = DIST / f"Pyxel-v{APP_VERSION}-win64.zip"


def run(cmd, **kw):
    print("$", " ".join(map(str, cmd)), flush=True)
    subprocess.run(cmd, check=True, **kw)


def running_from_dist():
    """True if a Pyxel.exe from dist/ is running: Windows locks its files, so
    PyInstaller could not replace the folder (and would half-delete it)."""
    if sys.platform != "win32":
        return False
    out = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "Get-Process Pyxel -ErrorAction SilentlyContinue | ForEach-Object { $_.Path }"],
        capture_output=True, text=True).stdout
    return any(Path(p).resolve().is_relative_to(DIST.resolve())
               for p in out.split() if p.strip())


def build():
    if running_from_dist():
        sys.exit("Pyxel.exe from dist/ is running. Close it, then build again.")
    run([sys.executable, str(ROOT / "packaging" / "make_icon.py")])
    run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
         "--distpath", str(DIST), "--workpath", str(ROOT / "build"),
         str(ROOT / "packaging" / "pyxel.spec")],
        env={**os.environ, "PYXEL_VERSION": APP_VERSION})
    # User-facing documents next to the exe
    readme = (ROOT / "packaging" / "README.txt").read_text(encoding="utf-8")
    (APP_DIR / "README.txt").write_text(readme.replace("{version}", APP_VERSION), encoding="utf-8")
    shutil.copy(ROOT / "LICENSE", APP_DIR / "LICENSE.txt")
    shutil.copy(ROOT / "CHANGELOG.md", APP_DIR / "CHANGELOG.md")


def package():
    ZIP.unlink(missing_ok=True)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(APP_DIR.rglob("*")):
            if path.is_file():
                zf.write(path, Path("Pyxel") / path.relative_to(APP_DIR))
    digest = hashlib.sha256(ZIP.read_bytes()).hexdigest().upper()
    (DIST / (ZIP.name + ".sha256")).write_text(f"{digest}  {ZIP.name}\n", encoding="ascii")
    size = sum(p.stat().st_size for p in APP_DIR.rglob("*") if p.is_file())
    print(f"\n{ZIP.name}: {ZIP.stat().st_size / 2**20:.1f} MB zipped, "
          f"{size / 2**20:.1f} MB unzipped\nSHA-256: {digest}")
    return digest


def verify():
    """Unzip the release to a fresh folder and run the exe's UI self-test there."""
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(ZIP) as zf:
            zf.extractall(tmp)
        exe = Path(tmp) / "Pyxel" / "Pyxel.exe"
        report = Path(tmp) / "selftest.json"
        # Minimal environment: no Python on PATH, no PYTHON* variables
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith("PYTHON")}
        env["PATH"] = os.pathsep.join([r"C:\Windows\System32", r"C:\Windows"])
        code = subprocess.run([str(exe), "--selftest", str(report)], env=env, cwd=tmp,
                              timeout=900).returncode
        result = json.loads(report.read_text(encoding="utf-8"))
        ok = (code == 0 and result.get("welcome") and result.get("backHome")
              and not result.get("errors") and not result["notes"]["katexErrors"]
              and all(c["rendered"] and c["splitEqual"] and c["resetDisabledOnLoad"]
                      for c in result["categories"])
              and result.get("notAtDefault") == []
              and result.get("reset", {}).get("betaDefault") == 2.667
              and all(result["reset"].get(k) for k in ("disabledAtStart", "enabledAfterEdit", "restored"))
              and any(c.get("png", "").startswith("Saved ") for c in result["categories"])
              and any(c.get("gif", "").startswith("Saved ") for c in result["categories"]))
        print(json.dumps(result, indent=1))
        print("\nFROZEN SELF-TEST:", "PASS" if ok else f"FAIL (exit {code})")
        return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="run the exe self-test after building")
    ap.add_argument("--skip-build", action="store_true", help="re-zip/verify an existing build")
    args = ap.parse_args()
    if not args.skip_build:
        build()
    package()
    if args.verify and not verify():
        sys.exit(1)
