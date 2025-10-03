import tomllib
import os

modList = []
CHECK = "✅"
CROSS = "❌"


def listFilesInDir(directory):
    try:
        items = os.listdir(directory)
        files = [f for f in items if os.path.isfile(os.path.join(directory,f))]
        return files
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return []

def getModListInfoFromTOMLfiles():
    try:
        mods = listFilesInDir("mods/")
        for mod in mods:
            with open(f"mods/{mod}","rb") as file:
                data = tomllib.load(file)

                main_keys = ["name","side","option"]
                sub_keys = ["optional","default","description"]
                result = {}

                for key in main_keys:
                    if key in data:
                        if type(data[key]) == str:
                            if key == "side":
                                match data[key]:
                                    case "client":
                                        result["client"] = CHECK
                                        result["server"] = CROSS
                                    case "server":
                                        result["client"] = CROSS
                                        result["server"] = CHECK
                                    case "both":
                                        result["client"] = CHECK
                                        result["server"] = CHECK
                            else:
                                result[key] = data[key]
                        else:
                            for sub in sub_keys:
                                if sub in data[key]:
                                    match data[key][sub]:
                                        case True:
                                            result[sub] = result[sub] = CHECK
                                        case False:
                                            result[sub] = result[sub] = CROSS
                                        case _:
                                            result[sub] = data[key][sub]
                    else:
                        for sub in sub_keys:
                            result[sub] = CROSS
                modList.append(result)
    except FileNotFoundError as e:
        print("Error: File not found: ", e)
    except tomllib.TOMLDecodeError as e:
        print("Error: Failed to parse TOML file: ", e)

def generateMODStable(modList):
    README = "# Mods\n\n"
    README += "| Name | Client | Server | Optional | Enabled by Default | Description |\n"
    README += "|------|:--------:|:--------:|:----------:|:---------:|-------------|\n"
    for mod in modList:
        README += f"|{mod["name"]}|{mod["client"]}|{mod["server"]}|{mod["optional"]}|{mod["default"]}|{mod["description"]}|\n"
    return(README)

getModListInfoFromTOMLfiles()

with open("README.md", "w", encoding="utf-8") as file:
    file.write("")
    
    file.write(generateMODStable(modList))