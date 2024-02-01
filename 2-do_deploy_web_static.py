#!/usr/bin/python3
"""
Fabric script for distributing an archive to web servers
"""

from fabric.api import env, run, put
# from os import path
import os

env.user = "ubuntu"
env.key_filename = "~/.ssh/my_school"
env.hosts = ['18.204.14.158', '54.82.197.53']

# def do_deploy(archive_path):
#     """
#     Distributes an archive to web servers

#     Args:
#         archive_path (str): Path to the archive file

#     Returns:
#         True if all operations ha
#            ve been done correctly, otherwise returns False
#     """
#     # Check if the archive file exists
#     if not path.exists(archive_path):
#         return False

#     # Extract information from the archive path
#     archive_filename = path.basename(archive_path)
#     folder_name = path.splitext(archive_filename)[0]
#     remote_archive_path = f"/tmp/{archive_filename}"

#     try:
#         # Upload the archive to the /tmp/ directory of the web server
#         put(archive_path, '/tmp/')

#         # Define the target extraction directory on the web server
#         target_extraction_path = f"/data/web_static/releases/{folder_name}"

#         # Create the target directory on the web server
#         run("mkdir -p {}".format(target_extraction_path))

#         # Extract the archive, stripping the top-level directory
#         run("tar -xzf {} -C {} --strip-components=1"
#             .format(remote_archive_path, target_extraction_path))

#         # Delete the uploaded archive from the web server
#         run("rm -f {}".format(remote_archive_path))

#         # Remove the previous symbolic link
#         symlink = "/data/web_static/current"
#         run(f"rm -rf {symlink}")

#         # Create a new symbolic link linked to the extracted version
#         run("ln -s {}/ {}"
#             .format(target_extraction_path, symlink))

#         return True

#     except Exception as e:
#         print(e)
#         return False


def do_deploy(archive_path):
    """
    distributes an archive to your web servers
    """
    # verificamos si el path existe
    if os.path.exists(archive_path) is False:
        return(False)
    try:
        put(archive_path, '/tmp/')
        _filename = archive_path.split("/")[-1]
        filename = _filename.split(".")[0]
        run('mkdir -p /data/web_static/releases/{}'.format(filename))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format
            (_filename, filename))
        run('rm /tmp/{}'.format(_filename))
        run('mv -u /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(filename, filename))
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(filename))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{} /data/web_static/current'
            .format(filename))
        return(True)
    except Exception:
        return(False)
