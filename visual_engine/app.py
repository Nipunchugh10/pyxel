"""Pyxel Canvas desktop app.

    python visual_engine/app.py                        # run the app
    python visual_engine/app.py --selftest report.json # drive the UI, write a report, exit

The frozen build (Pyxel.exe) accepts the same arguments.
"""
import argparse
import json
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

WEBVIEW2_URL = "https://developer.microsoft.com/microsoft-edge/webview2/"


def _message_box(title, text):
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, text, title, 0x10)   # MB_ICONERROR
    else:
        print(f"{title}: {text}", file=sys.stderr)


def _start_failure_help(exc):
    """Explain a start-up failure without guessing: only blame WebView2 when the
    error is actually about WebView2."""
    detail = f"{type(exc).__name__}: {exc}"
    if "webview2" in detail.lower() and "python.runtime" not in detail.lower():
        return ("Pyxel needs Microsoft Edge WebView2, which is part of Windows 11 "
                "and up-to-date Windows 10.\n\nInstall the free \"Evergreen Runtime\" "
                f"from:\n{WEBVIEW2_URL}\n\nDetails: {detail}")
    return ("Pyxel could not open its window.\n\n"
            "If you downloaded Pyxel, Windows may have blocked its files: delete the "
            "unzipped folder, right-click the zip > Properties > tick \"Unblock\" > OK, "
            "and unzip it again.\n\n"
            f"Details: {detail}")


def _safe_streams():
    """A windowed exe has no console (stdout is None), and a redirected one may
    use a legacy codepage that cannot encode the emoji in log messages. Neither
    may ever turn a print() into a failed export."""
    import io
    import os
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name)
        if stream is None:
            setattr(sys, name, open(os.devnull, "w", encoding="utf-8"))
        elif isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main(argv=None):
    _safe_streams()
    parser = argparse.ArgumentParser(description="Pyxel Canvas")
    parser.add_argument("--selftest", metavar="REPORT", help="run the UI self-test and exit")
    args = parser.parse_args(argv)

    # Patterns describe controls with ipywidgets; the app only reads them, so a
    # light stand-in replaces the real package (and the IPython stack it pulls in)
    from desktop import widget_shim
    widget_shim.install()

    import webview
    from desktop.backend import Backend
    from desktop.paths import APP_VERSION, ui_dir

    backend = Backend()
    window = webview.create_window(
        f"Pyxel Canvas {APP_VERSION}", url=str(ui_dir() / "index.html"),
        js_api=backend, width=1440, height=900, min_size=(1100, 700),
        background_color="#0d0f1a")
    backend._window = window

    if args.selftest:
        def start_selftest():
            window.run_js("runSelfTest()")   # fire and forget: evaluate_js would block on the promise
        window.events.loaded += start_selftest
        # Never hang a build check: give up after 10 minutes
        guard = threading.Timer(600, window.destroy)
        guard.daemon = True          # must not keep the process alive after a normal exit
        guard.start()

    try:
        # Force Edge WebView2: never fall back to the legacy IE engine
        webview.start(gui="edgechromium", http_server=True)
    except Exception as exc:
        if args.selftest:            # a build check must report, never block on a dialog
            Path(args.selftest).write_text(json.dumps({"errors": [f"start failed: {exc}"]}),
                                           encoding="utf-8")
            return 3
        _message_box("Pyxel Canvas could not start", _start_failure_help(exc))
        return 1

    if args.selftest:
        report = getattr(backend, "_selftest_result", None) or {"errors": ["self-test did not finish"]}
        Path(args.selftest).write_text(json.dumps(report, indent=2), encoding="utf-8")
        return 0 if not report.get("errors") else 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
