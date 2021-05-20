import os
from io import StringIO
from ftplib import FTP
import argparse
import requests
import py7zr
import shutil

version      = "v1.0" 
gitUrlScript = "https://api.github.com/repos/AlivE-github/oplUpdater/releases/latest"
gitUrlOpl    = "https://api.github.com/repos/ps2homebrew/Open-PS2-Loader/releases/tags/latest"

def getLastVersionScript():
  response = requests.get(gitUrlScript)
  lastVer = (response.json()["name"])
  return lastVer

def getVersionOpl():
  ver = StringIO()
  ftp = FTP(args.ip)
  ftp.login()
  ftp.cwd(args.oplPath)
  try:
    ftp.retrlines("RETR " + "version.txt", ver.write)
  except:
    ver.write("none")
  ftp.quit()
  return ver.getvalue()

def getLastVersionOpl():
  response = requests.get(gitUrlOpl)
  lastVer = (response.json()["name"])
  return lastVer

def downloadOpl():
  response = requests.get(gitUrlOpl)
  lastVerUrl = (response.json()["assets"][1]["browser_download_url"])
  oplArchiveUrl = requests.get(lastVerUrl)
  if not os.path.exists("tmp"):
    os.makedirs("tmp")
  with open("tmp/opl.7z", "wb") as localFile:
    localFile.write(oplArchiveUrl.content)

def extractOpl():
  with py7zr.SevenZipFile("tmp/opl.7z", mode = "r") as archive:
    archive.extractall(path = "tmp")

def searchFile():
  for filename in os.listdir("tmp/OPNPS2LD-VARIANTS"):
    if "IGS=1" in filename and "PADEMU=1" in filename and "RTL=1" in filename and "DTL_T10000=1" not in filename:
      return filename

def versionFile(ver):
  with open("tmp/version.txt","w+") as fileVer:
    fileVer.write(ver)

def ftpUpload(oplName):
  ftp = FTP(args.ip)
  ftp.login()
  ftp.cwd(args.oplPath)
  with open("tmp/version.txt", "rb") as textFile:
    ftp.storlines("STOR " + "version.txt", textFile)
  with open("tmp/OPNPS2LD-VARIANTS/" + oplName,"rb") as oplFile:
    ftp.storbinary("STOR " + "OPNPS2LD.ELF", oplFile)
  ftp.quit()

def clean():
  shutil.rmtree("tmp")

def main():
  scriptLast = getLastVersionScript()
  if version[1:] < scriptLast[1:]:
    print("New version found! Please update:")
    print("https://github.com/AlivE-github/oplUpdater/releases")
    os.system("pause")
  else:
    cur = getVersionOpl()
    print("Installed version: ", cur)
    last = getLastVersionOpl()
    print("Last version:      ", last)
    if cur == last:
      print("Already updated.")
    else:
      print("Download...")
      downloadOpl()
      print("Extracting...")
      extractOpl()
      versionFile(last)
      file = searchFile()
      print("Updating...")
      ftpUpload(file)
      print("Removing temporary files...")
      clean()
      print("DONE!")
    if args.pause == "y":
      os.system("pause")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='OPL updater')
  parser.add_argument("-i", "--ip", dest = "ip",
                    help = "conlose IP (example: 192.168.31.50)")
  parser.add_argument("-o", "--opl", dest = "oplPath",
                    help = "OPL path (example: hdd/0/__system/apps/OPL)")
  parser.add_argument("-p", "--pause", dest = "pause",
                    help = "pause a script after it finishes (default: y)", default = "y")
  parser.add_argument("-v", "--version", action="version", version=version)
  args = parser.parse_args()
  if not args.ip or not args.oplPath:
    parser.error("ip or OPL path not specified")
  main()