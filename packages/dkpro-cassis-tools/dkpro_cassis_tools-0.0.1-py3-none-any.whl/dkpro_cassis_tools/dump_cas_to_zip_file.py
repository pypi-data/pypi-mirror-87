import zipfile
from cassis import Cas


def dump_cas_to_zip_file(cas: Cas, zip_file, xmi_name: str = "xmi.xmi", type_system_file: str = "TypeSystem.xml"):
    zf = zipfile.ZipFile(zip_file, "w")
    zf.writestr(type_system_file, cas.typesystem.to_xml())
    zf.writestr(xmi_name, cas.to_xmi(pretty_print=True))
    zf.close()
