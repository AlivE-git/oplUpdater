# oplUpdater

A small script to quickly update OPL for Playstation 2.

Before launch, you need to start the FTP server in uLE.

The following additional packages are required:
```
pip install requests py7zr
``` 

> The ".exe" version of the script containing all the necessary packages is available in the releases.

```
usage: oplUpdate.py [-h] [-i IP] [-o OPLPATH] [-p PAUSE] [-v]

OPL updater

optional arguments:
  -h, --help            show this help message and exit
  -i IP, --ip IP        conlose IP (example: 192.168.31.50)
  -o OPLPATH, --opl OPLPATH
                        OPL path (example: hdd/0/__system/apps/OPL)
  -p PAUSE, --pause PAUSE
                        pause a script after it finishes (default: y)
  -v, --version         show program's version number and exit
```