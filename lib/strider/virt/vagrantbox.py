import vagrant
import os
from subprocess import CalledProcessError
from strider.common.instance_data import InstanceData, SshData
import strider.common.logger


class Vagrantbox(object):
    def __init__(self,
                 name=None,
                 ssh=None,
                 basebox=None,
                 bake_name=None,
                 bake_description=None,
                 user_data=None):
        self.name = name
        self.bake_name = bake_name
        self.basebox = basebox
        self.ssh = ssh
        self.log = strider.utils.logger.get_logger('Vagrant')
        if type(self.ssh) != dict:
            raise Exception("expecting 'ssh' to be a dictionary")

        self.vagrant_instance = vagrant.Vagrant()

    def describe(self):
        details = self._details()
        if details is None:
            return InstanceData(present=False)
        else:
            if self.ssh['username'] is not None:
                username = self.ssh['username']
            else:
                username = "vagrant"

            if self.ssh['private_key_path'] is not None:
                private_key_path = self.ssh['private_key_path']
            else:
                private_key_path = details['IdentityFile']

            port = details['Port']
            host = details['HostName']
            ssh_data = SshData(keyfile=private_key_path,
                               user=username,
                               host=host,
                               port=port)
        return InstanceData(present=True,
                            provider_specific=details,
                            ssh=ssh_data)

    def destroy(self):
        self.log("destroying instance")
        try:
            self.vagrant_instance.destroy()
        except CalledProcessError:
            self.log("already destroyed instance")
        try:
            os.remove("./Vagrantfile")
        except OSError:
            self.log("already removed Vagrantfile")

    def up(self):
        self.log("determining if we need to create an instance")
        try:
            self.vagrant_instance.init(box_name=self.basebox)
        except CalledProcessError:
            self.log("already initialised instance")
        try:
            self.log("bring up instance")
            self.vagrant_instance.up()
        except CalledProcessError:
            self.log("already up")

    def _details(self):
        try:
            conf = self.vagrant_instance.conf()
            return conf
        except CalledProcessError:
            self.log("No instance running")
        return None

    def bake(self):
        self.log("baking vagrant box")
        os.system("vagrant package --output {}.box".format(self.bake_name))
        self.up()
