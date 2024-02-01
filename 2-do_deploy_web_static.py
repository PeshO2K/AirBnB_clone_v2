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


def do_deploy(archive_path):
    """Function distributes an archive to my web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        # Extracting directory and file information
        path_split = os.path.splitext(os.path.basename(archive_path))
        no_extension = path_split[0]
        folder = '/data/web_static/releases/{}/'.format(no_extension)

        # Upload the archive to /tmp/
        put(archive_path, '/tmp/')

        # Create the release directory
        run('mkdir -p {}'.format(folder))

        # Extract the contents of the archive into the release directory
        run('tar -xzf /tmp/{} -C {}/'.format(
            os.path.basename(archive_path), folder))

        # Remove the uploaded archive from /tmp/
        run('rm /tmp/{}'.format(os.path.basename(archive_path)))

        # Move the contents of web_static to the release directory
        run('mv {}/web_static/* {}'.format(folder, folder))

        # Remove the now empty web_static directory
        run('rm -rf {}/web_static'.format(folder))

        # Update the symbolic link to the new release
        current = '/data/web_static/current'
        run('rm -rf {}'.format(current))
        run('ln -s {}/ {}'.format(folder, current))

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
