# -*- coding: utf-8 -*-
from time import sleep

from PyInquirer import prompt

from .ansible import AnsibleUtil
from .. import const
from ..model.colors import BColors
from ..model.config import AlloConfig
from ..utils.api import API


class ConfigLoader:
    def __init__(self, env):
        self.config = AlloConfig.load()
        # Check we have (id_client OR internal) AND teleport_token
        if (hasattr(self.config, "id_client") or self.config.internal) and hasattr(self.config, "teleport_token"):
            self.found_instance = API.find_instance()
        else:
            # We have to load the self.config from association
            self.config.env = env
            self.found_instance = API.find_instance()
            self.secret = API.get_secret()
            # We handle the found state and save the config file
            self.handle_state()
            # Create specific user to access node only if product is well known
            if self.config.code_produit in const.CODEPRODUIT.values():
                AnsibleUtil.create_user(self.config.code_produit.lower())
        self.__show_instance_informations()

    def __show_instance_informations(self):
        if "server_node_c" not in self.found_instance:
            BColors.header("Instance interne détectée")
        else:
            account_name = self.found_instance["account"]["name"]\
                if self.found_instance["account"] is not None and "name" in self.found_instance["account"] \
                else "Aucun compte associé"
            BColors.header("- Compte              : {}".format(account_name) + "\n" +
                           "- Type d'exploiration : {}".format(self.found_instance["type_exploitation"]) + "\n" +
                           "- Produit             : {}".format(self.found_instance["produit"]) + "\n" +
                           "- Version             : {}".format(self.found_instance["version_actuelle"]))

    def __association_handle(self):
        if "message" in self.found_instance and self.found_instance["message"] == "instance not found":
            BColors.info("En attente d'association... Identifiant du noeud : " + self.secret)
            while "token" not in self.found_instance:
                sleep(5)
                self.found_instance = API.find_instance()
            BColors.success("Association effectuée avec succès")

    def __product_handle(self):
        if "server_node_c" in self.found_instance:
            self.config.id_client = self.found_instance["server_node_c"]
            self.config.code_produit = const.CODEPRODUIT[self.found_instance["produit"]]
        else:
            self.config.id_client = self.secret
            self.config.internal = True
            self.config.code_produit = prompt(
                [{'type': 'input', 'name': 'code_produit', 'message': 'Code produit'}])['code_produit']

    def __token_handle(self):
        if "token" in self.found_instance:
            self.config.teleport_token = self.found_instance["token"]
        else:
            self.config.teleport_token = prompt(
                [{'type': 'input', 'name': 'teleport_token', 'message': 'Token de télémaintenance'}])['teleport_token']

    def handle_state(self):
        self.__association_handle()
        self.__product_handle()
        self.__token_handle()
        self.config.save()
