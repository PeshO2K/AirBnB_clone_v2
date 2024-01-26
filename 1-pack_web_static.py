#!/usr/bin/python3
""" Fabric script for creating archive from github repos"""
from fabric.api import local
from datetime import datetime
import os


# def do_pack():
#     """creates a tgz archive from the current folder"""
#     local("mkdir -p versions")
#     out_name = f"web_static_{datetime.now().strftime('%Y%m%d%H%M%S')}.tgz"
#     result = local("tar -cvzf versions/{} web_static".format(out_name),
#                    capture=True)
#     if not result.return_code:
#         return f"versions/{out_name}"
#     return None

def do_pack():
    """Creates a .tgz archive from the contents of the web_static folder.
    """
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Generate timestamp for the archive name
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')

    # Create the archive file name
    archive_name = f"web_static_{timestamp}.tgz"

    # Compress the web_static folder into the archive
    exit_code = local(f"tar -cvzf versions/{archive_name} web_static", capture=True)
    if exit_code.return_code:
        return None
    return os.path.join("versions", archive_name)
