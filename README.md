# pyXuSB
<img src="https://img.shields.io/badge/-Linux-black?style=for-the-badge&logo=Linux&logoColor=white"> <img src="https://img.shields.io/badge/-Python-black?style=for-the-badge&logo=python&logoColor=white">

- [x] Usage: ```sudo python3 pyXuSB.py```

# Screenshot
![Screen](.animations/Screenshot.png)

# Usage
![animation](.animations/usb.gif)

# Updates
<b>14/12/2020</b>
- [x] Added Windows pendrive creating option!! Now you can create Windows pendrives easily. ;)
- [x] UI is a little bit changed.

# Setup
<b>Necessary python modules</b>
- ```npyscreen``` => <i>Creating TUI.</i>
- ```psutil``` => <i>Handling processes such as dd and mkfs.</i>

<b>Installation of python modules</b>: ```sudo pip3 install -r requirements.txt```<br>
<b>Gathering other dependencies</b>:
- ```gettext```: ```sudo apt-get install gettext```
- ```ms-sys```: ```http://ms-sys.sourceforge.net/```

<b>MS-SYS Installation</b>:
- ```tar -zxvf ms-sys*.tgz```
- ```cd ms-sys```
- ```make```
- ```sudo make install```
