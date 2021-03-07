# Valheim ModSync
ModSync is a simple Python script for downloading a (BepInEx) ModPack wich you offer and copy the files to the game directory.

With this script the players dont have to search all mod updates manually, only the Hoster have to provide a ready to use ModPack.

## Usage

Adjust the "URL_TO_MODPACK" in the config file to your ModPack.

NOTE: The archive have to be a .7z archive. 
```json
{
    "modURL": "URL_TO_MODPACK", 
    "steamappID": "892970"
}
```

Execute the modSync.exe 

## Dependencies to run in python

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

#### wget

```bash
pip install wget
```
#### py7zr

```bash
pip install py7zr
```

#### cx_freeze (optional)

```bash
pip install cx_freeze
```

## Contributing
Pull requests are welcome.
