#!/usr/bin/python3
"""
A Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers
using the function do_deploy
"""

from fabric.api import *
from os import path

# Define the web server IPs and username for Fabric
env.hosts = ['52.91.157.33', '3.85.148.37']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school '


def do_deploy(archive_path):
    """
    Sharesthe compressed web static package to web servers.

    :param archive_path: Path to the compressed archive on the local machine.
    :return: True if deployment is successful or False otherwise.
    """

    try:
        # Determines if the archive file exists
        if not path.exists(archive_path):
            print(f"Error: Archive not found at {archive_path}")
            return False

        # the archive to the /tmp/ directory on the web server is uploaded
        put(archive_path, '/tmp/')

        # the filename without extension which will be use as timestamp is extracted
        timestamp = path.basename(archive_path).split('.')[0]

        # the target directory for deployment is defined
        target_dir = '/data/web_static/releases/web_static_{}/'.format(timestamp)

        # target directory for deployment is created
        run('sudo mkdir -p {}'.format(target_dir))

        # the archive to the target directory is uncompressed
        run('sudo tar -xzf /tmp/{}.tgz -C {}'.format(timestamp, target_dir))

        # the uploaded archive is removed
        run('sudo rm /tmp/{}.tgz'.format(timestamp))

        # Move contents into the target directory
        run('sudo mv {}/web_static/* {}'.format(target_dir, target_dir))

        # the extraneous web_static directory is removed
        run('sudo rm -rf {}/web_static'.format(target_dir))

        # the pre-existing symbolic link is deleted
        run('sudo rm -rf /data/web_static/current')

        # a new symbolic link is created
        run('sudo ln -s {} /data/web_static/current'.format(target_dir))

        # True is returned on success
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
