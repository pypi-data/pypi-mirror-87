import click
from allo.model.config import AlloConfig
from allo.model.colors import BColors
from .telem import TelemUtil


@click.group(invoke_without_command=True)
@click.pass_context
def telem(ctx):
    """Affiche l'état de la télémaintenance."""
    if not hasattr(AlloConfig.load(), "teleport_token"):
        BColors.error("Allo non initialisé. Merci de lancer la commande 'allo'")
        exit(1)

    if not ctx.invoked_subcommand:
        TelemUtil.telem_status()


@telem.command()
def start():
    """Lancement de la télémaintenance."""
    TelemUtil.telem_start()


@telem.command()
def stop():
    """Arrêt de la télémaintenance."""
    TelemUtil.telem_stop()
