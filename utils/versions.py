import json
import os
import pathlib

current_version = "2.0.1"
path = "utils/versions_stock/"


def create_version_file(version, amount: int):
    if not os.path.exists(f"{path}{version}.json"):

        change = {"changes": []}

        for i in range(amount):
            change["changes"].append({
                "name": "Change",
                "description": "Description"
            })

        with open(f"{path}{version}.json", "w") as json_file:
            json.dump(change, json_file, indent=4)

        return f"Successfully created **{version}.json** with a amount of **{amount}** changes."

    else:
        return "This file already exists."


def changes(version):
    if os.path.exists(f"{path}{version}.json"):
        with open(f"{path}{version}.json") as json_file:
            file = json.load(json_file)
            changelist = []
            for change in file["changes"]:
                changelist.append("\n".join([f"**{change['name']}**", f"{change['description']}"]))
            return "\n\n".join(changelist)
    elif not os.path.exists(f"{path}{version}.json") and version == current_version:
        change = {"changes": []}
        change["changes"].append({
            "name": "No changes submitted.",
            "description": "Try it with another version."
        })

        with open(f"{path}{version}.json", "w") as json_file:
            json.dump(change, json_file, indent=4)
        changes(version)
    else:
        files = [file for file in [file.stem for file in pathlib.Path(path).glob('*.json')]]
        return f"Version **{version}** wasn't found.\n_All available versions:_```" + "\n".join(files) + "```"



