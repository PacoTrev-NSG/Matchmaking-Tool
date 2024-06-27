# Matchmaking Tool

## Overall Description
This code comprises a custom Odoo Module that helps SME find optimal solutions based on a developed matchmaking framework.
It allows to register suppliers, users (SMEs), digital solutions and perform searches on these solutions based on a set of preferences and functionalities defined by the user.

## Functionalities
* **Register of SMEs with skills and preferences**
* **Register of prospective solutions with functionalities and required skills**
* **Configuration of tags and skills in platform**
* **Creation and customization of searches**
* **Leverage Odoo functionalities to manage user access**

## Installation

### Odoo Requirements
The custom module is designed for Odoo v14.0. The module doesn't depend on other modules on Odoo.

### AWS Setup
On AWS, launch an EC2 instance based on Amazon Machine Image Ubuntu Server 22.04 LTS or Ubuntu Server 24.04 LTS.

Once the instance is running, connect to the instance and perform the folllowing commands:
```
sudo su
apt update && sudo apt upgrade -y
```
To run Odoo, it is needed to install PostgreSQL
```
apt install postgresql -y
```
Also, it is needed to install wkhtmltopdf.
```
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
apt install /home/user/wkhtmltox_0.12.6-1.focal_amd64.deb
```

### Odoo Install on AWS
To install Odoo, download the official Ubuntu / Debian repository root.
```
wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
echo "deb http://nightly.odoo.com/14.0/nightly/deb/ ./" >> /etc/apt/sources.list.d/odoo.list
apt-get update && apt-get install odoo
```
### Odoo Setup
Once the installation is done, open the public IPv4 address with port 8069. Example: 18.117.21.224:8069. It will open a page to set the master password which will allow database management. The mail and password set up will be the ones to be used for platform login.

## Module Setup
To upload the Matchmaking Tool Module, it is needed to modify the odoo.conf file which is usually located in /etc/odoo/odoo.conf.
But before, create a folder on /usr/lib/python3/dist-packages/odoo/[Your folder name] where all custom modules can be stored.
Then add that path in odoo.conf in addons_path separated by ','. (Don't delete existing paths, just add)
```
Example: addons_path /usr/lib/python3/dist-packages/odoo/addons, /usr/lib/python3/dist-packages/odoo/[Your folder name]
```
Finally, add this module folder to your newly created folder. 

## Module Install
After doing the setup, restart Odoo to load the new module. 
```
sudo service odoo stop
sudo service odoo start
```
Then go to the 'Settings' menu, click on 'Activate developer mode' on said menu. 
Being on developer mode, enter 'Application' menu. On the submenus, click 'Update Apps List' to ensure that the custom module appears on the lists.
Finally, search on the app list for the custom module and click on install.

## User Manual
For more information on use refer to the User_Manual.pptx file found in this repository under the doc folder.
