import sys
from unittest.mock import MagicMock

sys.modules["fcntl"] = MagicMock(name="fcntl")
sys.modules["codegen"] = MagicMock(name="codegen")
sys.modules["hashserv"] = MagicMock(name="hashserv")
sys.modules["hashserv.client"] = MagicMock(name="hashserv.client")


from pathlib import Path, PurePosixPath
from workers import Response, WorkerEntrypoint
import zipimport

_BITBAKE_ZIP_FILE = Path(__file__).resolve().parent / "bundled" / "yocto-5.2.4.zip"
zip_loader = zipimport.zipimporter(str(_BITBAKE_ZIP_FILE / "bitbake-yocto-5.2.4" / "lib"))

zip_loader.load_module("simplediff")
bb = zip_loader.load_module("bb")

import bb.data_smart
import bb.parse
import bb.siggen
from bb.data_smart import DataSmart
import tempfile

def parsehelper(content, suffix = ".bb"):
    f = tempfile.NamedTemporaryFile(suffix = suffix)
    f.write(bytes(content, "utf-8"))
    f.flush()
    # os.chdir(os.path.dirname(f.name))
    return f


DOC = """
A = "G"
B = "C"
C = "${B} ${A}"

"""

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        with parsehelper(DOC) as f:
            d = DataSmart()
            bb.parse.siggen = bb.siggen.init(d)
            d = bb.parse.handle(f.name, d)['']

        # d = DataSmart()
        # d.setVar("A", "B")

        return Response(f"{d.getVar("C")}")

        
