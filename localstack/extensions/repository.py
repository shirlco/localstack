import logging
import os

from localstack import config, constants
from localstack.utils.venv import VirtualEnvironment

LOG = logging.getLogger(__name__)

LOCALSTACK_VENV = VirtualEnvironment(os.path.join(constants.LOCALSTACK_ROOT_FOLDER, ".venv"))

VENV_DIRECTORY = "extensions/python_venv"


def get_extensions_venv() -> VirtualEnvironment:
    """
    Returns a VirtualEnvironment object point to ``<var_libs>/extensions/python_venv``, either on the host or in the
    container.

    :return: the virtual environment
    """
    return VirtualEnvironment(os.path.join(config.dirs.var_libs, VENV_DIRECTORY))


def init():
    """
    Idempotent operation to ensure the extensions virtual environment is created, and the localstack venv is linked
    into it via a .pth file.
    """
    venv = get_extensions_venv()

    if not venv.exists:
        LOG.info("creating virtual environment at %s", venv.venv_dir)
        venv.create()
        LOG.info("adding localstack venv path %s", venv.venv_dir)
        venv.add_pth("localstack-venv", LOCALSTACK_VENV)

    LOG.info("injecting venv into path %s", venv.venv_dir)
    venv.inject_to_sys_path()
