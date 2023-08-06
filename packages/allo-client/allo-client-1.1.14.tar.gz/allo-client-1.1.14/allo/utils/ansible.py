import os
import subprocess
import sys

import progressbar


class AnsibleUtil:
    def __init__(self, process, widgets):
        self.process = process
        self.iterations = 0
        self.bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength, widgets=widgets)
        self.__process()

    def __wait(self):
        try:
            self.iterations += 1
            self.bar.update(self.iterations)
            self.process.wait(0.2)
            self.bar.finish()
            return True
        except subprocess.TimeoutExpired:
            return False

    def __process(self):
        while not self.__wait():
            # Do nothing, just wait and update progressbar
            pass
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")

    @staticmethod
    def create_user(product):
        AnsibleUtil._run_playbook("create_user.yml", [
            'Création de l\'utilisateur de télémaintenance : ', progressbar.AnimatedMarker()
        ], "user_name=libriciel-{}".format(product.lower()))

    @staticmethod
    def install_dependencies():
        AnsibleUtil._run_playbook("install_allo.yml", [
            'Installation des dépendances : ', progressbar.AnimatedMarker()
        ])

    @staticmethod
    def start_telem():
        AnsibleUtil._run_playbook("start_service.yml", [
            'Lancement de la télémaintenance : ', progressbar.AnimatedMarker()
        ])

    @staticmethod
    def stop_telem():
        AnsibleUtil._run_playbook("stop_service.yml", [
            'Arrêt de la télémaintenance : ', progressbar.AnimatedMarker()
        ])

    @staticmethod
    def _run_playbook(ymlfile, widgets, pb_vars=""):

        fh = open(os.devnull, "w")
        AnsibleUtil(subprocess.Popen(
            (
                'ansible-playbook',
                os.path.dirname(os.path.realpath(__file__)) + "/playbooks/" + ymlfile,
                "--extra-vars",
                pb_vars
            ), stdout=fh, stderr=fh), widgets)

        fh.close()
