#!/usr/bin/python3
""" Fabric script for creating archive from github repos"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Creates a .tgz archive from the contents of the web_static folder.
    """
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")
    # Generate timestamp for the archive name
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # Create the archive file name
    archive_path_name = f"versions/web_static_{timestamp}.tgz"
    # Compress the web_static folder into the archive
    exit_code = local(f"tar -cvzf {archive_path_name} web_static",
                      capture=True)
    if exit_code.return_code:
        return None
    return archive_path_name

    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(now)

        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_name))

        print("web_static packed: {} -> {}Bytes".format(archive_name, os.path.getsize(archive_name)))

        return archive_name
    except Exception as e:
        print(e)
        return None
