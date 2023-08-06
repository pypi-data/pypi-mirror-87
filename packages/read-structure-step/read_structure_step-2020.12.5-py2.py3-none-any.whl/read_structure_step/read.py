"""
The public interface to the read_structure_step SEAMM plugin
"""

from . import utils
from . import formats
import os


def read(file_name, system, extension=None):
    """
    Calls the appropriate functions to parse the requested file.

    Parameters
    ----------
    file_name : str
        Name of the file

    system : System
        The SEAMM system to read into

    extension : str, optional, default: None

    Returns
    -------
    None
    """

    if type(file_name) is not str:
        raise TypeError(
            """read_structure_step: The file name must be a string, but a
            %s was given. """ % str(type(file_name))
        )

    if file_name == '':
        raise NameError(
            """read_structure_step: The file name for the structure file
            was not specified."""
        )

    file_name = os.path.abspath(file_name)

    if extension is None:

        extension = utils.guess_extension(file_name, use_file_name=True)

        if extension is None:

            extension = utils.guess_extension(file_name, use_file_name=False)

    else:
        extension = utils.sanitize_file_format(extension)

    if extension is None:
        raise NameError("Extension could not be identified")

    if extension not in formats.registries.REGISTERED_READERS.keys():
        raise KeyError(
            'read_structure_step: the file format %s was not recognized.' %
            extension
        )

    reader = formats.registries.REGISTERED_READERS[extension]

    reader(file_name, system)
