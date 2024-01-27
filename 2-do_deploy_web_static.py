#!/usr/bin/python3
"""
Fabric script for distributing an archive to web servers
"""

from fabric.api import env, run, put
import os

env.hosts = ['18.204.14.158', '54.82.197.53']

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
