from . import LoadComputers
from ..models import Workstation


class LoadWorkstations(LoadComputers):
    model = Workstation
