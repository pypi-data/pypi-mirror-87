from . import LoadComputers
from ..models import Server


class LoadServers(LoadComputers):
    model = Server
