# -*- coding: utf-8 -*-

from ..model.config import AlloConfig
from ..const import *


class TelemUtil:
    config_file = "/etc/teleport.yaml"

    @staticmethod
    def telem_running():
        return os.path.exists("/run/teleport.pid")

    @staticmethod
    def telem_status():
        from allo.model.colors import BColors
        print("Etat de le télémaintenance : ", end="")
        if TelemUtil.telem_running():
            BColors.success("Démarrée")
        else:
            BColors.error("Stoppée")

    @staticmethod
    def telem_start():
        from allo.utils.ansible import AnsibleUtil
        TelemUtil.__init()
        AnsibleUtil.start_telem()
        TelemUtil.telem_status()

    @staticmethod
    def telem_stop():
        from allo.utils.ansible import AnsibleUtil
        TelemUtil.__init()
        AnsibleUtil.stop_telem()
        TelemUtil.telem_status()

    @staticmethod
    def __init():
        if os.path.exists(TelemUtil.config_file):
            return
        config = AlloConfig.load()
        teleport_yaml = ("teleport:",
                         '    auth_token: "{}"'.format(config.teleport_token),
                         '    ca_pin: "sha256:' + TELEPORT_SHA + '"',
                         '    auth_servers:',
                         '        - {}'.format(ALLO_URL),
                         'auth_service:',
                         '    enabled: no',
                         'proxy_service:',
                         '    enabled: no',
                         'ssh_service:',
                         '    enabled: "yes"',
                         '    labels:',
                         '        produit: {}'.format(config.code_produit),
                         '        secret: {}'.format(config.id_client),
                         '        internal: {}'.format("true" if config.internal else "false"),
                         '    commands:',
                         '    - name: diff',
                         '      command: [allo, changes]',
                         '      period: 1m0s')

        with open(TelemUtil.config_file, 'w+') as yaml_file:
            yaml_file.write('\n'.join(teleport_yaml))
