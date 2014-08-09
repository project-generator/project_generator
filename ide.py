from uvision4 import Uvision4
from gccarm import GccArm

IDE_SUPPORTED = {
    'uvision': Uvision4,
    #'gcc_arm': GccArm,
}

def export(data, ide):
    if ide not in IDE_SUPPORTED:
        raise RuntimeError("Non supported IDE")

    Exporter = IDE_SUPPORTED[ide]
    exporter = Exporter()
    #run exporter for defined bootloader project
    exporter.generate(data, ide)
