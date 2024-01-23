#!/usr/bin/env bash
# Bash script to setup webservers for
# deployment of web static

# function to install packages if they don't exist
install_if_not_exist() {
  if dpkg -s "$1" &>/dev/null; then
    PKG_EXIST=$(dpkg -s "$1" | grep "install ok installed")
    if [[ -n "$PKG_EXIST" ]]; then
      return
    fi
  fi
  apt-get install -y "$1"
}

# Update package information
apt-get update -y

# Install Nginx if not already installed
install_if_not_exist nginx

# Start Nginx service
service nginx start
# create necessary folders
mkdir -p /data/web_static/releases/test/ /data/web_static/shared/

# Create the directory '/var/www/html/' if it doesn't exist
mkdir -p /var/www/html/

# Create a file named 'index.html' with the content 'Hello World!'
echo 'Hello World!' > /var/www/html/index.html

# Create the custom 404 page
echo "Ceci n'est pas une page" > /var/www/html/custom_404.html

# create fake html for testing
echo "
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change owner and group recursively to ubuntu
chown -hR ubuntu:ubuntu /data/

# Create a redirection, a page that returns 'Hello World!', and a custom 404 page
echo "server {
    listen 80;
	listen [::]:80;
    server_name _;

    add_header X-Served-By \$hostname;

	root /var/www/html;
    index index.html index.htm;

    location = /hbnb_static/ {
        alias data/web_static/current/;
    }

    error_page 404 /custom_404.html;
    location  = /custom_404.html {
        root /var/www/html;
        internal;
    }
    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

}" > /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart

# Exit successfully
exit 0
