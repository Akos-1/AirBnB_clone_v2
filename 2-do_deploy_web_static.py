#!/usr/bin/python3
"""
a Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers
using the function do_deploy
"""

from fabric.api import *
from os import path

# Define the web server IPs and username for Fabric
env.hosts = ['52.91.157.33', '3.85.148.37']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    Sharesthe compressed web static package to web servers.

    :param archive_path: Path to the compressed archive on the local machine.
    :return: True if deployment is successful or False otherwise.
    """

    try:
        # Check if the archive file exists
        if not path.exists(archive_path):
            print(f"Error: Archive not found at {archive_path}")
            return False

        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract filename without extension to use as timestamp
        timestamp = path.basename(archive_path).split('.')[0]

        # Define target directory for deployment
        target_dir = '/data/web_static/releases/web_static_{}/'.format(timestamp)

        # Create target directory for deployment
        run('sudo mkdir -p {}'.format(target_dir))

        # Uncompress the archive to the target directory
        run('sudo tar -xzf /tmp/{}.tgz -C {}'.format(timestamp, target_dir))

        # Remove the uploaded archive
        run('sudo rm /tmp/{}.tgz'.format(timestamp))

        # Move contents into the target directory
        run('sudo mv {}/web_static/* {}'.format(target_dir, target_dir))

        # Remove the extraneous web_static directory
        run('sudo rm -rf {}/web_static'.format(target_dir))

        # Delete pre-existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('sudo ln -s {} /data/web_static/current'.format(target_dir))

        # Return True on success
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
