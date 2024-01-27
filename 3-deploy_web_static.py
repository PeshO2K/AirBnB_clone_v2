#!/usr/bin/python3
"""
Fabric script for distributing an archive to web servers
"""

from fabric.api import env, run, put, local
from os import path
from datetime import datetime

env.user = "ubuntu"
env.key_filename = "~/.ssh/my_school"
env.hosts = ['18.204.14.158', '54.82.197.53']


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


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
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
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """stack and deploy"""
    archive_filepath = do_pack()
    if not archive_filepath:
        return False
    return (do_deploy(archive_filepath))

# def deploy():
#     do_pack_path = "1-pack_web_static.py"
#     do_deploy = "2-do_deploy_web_static.py"
#     archive_path = run(f"fab -f {do_pack_path} do_pack")
#     if archive_path == None:
#         return False

#     return run(f"fab -f {do_deploy} do_deploy:archive_path={archive_path}\
#                 -i ~/.ssh/school -u ubuntu")
