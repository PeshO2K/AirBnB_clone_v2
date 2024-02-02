#!/usr/bin/python3
""" Fabric script for creating archive from github repos"""

from fabric.api import local
from datetime import datetime
import os


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
    print("web_static packed: {} -> {}Bytes".format(archive_path_name, os.path.getsize(archive_path_name)))
    return archive_path_name
