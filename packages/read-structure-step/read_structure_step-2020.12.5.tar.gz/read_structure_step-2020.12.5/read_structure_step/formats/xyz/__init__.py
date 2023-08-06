from . import obabel  # noqa: F401
from read_structure_step.formats.registries import register_format_checker
import re


@register_format_checker('.xyz')
def check_format(file_name):

    element_coords_regex = r"""^\s*(A[cglmrstu]|B[aehikr]?|C[adeflmnorsu] \
            ?|D[bsy]|E[rsu]|F[elmr]?|G[ade]|H[efgos]?|I[nr]?|Kr?|L[airuv] \
            |M[dgnot]|N[abdeiop]?|Os?|P[abdmortu]?|R[abefghnu]|S[bcegimnr\]?| \
            T[abcehilm]|U(u[opst])?|V|W|Xe|Yb?|Z[nr \
            ])\s*(\s*-?\d+(\.\d+([-+]e\d+)?)?\s*){3}$"""

    with open(file_name, "r") as f:

        for line_nbr, line in enumerate(f):

            if line_nbr > 2:
                break

            if line_nbr == 0 and re.search(r"^\s*[0-9]+\s*$", line) is None:
                return False

            if line_nbr == 2 and re.search(
                element_coords_regex, line
            ) is not None:
                return True
