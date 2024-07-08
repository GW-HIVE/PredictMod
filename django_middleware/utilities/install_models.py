from ui.models import ReleasedModel, PendingModel

import json
import os
import time
import tomli


with open("./utilities/released_models.toml", "rb") as fp:
    released_configs = tomli.load(fp)

with open("./utilities/pending_models.toml", "rb") as fp:
    pending_configs = tomli.load(fp)

DRY_RUN = False
BCO_DIR = os.path.abspath("../flask_backend/models")

print(f"Examining file {BCO_DIR}")


def handle_BCO(bco_path):
    with open(os.path.join(BCO_DIR, bco_path), "r") as fp:
        bco = json.load(fp)
    fp.close()
    print(f"===> Got info: {bco['provenance_domain']}\n{type(bco)}")
    formatted_info = {
        "name": bco["provenance_domain"]["name"],
        "version": bco["provenance_domain"]["version"],
        # "release_date": time.strptime(
        #     bco["provenance_domain"]["modified"], "%Y-%m-%dT%H:%M:%S"
        # ),
        "release_date": bco["provenance_domain"]["modified"].split("T")[0],
    }
    return formatted_info


for k, v in released_configs.items():
    if "BCO" in v.keys():
        print(f"{k}: Procssing BCO {v['BCO']}")
        bco_info = handle_BCO(v["BCO"])
        print(f"===Got info: {bco_info}")
        v.pop("BCO")
        # Requires python 3.9+
        v = v | bco_info
        print(f"{v}")
    if DRY_RUN:
        continue
    link = "{}".format(v["name"].replace(" ", "-"))
    ReleasedModel.objects.create(
        name=v["name"],
        version=v["version"],
        release_date=v["release_date"],
        data_type=v["data_type"],
        model_type=v["model_type"],
        data_meta=v["data_meta"],
        backend=v["backend"],
        link=link,
    )

for k, v in pending_configs.items():
    print(f"Creating Model ---> {k}")
    if DRY_RUN:
        continue
    link = "{}-anticipated".format(v["name"].replace(" ", "-"))
    PendingModel.objects.create(
        name=v["name"], version=v["version"], data_type=v["data_type"], link=link
    )
