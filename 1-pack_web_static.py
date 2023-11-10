#!/usr/bin/python3
from fabric.api import local
from time import strftime

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
        filename = "web_static_{}.tgz".format(strftime("%Y%m%d%H%M%S"))

        # Create the .tgz archive
        local("tar -czvf versions/{} web_static/".format(filename))

        return "versions/{}".format(filename)

    except Exception as e:
        print("Error: {}".format(e))
        return None

