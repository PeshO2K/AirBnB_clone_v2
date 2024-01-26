#!/usr/bin/python3
"""
Fabric script for distributing an archive to web servers
"""

from fabric.api import env, run, put
from os.path import exists
from datetime import datetime

env.hosts = ['18.204.14.158', '54.82.197.53']


# def do_deploy(archive_path):
#     """
#     Distributes an archive to web servers
#     """
#     if not exists(archive_path):
#         return False

#     try:
#         # Upload the archive to the /tmp/ directory of the web server
#         put(archive_path, "/tmp/")

#         # Extract the archive to the folder /data/web_static/releases/<archive
#         # filename without extension>
#         archive_filename = archive_path.split("/")[-1]
#         folder_name = archive_filename.split(".")[0]
#         run("mkdir -p /data/web_static/releases/{}".format(folder_name))
#         run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
#             .format(archive_filename, folder_name))

#         # Delete the archive from the web server
#         run("rm /tmp/{}".format(archive_filename))

#         # Delete the symbolic link /data/web_static/current from the web server
#         run("rm -rf /data/web_static/current")

#         # Create a new symbolic link /data/web_static/current linked to
#         # the new version of the code
#         run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
#             .format(folder_name))
#         return True
#     except Exception as e:
#         return False


# env.hosts = [
#     '3.85.54.241',
#     '52.86.86.171'
# ]


def do_deploy(archive_path):
    """distributes an archive to webservers"""
    if not os.path.exists(archive_path):
        return False

    basename = os.path.basename(archive_path)
    rem_archive_path = f"/tmp/{basename}"

    try:
        put(archive_path, rem_archive_path)
        x_archive = "/data/web_static/releases/{}".format(
            os.path.splitext(basename)[0]
        )
        run(f"mkdir -p {x_archive}")
        run("tar -xzf {} -C {} --strip-components=1".format(
            rem_archive_path, x_archive
        ))
        run(f"rm -f {rem_archive_path}")
        symlink = "/data/web_static/current"
        run(f"rm -rf {symlink}")
        run(f"ln -s {x_archive}/ {symlink}")
    except Exception:
        return False
    return True
