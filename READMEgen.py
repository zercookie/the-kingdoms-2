import tomllib
import os

def listFilesInDir(directory):
    try:
        items = os.listdir(directory)
        files = [f for f in items if os.path.isfile(os.path.join(directory,f))]
        return files
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return []

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
                                    result["client"] = "✅"
                                    result["server"] = "❌"
                                case "server":
                                    result["client"] = "❌"
                                    result["server"] = "✅"
                                case "both":
                                    result["client"] = "✅"
                                    result["server"] = "✅"
                        else:
                            result[key] = data[key]

                    else:
                        for sub in sub_keys:
                            if sub in data[key]:
                                result[sub] = data[key][sub]
                else:
                    for sub in sub_keys:
                        result[sub] = "❌"
            print(result)

except FileNotFoundError as e:
    print("Error: File not found: ", e)
except tomllib.TOMLDecodeError as e:
    print("Error: Failed to parse TOML file: ", e)



# | Name | Server | Client | Optional | Default | Description |
# |------|--------|--------|----------|---------|-------------|
#
#
#
#
#
