# PyInstaller spec for the Pyxel Canvas desktop app (one-folder build).
# Build with:  python packaging/build_release.py
import os
from pathlib import Path

ROOT = Path(SPECPATH).resolve().parent
VE = ROOT / "visual_engine"
VERSION = os.environ.get("PYXEL_VERSION", "1.0.0")
vparts = tuple(int(x) for x in VERSION.split(".")) + (0,)

a = Analysis(
    [str(VE / "app.py")],
    pathex=[str(VE)],
    datas=[
        (str(VE / "desktop" / "ui"), "desktop/ui"),
        (str(VE / "notebook.ipynb"), "."),          # source of the concept notes
    ],
    hiddenimports=[],
    excludes=[
        # Development / notebook tooling installed in .venv but not used by the app
        "jupyterlab", "notebook", "jupyter_server", "jupyter_client", "nbconvert",
        "pytest", "pyflakes", "sphinx",
        # Notebook-only: the app uses desktop/widget_shim.py instead of ipywidgets
        "ipywidgets", "IPython", "ipykernel", "jedi", "parso", "zmq", "comm",
        "prompt_toolkit", "debugpy", "tornado", "traitlets", "jupyter_core",
        # Other GUI toolkits matplotlib or pywebview could pull in
        "tkinter", "PyQt5", "PyQt6", "PySide2", "PySide6", "gi",
    ],
    noarchive=False,
)
pyz = PYZ(a.pure)

from PyInstaller.utils.win32.versioninfo import (  # noqa: E402
    VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct,
    VarFileInfo, VarStruct)

version_info = VSVersionInfo(
    ffi=FixedFileInfo(filevers=vparts, prodvers=vparts),
    kids=[
        StringFileInfo([StringTable("040904B0", [
            StringStruct("CompanyName", "Nipun Chugh"),
            StringStruct("FileDescription", "Pyxel Canvas"),
            StringStruct("FileVersion", VERSION),
            StringStruct("InternalName", "Pyxel"),
            StringStruct("LegalCopyright", "MIT License"),
            StringStruct("OriginalFilename", "Pyxel.exe"),
            StringStruct("ProductName", "Pyxel Canvas"),
            StringStruct("ProductVersion", VERSION),
        ])]),
        VarFileInfo([VarStruct("Translation", [1033, 1200])]),
    ],
)

exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="Pyxel",
    icon=str(ROOT / "packaging" / "pyxel.ico"),
    version=version_info,
    console=False,               # windowed app: no console window
    upx=False,
)
coll = COLLECT(exe, a.binaries, a.datas, name="Pyxel", upx=False)
