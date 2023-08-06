import zipfile
from typing import Union, Tuple
from typing import BinaryIO
from cassis import Cas, TypeSystem, load_typesystem, load_cas_from_xmi


def load_cas_from_zip_file(f: BinaryIO, return_type_system=False) -> Union[Cas, Tuple[Cas, TypeSystem]]:
    archive = zipfile.ZipFile(f)

    # Type system
    type_system_file = list(filter(
        lambda f: f.filename.endswith('.xml'),
        archive.infolist()))[0]
    with archive.open(type_system_file, 'r') as f:
        type_system = load_typesystem(f)

    # Xmi
    xmi_file = list(filter(
        lambda f: f.filename.endswith('.xmi'),
        archive.infolist()))[0]
    with archive.open(xmi_file, 'r') as f:
        cas = load_cas_from_xmi(f, typesystem=type_system)

    if return_type_system:
        return cas, type_system
    else:
        return cas
