from typing import Optional
import zipfile
from cassis import Cas


def dump_cas_to_zip_file(
        cas: Cas,
        zip_file: str,
        xmi_file: Optional[str] = None,
        type_system_file: Optional[str] = None):

    if xmi_file is None:
        xmi_file = "xmi.xmi"

    if type_system_file is None:
        type_system_file = "TypeSystem.xml"

    zf = zipfile.ZipFile(zip_file, "w")
    zf.writestr(type_system_file, cas.typesystem.to_xml())
    zf.writestr(xmi_file, cas.to_xmi(pretty_print=True))
    zf.close()
