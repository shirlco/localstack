import logging
import os

from localstack import config, constants
from localstack.utils.venv import VirtualEnvironment

LOG = logging.getLogger(__name__)

LOCALSTACK_VENV = VirtualEnvironment(os.path.join(constants.LOCALSTACK_ROOT_FOLDER, ".venv"))

VENV_DIRECTORY = "extensions/python_venv"


def get_extensions_venv():
    return VirtualEnvironment(os.path.join(config.dirs.var_libs, VENV_DIRECTORY))


def init():
    venv = get_extensions_venv()

    if not venv.exists:
        LOG.info("creating virtual environment at %s", venv.venv_dir)
        venv.create()
        LOG.info("adding localstack venv path %s", venv.venv_dir)
        venv.add_pth("localstack-venv", LOCALSTACK_VENV)

    LOG.info("injecting venv into path %s", venv.venv_dir)
    venv.inject_to_sys_path()
