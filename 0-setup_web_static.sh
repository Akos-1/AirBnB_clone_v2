#!/usr/bin/env bash
# Bash script for setting up web servers for the deployment of web_static

# Update package information
sudo apt-get update

# Install Nginx
sudo apt-get -y install nginx

# Allow Nginx through the firewall
sudo ufw allow 'Nginx HTTP'

# Create directory structure
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create index.html with a simple message
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link to the 'current' release
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# Set ownership to the user 'ubuntu'
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to include the static files
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

# Restart Nginx for changes to take effect
sudo service nginx restart
