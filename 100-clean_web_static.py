#!/usr/bin/python3
"""
Fabric script for distributing an archive to web servers
and clean up
"""

from fabric.api import *
import os
from datetime import datetime
# import os

env.user = "ubuntu"
env.key_filename = "~/.ssh/my_school"
env.hosts = ['18.204.14.158', '54.82.197.53']


def do_clean(number=0):
    """Delete out-of-date archives.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
