import wget
import json
import py7zr
import winreg
import sys
import os.path
import shutil

def printError(text):
    print("ERROR: {}".format(text))
    sys.exit()

def readACF(acfFile):
     with open(acfFile) as f: 
            for line in f: 
                if "installdir" in line:
                    return("\\steamapps\\common\\{}".format(line.split("\"")[3]))
    
    
def getGamePath(steamAppId): 
    print("Try to get game path")
    gameDir = None
    #read the steam instalation path from registry
    try:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
    except:
        hkey = None 
        printError("Can't find HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam")
    try:
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")
    except:
        steam_path = None
        printError("Can't find value InstallPath in HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam")
    winreg.CloseKey(hkey) 

    if  os.path.isfile(steam_path[0]+"\\steamapps\\appmanifest_{}.acf".format(steamAppId)):   
            
        gameDir = steam_path[0] + readACF(steam_path[0]+"\\steamapps\\appmanifest_{}.acf".format(steamAppId))
    
    else: #check if the game is installed in a secondary game lib
        with open(steam_path[0]+"\\steamapps\\libraryfolders.vdf") as f: 
            for line in f: 
                elements = line.split("\"")
                if len(elements) == 5:
                    path = line.split("\"")[3]
                    if os.path.isdir(path):
                        path = path.replace("\\\\","\\")
                        if  os.path.isfile(path+"\\steamapps\\appmanifest_{}.acf".format(steamAppId)):
                            gameDir = path + readACF(path+"\\steamapps\\appmanifest_{}.acf".format(steamAppId))
                            break  
                    else:
                        continue
    print("Game path found:\n{}".format(gameDir))
    return(gameDir)

def downloadModArchive(url):
    print("Try to download the modPack archive")

    filename = os.path.basename(url)
    if os.path.exists(filename):
        os.remove(filename)
    try:
        wget.download(url, './')
    except:
        printError("Download failed")
    print("\nFile downloaded: {}".format(filename))
    
def extractArchive(filename):
    print("Extract the downloaded mod-pack")
    try:
        archive = py7zr.SevenZipFile(filename, mode='r')
        archive.extractall(path="./tmp")
        archive.close()
        os.remove(filename)
        print("Extraction completed")
    except:
        printError("Can't extract the archive")        
    
def copyFiles(dest):
    print("Copy files to the game directory")
    try:
        shutil.copytree("./tmp", dest, dirs_exist_ok=True)
        shutil.rmtree('./tmp')
    except:
        printError("Copy failed")
    print("Done")

def main():
    modURL = None
    steamappID = None
    gamePath = None
    try:
        with open("config.json") as f:
            data = json.load(f)
    except:
        printError("Can't read the config file")
    
    steamappID = data["steamappID"]
    modURL = data["modURL"]   

    gamePath = (getGamePath(steamappID))

    downloadModArchive(modURL)

    extractArchive(os.path.basename(modURL))
    copyFiles(gamePath)


if __name__ == '__main__':
    main()