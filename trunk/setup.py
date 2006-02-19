# setup.py
from distutils.core import setup
import py2exe
import glob

opts = {
    "py2exe": {
        "includes": "pango,atk,gobject",
        "dll_excludes": [
        "iconv.dll","intl.dll","libatk-1.0-0.dll",
        "libgdk_pixbuf-2.0-0.dll","libgdk-win32-2.0-0.dll",
        "libglib-2.0-0.dll","libgmodule-2.0-0.dll",
        "libgobject-2.0-0.dll","libgthread-2.0-0.dll",
        "libgtk-win32-2.0-0.dll","libpango-1.0-0.dll",
        "libpangowin32-1.0-0.dll"],
        }
    }

setup(
    name = "PyAcqua",
    description = "Programma per la gestione degli acquari.",
    version = "0.8",
    windows = [
        {"script": "gui.py",
        "icon_resources": [(1, "pyacqua.ico")]
        }
    ],
    options=opts,
    data_files=[("pixmaps", glob.glob("pixmaps/*"))
    ],
)