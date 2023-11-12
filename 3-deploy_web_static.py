#!/usr/bin/python3
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

# Set the user and hosts using Fabric environment variables
env.user = 'ubuntu'
env.hosts = ['52.91.157.33', '3.85.148.37']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """

    # Create the folder if it doesn't exist
    local("mkdir -p versions")

    # Generate the file name with the current timestamp
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "web_static_{}.tgz".format(now)

    # Compress the contents of web_static into the archive
    result = local("tar -cvzf versions/{} web_static".format(file_name), capture=True)

    # Return the path to the created archive if successful, otherwise return None
    return "versions/{}".format(file_name) if exists("versions/{}".format(file_name)) and result.succeeded else None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """

    # Check if the file at archive_path exists
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Get the filename without extension
        filename = archive_path.split('/')[-1].split('.')[0]

        # Create the releases folder if it doesn't exist
        run("mkdir -p /data/web_static/releases/{}".format(filename))

        # Uncompress the archive to /data/web_static/releases/<filename> on the web server
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(filename + '.tgz', filename))

        # Remove the archive from the web server
        run("rm /tmp/{}".format(filename + '.tgz'))

        # Move contents to the current version
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(filename, filename))

        # Remove the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link linked to the new version
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(filename))

        print("New version deployed!")

        return True

    except Exception as e:
        print("Error: {}".format(e))
        return False


def deploy():
    """
    Creates and distributes an archive to the web servers
    """

    # Call do_pack and store the path of the created archive
    archive_path = do_pack()

    # Return False if no archive has been created
    if not archive_path:
        return False

    # Call do_deploy using the new path of the new archive
    return do_deploy(archive_path)
