#!/bin/bash

#: Sets up the fax machine on Rapsbian
#:
#: PRECONDITION: dependencies in requirements.txt have been installed
#:
#: Author: Fastily

if [ "$#" -ne 1 ]; then
	printf "Usage: setupForTheLazy.sh <SERVER_HOSTNAME_OR_IP>\n"
	exit 1
fi

sudo apt install update && sudo apt install -y nginx ufw

cd "${0%/*}" &> /dev/null

# setup gunicorn
sudo cp gunicorn.service gunicorn.socket /etc/systemd/system/
sudo systemctl start gunicorn && sudo systemctl enable gunicorn && systemctl status gunicorn

# nginx config
faxMachineConf="/etc/nginx/sites-available/faxmachine"
printf "$(<nginxconfig.txt)" "$1" | sudo tee "$faxMachineConf" > /dev/null
sudo ln -s "$faxMachineConf" /etc/nginx/sites-enabled
sudo nginx -t && sudo systemctl restart nginx

# firewall settings
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'