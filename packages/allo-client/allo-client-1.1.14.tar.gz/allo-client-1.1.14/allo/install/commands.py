import os
import time
import click
from allo.model.colors import BColors

from allo.model.config import AlloConfig


def exit_if_no_conf():
    if not hasattr(AlloConfig.load(), "repo_path"):
        BColors.error("Produit non installé ou non détecté.")
        exit(1)

@click.command()
def install():
    """Demande d'installation du produit."""
    from allo.telem.telem import TelemUtil
    from allo.utils.api import API
    from allo.utils.ansible import AnsibleUtil
    from allo.utils.logreader import LogReader

    # Install deps and init allo yml file
    AnsibleUtil.install_dependencies()
    TelemUtil.telem_start()
    # Wait 2 seconds, waiting for node to be visible on teleport side
    time.sleep(2)

    fileresult = "/tmp/install_result"

    if os.path.exists(fileresult):
        os.remove(fileresult)
    API.ask_install()

    logreader = LogReader(1, "/tmp/install.log", False)
    logreader.start()

    print("En attente de lancement de l'installation ...")

    while not os.path.exists(fileresult):
        time.sleep(1)

    print("Installation terminée")
    logreader.stop()
    logreader.join()
