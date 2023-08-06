import click
from allo.model.config import AlloConfig
from allo.model.colors import BColors


def exit_if_no_conf():
    if not hasattr(AlloConfig.load(), "repo_path"):
        BColors.error("Produit non installé ou non détecté.")
        exit(1)


@click.group(invoke_without_command=True)
@click.pass_context
def changes(ctx):
    """Liste des différences dans l'application."""

    if not ctx.invoked_subcommand:
        if not hasattr(AlloConfig.load(), "repo_path"):
            return
        from allo.utils.git import GitHelper
        print(GitHelper().get_diff())


@changes.command(name='init')
@click.argument('path')
@click.argument('message')
def init_git_repo(path, message):
    """Initialisation du dossier d'installation.

    \b
    PATH est le chemin de l'installation.
    MESSAGE est le message d'initialisation.
    """
    from allo.utils.git import GitHelper
    helper = GitHelper()
    helper.set_git_root_directory(path)
    helper.init_repo(message)

    BColors.success("Dossier initialisé")


@changes.command(name='update')
@click.argument('message')
def update_git_reo(message):
    """Modification du dossier d'installation.

    \b
    MESSAGE est le message de modification.
    """
    from allo.utils.git import GitHelper
    exit_if_no_conf()
    GitHelper().update(message)

    BColors.success("Dossier mis à jour")
