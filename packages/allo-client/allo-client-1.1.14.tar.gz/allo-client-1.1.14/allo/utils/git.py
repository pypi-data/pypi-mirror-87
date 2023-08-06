from allo.model.colors import BColors
from git import Repo, InvalidGitRepositoryError

from allo.model.config import AlloConfig


class GitHelper:
    """
    Utilitaire GIT pour allo, ajoutant une couche d'abstraction
    """
    def __init__(self):
        self.allo_config = AlloConfig.load()
        if hasattr(self.allo_config, "repo_path"):
            self.set_git_root_directory(self.allo_config.repo_path)

    def set_git_root_directory(self, path: str):
        # Set repo path and save config
        self.allo_config.repo_path = path
        self.allo_config.save()

    def init_repo(self, message: str):
        if not self.__load_repo(False):
            self.git_repo = Repo.init(self.allo_config.repo_path)
            self.git_repo.git.add(all=True)
            self.git_repo.index.commit(message)

    def get_diff(self):
        if not self.__load_repo():
            return ""
        head = self.git_repo.head.commit.tree
        return self.git_repo.git.diff(head).rstrip()

    def update(self, message: str):
        if not self.__load_repo():
            return
        self.git_repo.git.add(all=True)
        self.git_repo.index.commit(message)

    def __load_repo(self, print_error: bool = True):
        try:
            self.git_repo = Repo(self.allo_config.repo_path)
        except InvalidGitRepositoryError:
            if print_error:
                BColors.warning("Répertoire non initialisé")
            return False
        return True


