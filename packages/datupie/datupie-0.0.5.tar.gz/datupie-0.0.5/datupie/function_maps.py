from datupie.core.startproject import StartCommand
from datupie.core.deployproject import DeployCommand
from datupie.core.destroyproject import DestroyCommand
from datupie.core.cloneproject import CloneCommand
#from core.startproject import StartCommand
#from core.deployproject import DeployCommand
#from core.destroyproject import DestroyCommand
#from core.cloneproject import CloneCommand

FUNCTION_MAP = {
    'startproject': StartCommand().startproject,
    'deployproject': DeployCommand().deployproject,
    'destroyproject': DestroyCommand().destroyproject,
    'cloneproject': CloneCommand().cloneproject,
}