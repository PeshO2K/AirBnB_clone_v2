#!/usr/bin/python3
"""
Fabric script for distributing an archive to web servers
"""

from fabric.api import env, run, put
from os import path

env.hosts = ['18.204.14.158', '54.82.197.53']

def do_deploy(archive_path):
    """
    Distributes an archive to web servers

    Args:
        archive_path (str): Path to the archive file

    Returns:
        True if all operations have been done correctly, otherwise returns False
    """
    # Check if the archive file exists
    if not path.exists(archive_path):
        return False

    # Extract information from the archive path
    archive_filename = path.basename(archive_path)
    folder_name = path.splitext(archive_filename)[0]
    remote_archive_path = f"/tmp/{archive_filename}"

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Define the target extraction directory on the web server
        target_extraction_path = f"/data/web_static/releases/{folder_name}"

        # Create the target directory on the web server
        run("mkdir -p {}".format(target_extraction_path))

        # Extract the archive, stripping the top-level directory
        run("tar -xzf {} -C {} --strip-components=1"
            .format(remote_archive_path, target_extraction_path))

        # Delete the uploaded archive from the web server
        run("rm -f {}".format(remote_archive_path))

        # Remove the previous symbolic link
        symlink = "/data/web_static/current"
        run(f"rm -rf {symlink}")

        # Create a new symbolic link linked to the extracted version
        run("ln -s {}/ {}"
            .format(target_extraction_path, symlink))

        return True

    except Exception as e:
        print(e)
        return False
