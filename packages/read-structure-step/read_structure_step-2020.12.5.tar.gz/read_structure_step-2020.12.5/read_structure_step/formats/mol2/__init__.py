from read_structure_step.formats.registries import register_format_checker
from . import obabel  # noqa: F401

keywords = ['@<TRIPOS>']


@register_format_checker('.mol2')
def check_format(file_name):

    with open(file_name, "r") as f:

        data = f.read()

        if all(keyword in data for keyword in keywords):
            return True
        else:
            return False
