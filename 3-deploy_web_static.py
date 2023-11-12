#!/usr/bin/python3
from fabric.api import env, task
from os.path import exists

# Set the user and hosts using Fabric environment variables
env.user = 'ubuntu'
env.hosts = ['52.91.157.33', '3.85.148.37']


def deploy():
    """
    Creates and distributes an archive to the web servers
    """

    # Call the do_pack function and store the path of the created archive
    archive_path = do_pack()

    # Return False if no archive has been created
    if not archive_path:
        return False

    # Call the do_deploy function using the new path of the new archive
    return do_deploy(archive_path)


def do_pack():
    """
    A Fabric script that generates a .tgz archive from
    the contents of the web_static folder
    folder of my AirBnB Clone repo
    """

    try:
        # Create the 'versions' directory if it doesn't exist
        local("mkdir -p versions")

        # Generate filename based on the current date and time
        filename = "web_static_{}.tgz".format(datetime.now().strftime("%Y%m%d%H%M%S"))

        # Create the .tgz archive
        local("tar -czvf versions/{} web_static/".format(filename))

        return "versions/{}".format(filename) if exists("versions/{}".format(filename)) else None

    except Exception as e:
        print("Error: {}".format(e))
        return None

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
