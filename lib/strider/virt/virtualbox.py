# Copyright 2015 Gerard Cristofol <gcristofol/gmail>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Import the vboxapi package
from vboxapi import VirtualBoxManager

import socket
import time
from strider.common.instance_data import InstanceData, SshData
import strider.common.logger

class VBOX(object):

    def __init__(self, name=None, instance_type=None, virtualbox_manager=None, tags=None):

        self.name = name
        self.instance_type = instance_type
        self.tags = {}
        self.virtualbox_manager = virtualbox_manager

        # utility instances
        self.log = strider.utils.logger.get_logger('VBOX')

        # check for required args
        if not self.name:
            raise Exception("'name' is required")
        if not self.instance_type:
            raise Exception("'instance_type' is required")

        # coerce inputs
        self.tags['Name'] = self.name


    # --------------------------------------------------------------------------
    # PUBLIC VIRT API INTERFACE
    # --------------------------------------------------------------------------

    def up(self):
        """ Instantiate instances if needed, otherwise just start them """

        self.log("determining if we need to create an instance")
        me = self.describe().provider_specific
        if me is None:
            self.log("creating an instance")
            
            #TODO Create the virtualbox instance
            # 2. Get the IVirtualBox object
            virtualbox = self.virtualbox_manager.getVirtualBox()
            virtualbox.createInstance() #parameter home???
            
            self.log("instance created")
        else:
            self.log("instance already exists, starting if needed")
            self.connection.start_instances([me.id])

        me = self.describe()
        if not me.present:
            raise Exception("unexpectedly can't find the instance.")

    # --------------------------------------------------------------------------

    def destroy(self):
        """ Destroy the described instance """

        self.log("looking for instances to destroy")
        me = self.describe()
        if me.present:
            self.log("destroying instance")
            self.connection.terminate_instances(instance_ids=[me.provider_specific.id])
            self.log("instance destroyed")
        else:
            self.log("no instance found to destroy")
          
    # --------------------------------------------------------------------------            
            
    def describe(self):
        """ Return details about the instance.  Standardized between cloud providers """

        details = self._details()
        if details is None:
            return InstanceData(present=False)

    # --------------------------------------------------------------------------
    # PRIVATE FUNCTIONS
    # --------------------------------------------------------------------------


    def _details(self):
        """ Return the cloud provider's info about the described instance"""

        # 2. Get the IVirtualBox object
        virtualbox = self.virtualbox_manager.getVirtualBox()
        
        # For IVirtualBox array attributes you need to use 
        # the VirtualBoxManager.getArray() method:

        # Iterate the IVirtualBox::machines array.
        # Each element is an IMachine instance.
        machines = self.virtualbox_manager.getArray(virtualbox, 'machines')
        for machine in machines:
            print 'Virtual machine, name: ', machine.name 
            if machine.name is self.name:
                return machine
            
        return None

  
