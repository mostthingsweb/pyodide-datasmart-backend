import sys
from unittest.mock import MagicMock

sys.modules["fcntl"] = MagicMock(name="fcntl")
sys.modules["codegen"] = MagicMock(name="codegen")

from pathlib import Path, PurePosixPath
from workers import Response, WorkerEntrypoint
import zipimport

_BITBAKE_ZIP_FILE = Path(__file__).resolve().parent / "bundled" / "yocto-5.2.4.zip"
imp = zipimport.zipimporter(str(_BITBAKE_ZIP_FILE / "bitbake-yocto-5.2.4" / "lib"))

imp.load_module("bs4")
bb = imp.load_module("bb")

import bb.data_smart
from bb.data_smart import DataSmart

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        try:
            ds = DataSmart()
            return Response(f"DataSmart import OK ({DataSmart.__module__}), obj={ds}")
        except Exception as exc:
            return Response(f"DataSmart import failed: {exc!r}\nsys.path={sys.path}")
    
