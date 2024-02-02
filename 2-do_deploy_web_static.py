#!/usr/bin/python3
"""
Fabric script for distributing an archive to web servers
"""

from fabric.api import *
from os import path
from datetime import datetime
# import os

env.user = "ubuntu"
env.key_filename = "~/.ssh/my_school"
env.hosts = ['18.204.14.158', '54.82.197.53']


def do_pack():
    """Creates a .tgz archive from the contents of the web_static folder.
    """
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions", capture=True)
    # Generate timestamp for the archive name
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # Create the archive file name
    archive_path_name = f"versions/web_static_{timestamp}.tgz"
    print(f"Packing web_static to {archive_path_name}")
    # Compress the web_static folder into the archive
    exit_code = local(f"tar -cvzf {archive_path_name} web_static")
    if exit_code.failed:
        return None
    print("web_static packed: {} -> {}Bytes".format(
        archive_path_name, path.getsize(archive_path_name)))
    return archive_path_name


def do_deploy(archive_path):
    """Distributes an archive to the web servers
    """
    if not path.exists(archive_path):
        return False
    try:
        # Upload archive to /tmp
        put(archive_path, '/tmp/')
        # uncompress to /data/web_static/releases/archive_folder
        archive_filename = path.basename(archive_path)
        archive_folder = path.splitext(archive_filename)[0]
        file_path = f"/tmp/{archive_filename}"
        folder_path = f"/data/web_static/releases/{archive_folder}"
        # # create folder
        run(f"mkdir -p {folder_path}")
        # # extract to folder
        run(f"tar -xzf {file_path} -C {folder_path}")
        # # remove temporary file
        run(f"rm -rf {file_path}")
        run(f"mv {folder_path}/web_static/* {folder_path}/")
        run(f"rm -rf {folder_path}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {folder_path}/ /data/web_static/current")
        print("New version deployed!")

        return True
    except Exception:
        return False
