from read_structure_step.formats.registries import register_format_checker
from . import obabel  # noqa: F401

mandatory_keywords = [
    "HEADER", "TITLE", "COMPND", "SOURCE", "KEYWDS", "EXPDTA", "AUTHOR",
    "REVDAT", "REMARK 2", "REMARK 3", "SEQRES", "CRYST1",
    "ORIGX1 ORIGX2 ORIGX3", "SCALE1 SCALE2 SCALE3", "MASTER", "END"
]

optional_keywords = [
    "OBSLTE", "SPLIT", "CAVEAT", "NUMMDL", "MDLTYP", "SPRSDE", "JRNL",
    "REMARK 0", "REMARK 1", "REMARK N", "DBREF", "DBREF1/DBREF2", "SEQADV",
    "MODRES", "HET", "HETNAM", "HETSYN", "FORMUL", "HELIX", "SHEET", "SSBOND",
    "LINK", "CISPEP", "SITE", "MTRIX1 MTRIX2 MTRIX3", "MODEL", "ATOM",
    "ANISOU", "TER", "HETATM", "ENDMDL", "CONECT"
]


@register_format_checker('.pdb')
def check_format(file_name):

    with open(file_name, "r") as f:

        data = f.read()

        if any(keyword in data for keyword in mandatory_keywords):
            return True
        else:

            if any(keyword in data for keyword in optional_keywords):
                return True
            else:
                return False
