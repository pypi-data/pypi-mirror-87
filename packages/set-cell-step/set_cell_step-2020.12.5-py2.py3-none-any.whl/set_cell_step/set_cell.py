# -*- coding: utf-8 -*-

"""Non-graphical part of the Set Cell step in a SEAMM flowchart
"""

import logging
import pprint  # noqa: F401

import set_cell_step
import seamm
from seamm_util import ureg, Q_  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

# In addition to the normal logger, two logger-like printing facilities are
# defined: 'job' and 'printer'. 'job' send output to the main job.out file for
# the job, and should be used very sparingly, typically to echo what this step
# will do in the initial summary of the job.
#
# 'printer' sends output to the file 'step.out' in this steps working
# directory, and is used for all normal output from this step.

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('Set Cell')


class SetCell(seamm.Node):
    """
    The non-graphical part of a Set Cell step in a flowchart.

    Attributes
    ----------
    parser : configargparse.ArgParser
        The parser object.

    options : tuple
        It contains a two item tuple containing the populated namespace and the
        list of remaining argument strings.

    subflowchart : seamm.Flowchart
        A SEAMM Flowchart object that represents a subflowchart, if needed.

    parameters : SetCellParameters
        The control parameters for Set Cell.

    See Also
    --------
    TkSetCell,
    SetCell, SetCellParameters
    """

    def __init__(
        self, flowchart=None, title='Set Cell', extension=None, logger=logger
    ):
        """A step for Set Cell in a SEAMM flowchart.

        You may wish to change the title above, which is the string displayed
        in the box representing the step in the flowchart.

        Parameters
        ----------
        flowchart: seamm.Flowchart
            The non-graphical flowchart that contains this step.

        title: str
            The name displayed in the flowchart.
        extension: None
            Not yet implemented
        logger : Logger = logger
            The logger to use and pass to parent classes

        Returns
        -------
        None
        """
        logger.debug('Creating Set Cell {}'.format(self))

        super().__init__(
            flowchart=flowchart,
            title='Set Cell',
            extension=extension,
            module=__name__,
            logger=logger
        )  # yapf: disable

        self.parameters = set_cell_step.SetCellParameters()

    @property
    def version(self):
        """The semantic version of this module.
        """
        return set_cell_step.__version__

    @property
    def git_revision(self):
        """The git version of this module.
        """
        return set_cell_step.__git_revision__

    def description_text(self, P=None):
        """Create the text description of what this step will do.
        The dictionary of control values is passed in as P so that
        the code can test values, etc.

        Parameters
        ----------
        P: dict
            An optional dictionary of the current values of the control
            parameters.

        Returns
        -------
        str
            A description of the current step.
        """
        if not P:
            P = self.parameters.values_to_dict()

        method = P['method']

        if method == 'density':
            density = P['density']
            if self.is_expr(density):
                text = (
                    "The cell will be adjusted isotropically to a density "
                    f"given by '{density}'."
                )
            else:
                text = (
                    "The cell will be adjusted isotropically to a density "
                    f"of {density}."
                )
        elif method == 'volume':
            volume = P['volume']
            if self.is_expr(volume):
                text = (
                    "The cell will be adjusted isotropically to a volume "
                    f"given by '{volume}'."
                )
            else:
                text = (
                    "The cell will be adjusted isotropically to a volume "
                    f"of {volume}."
                )
        elif method == 'cell parameters':
            text = "The cell parameters will be set as follows:"
            for parameter in ('a', 'b', 'c', 'alpha', 'beta', 'gamma'):
                text += f"  {parameter:>5}: {P[parameter]}"
        elif method == 'uniform contraction/expansion':
            text = (
                f"The cell will be adjusted isotropically by {P['expansion']} "
                "in each direction."
            )
        else:
            raise RuntimeError(f"Don't recognize method '{method}'!")

        return self.header + '\n' + __(text, **P, indent=4 * ' ').__str__()

    def run(self):
        """Run a Set Cell step.

        Parameters
        ----------
        None

        Returns
        -------
        seamm.Node
            The next node object in the flowchart.
        """
        next_node = super().run(printer)
        # Get the values of the parameters, dereferencing any variables
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Print what we are doing -- getting formatted values for printing
        PP = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data,
            formatted=True,
            units=False
        )
        self.logger.debug(f'Formatted values:\n{pprint.pformat(PP)}')
        printer.normal(__(self.description_text(PP), indent=self.indent))

        method = P['method']
        system = self.get_variable('_system')

        cell = system.cell.cell()
        a, b, c, alpha, beta, gamma = cell.parameters
        if method == 'density':
            rho = P['density'].to('g/mL').magnitude
            rho0 = system.density()
            delta = (rho0 / rho)**(1 / 3)
            a = a * delta
            b = b * delta
            c = c * delta
        elif method == 'volume':
            V = P['volume'].to('Å^3').magnitude
            V0 = system.volume()
            delta = (V / V0)**(1 / 3)
            a = a * delta
            b = b * delta
            c = c * delta
        elif method == 'cell parameters':
            a = P['a'].to('Å').magnitude
            b = P['b'].to('Å').magnitude
            c = P['c'].to('Å').magnitude
            alpha = P['alpha'].to('degree').magnitude
            beta = P['beta'].to('degree').magnitude
            gamma = P['gamma'].to('degree').magnitude
        elif method == 'uniform contraction/expansion':
            delta = (1 + P['expansion'])**(1 / 3)
            a = a * delta
            b = b * delta
            c = c * delta
        else:
            raise RuntimeError(f"Don't recognize method '{method}'!")

        system.cell.set_cell(a, b, c, alpha, beta, gamma)

        text = '\nAdjusted the cell:\n'
        text += f'         a: {a:8.3f}\n'
        text += f'         b: {b:8.3f}\n'
        text += f'         c: {c:8.3f}\n'
        text += f'     alpha: {alpha:7.2f}\n'
        text += f'      beta: {beta:7.2f}\n'
        text += f'     gamma: {gamma:7.2f}\n'
        text += '\n'
        text += f'    volume: {system.volume():10.1f} Å^3\n'
        text += f'   density: {system.density():11.2f} g/mL\n'

        printer.normal(__(text, indent=self.indent + 4 * ' '))

        printer.normal('')

        # Add other citations here or in the appropriate place in the code.
        # Add the bibtex to data/references.bib, and add a self.reference.cite
        # similar to the above to actually add the citation to the references.

        return next_node
