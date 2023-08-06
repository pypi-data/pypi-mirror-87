# -*- coding: utf-8 -*-

"""
set_cell_step
A plug-in for setting the periodic (unit) cell in a SEAMM flowchart
"""

# Bring up the classes so that they appear to be directly in
# the set_cell_step package.

from set_cell_step.set_cell import SetCell  # noqa: F401, E501
from set_cell_step.set_cell_parameters import SetCellParameters  # noqa: F401, E501
from set_cell_step.set_cell_step import SetCellStep  # noqa: F401, E501
from set_cell_step.tk_set_cell import TkSetCell  # noqa: F401, E501

# Handle versioneer
from ._version import get_versions
__author__ = """Paul Saxe"""
__email__ = 'psaxe@molssi.org'
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
