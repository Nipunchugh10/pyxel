"""Filesystem locations for the desktop app, in development and when frozen."""
import sys
from pathlib import Path

APP_NAME = "Pyxel"
APP_VERSION = "1.0.1"
SOURCE_URL = "https://github.com/Nipunchugh10/pyxel"


def bundle_root() -> Path:
    """The visual_engine directory: next to this file in development, or
    PyInstaller's unpacked bundle (sys._MEIPASS) in the frozen app."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[1]


def ui_dir() -> Path:
    return bundle_root() / "desktop" / "ui"


def notebook_path() -> Path:
    return bundle_root() / "notebook.ipynb"


def pictures_dir() -> Path:
    """The user's Pictures folder via the Windows known-folder API (follows
    OneDrive or a moved Pictures folder); falls back to ~/Pictures."""
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes
            from uuid import UUID

            class GUID(ctypes.Structure):
                _fields_ = [("Data1", wintypes.DWORD), ("Data2", wintypes.WORD),
                            ("Data3", wintypes.WORD), ("Data4", wintypes.BYTE * 8)]

            u = UUID("33E28130-4E1E-4676-835A-98395C3BC3BB")   # FOLDERID_Pictures
            guid = GUID(u.fields[0], u.fields[1], u.fields[2],
                        (wintypes.BYTE * 8).from_buffer_copy(u.bytes[8:]))
            out = ctypes.c_wchar_p()
            shell32 = ctypes.windll.shell32
            if shell32.SHGetKnownFolderPath(ctypes.byref(guid), 0, None,
                                            ctypes.byref(out)) == 0:
                path = Path(out.value)
                ctypes.windll.ole32.CoTaskMemFree(out)
                return path
        except Exception:
            pass
    return Path.home() / "Pictures"


def exports_dir() -> Path:
    return pictures_dir() / APP_NAME
