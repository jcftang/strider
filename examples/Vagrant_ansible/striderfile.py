#!/usr/bin/env python
# example strider file

from strider import Strider
from strider.virt.vagrantbox import Vagrantbox
from strider.provisioners.shell import Shell
import time
import os

# ==============================================================================
# vagrant instance and builder configuration

instance = Vagrantbox(
    name                      = "%s-strider-test" % os.environ["USER"], # currently not used
    basebox                   = "wheezy", # the basebox to use
    ssh = dict(
        username              = "vagrant",# default username to login with
	private_key_path      = "/Users/jtang/.vagrant.d/insecure_private_key", # key to use
    ),
    bake_name                 = "strider-produced-basebox-%d" % int(time.time()), # output filename
    bake_description          = "Vagrant basebox description goes here version 1.00",

    # other optional parameters:
    user_data                 = open("userdata.sh").read(),
)

# ==============================================================================
# The provisioner decides how the instance will be configured

provisioner = Shell(
    commands = [

	# you can deselect 'rsync' by changing to 'copy' below for the type parameter.
	# rsync on AWS free tier has been observed to be unreliable - protocol errors
	# so if you see this, know why

        "sudo DEBIAN_FRONTEND=noninteractive apt-get update -y",
        "sudo DEBIAN_FRONTEND=noninteractive apt-get -y install rsync",
	dict(type='rsync', copy_from="./deploy", copy_to="/home/vagrant/deploy_root"),
    ]
)

# Alternative: run ansible remotely from the build machine / workstation
# (more SSH activity, but shares less information with the guest)

# provisioner = Shell(
#     commands = [
#         dict(type='command', 
#              command='PYTHONUNBUFFERED=1 ansible-playbook -v -i {{ssh_host}}, -u {{ssh_user}} -e "target={{ssh_host}}" deploy/test.yml'),
       
#     ]
# )

# optional steps to run prior to --bake commands that will only run with --bake
pre_bake = Shell(
    commands = [
        "sync"
    ]
)

# optional commands to run after successful bake jobs to use remaining compute time
post_bake = Shell(
    commands = [
        "echo 'post bake steps!'"
    ]
)

# =============================================================================
# go!

strider = Strider(provisioner=provisioner, pre_bake=pre_bake, post_bake=post_bake).cli(instance)
