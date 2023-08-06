#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .changes import commands as changes
from .telem import commands as telem
from .update import commands as update
from .install import commands as install

import click
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@click.group(invoke_without_command=True)
@click.version_option()
@click.pass_context
def cmd(ctx):
    """Outil de télémaintenance et de mise à jour automatique Libriciel-SCOP"."""

    from allo.model.config import AlloConfig
    from allo.model.colors import BColors

    if not ctx.invoked_subcommand:
        import allo
        from allo.utils.configloader import ConfigLoader
        from allo.utils.ansible import AnsibleUtil

        BColors.info("ALLO-NG v{} - Utilitaire de mise a jour automatique et telemaintenance".format(allo.__version__))

        AnsibleUtil.install_dependencies()
        ConfigLoader("PROD")

        BColors.success("Initialisation terminée")
    elif not hasattr(AlloConfig.load(), "teleport_token"):
        BColors.error("Allo non initialisé. Merci de lancer la commande 'allo'")
        exit(1)


cmd.add_command(changes.changes)
cmd.add_command(telem.telem)
cmd.add_command(update.update)
cmd.add_command(install.install)
