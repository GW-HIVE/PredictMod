from ui.models import ReleasedModel, PendingModel

import tomli

with open("./utilities/released_models.toml", "rb") as fp:
    released_configs = tomli.load(fp)

with open("./utilities/pending_models.toml", "rb") as fp:
    pending_configs = tomli.load(fp)

for k, v in released_configs.items():
    print(f"Creating Model ---> {k}")
    ReleasedModel.objects.create(
        name=v["name"],
        version=v["version"],
        release_date=v["release_date"],
        data_type=v["data_type"],
        model_type=v["model_type"],
        data_meta=v["data_meta"],
        backend=v["backend"],
    )

for k, v in pending_configs.items():
    print(f"Creating Model ---> {k}")
    PendingModel.objects.create(
        name=v["name"],
        version=v["version"],
        data_type=v["data_type"],
    )
