import json
import os
import time
import tomli

IN_DJANGO = bool(os.environ.get("DJANGO_SETTINGS_MODULE", False))

if IN_DJANGO:
    from ui.models import (
        ReleasedModel,
        PendingModel,
        Condition,
        Intervention,
        InputDataType,
    )

    with open("./scripts/released_models.toml", "rb") as fp:
        released_configs = tomli.load(fp)

    with open("./scripts/pending_models.toml", "rb") as fp:
        pending_configs = tomli.load(fp)
    BCO_DIR = os.path.abspath("../flask_backend/models")
    MODELS_DIR = os.path.abspath("../flask_backend/models")
else:
    with open("./released_models.toml", "rb") as fp:
        released_configs = tomli.load(fp)
    with open("./pending_models.toml", "rb") as fp:
        pending_configs = tomli.load(fp)
    BCO_DIR = os.path.abspath("../../flask_backend/models")
    MODELS_DIR = os.path.abspath("../../flask_backend/models")


def handle_BCO(bco: dict):
    formatted_info = {
        "name": bco["provenance_domain"]["name"],
        "version": bco["provenance_domain"]["version"],
        "release_date": bco["provenance_domain"]["modified"].split("T")[0],
    }
    return formatted_info


def find_models(model_definition_string, parent_dir):
    target_definitions = []
    for parent, dirnames, filenames in os.walk(parent_dir):
        if model_definition_string in filenames:
            target_definitions.append(os.path.join(parent, model_definition_string))
    return target_definitions


# Ingest self-defined model information (new method)
print(f"====\tCreating MODELS\t====")
model_definitions = find_models("model.toml", MODELS_DIR)
for model in model_definitions:
    print(f"===> Using model definition from {model}")
    with open(model, "rb") as fp:
        config = tomli.load(fp)
    # Get BCO information
    model_root = os.path.dirname(model)
    # Carve-out for the automated pipeline
    # Provide a non-"model" representation of that tool
    if "automated" in model_root:
        continue
    with open(os.path.join(model_root, config["BCO"]), "r") as fp:
        bco = json.load(fp)
    bco_info = handle_BCO(bco)
    ### XXX: Duplicated code is expedient, but needs to be trimmed once
    ### the previous model definitions have been fully deprecated
    if not IN_DJANGO:
        continue
    # Merge name, version, release date from BCO
    config = config | bco_info
    link = "{}".format(config["name"].replace(" ", "-"))

    print(f"XXX Model {config['name']} ::: {link}")

    # Now (possibly) providing support for multiples of condition, intervention, or data types
    condition_names = config["conditions"]
    intervention_names = config["interventions"]
    data_types = config["data_types"]
    if isinstance(data_types, str):
        input_data_type_name = data_types
    elif isinstance(data_types, dict):
        input_data_type_name = list(data_types.keys())[0]

    ReleasedModel.objects.create(
        name=config["name"],
        version=config["version"],
        release_date=config["release_date"],
        data_type=input_data_type_name,
        model_type=config["model_type"],
        data_meta=config["data_meta"],
        backend=config["backend"],
        link=link,
    )

    model = ReleasedModel.objects.filter(name=config["name"]).first()

    for condition_name, description in condition_names.items():
        condition_list = Condition.objects.filter(name=condition_name)
        if not condition_list:
            print(
                f"===> Condition list for {condition_name} was empty! Creating Condition <==="
            )
            Condition.objects.update_or_create(
                name=condition_name,
                description=description,
            )
        condition = Condition.objects.filter(name=condition_name).first()
        model.condition.add(condition)
    for intervention_name, description in intervention_names.items():
        intervention_list = Intervention.objects.filter(name=intervention_name)
        if not intervention_list:
            print(
                f"===> Intervention list for {intervention_name} was empty! Creating Intervention <==="
            )
            Intervention.objects.update_or_create(
                name=intervention_name, description=description
            )
        intervention = Intervention.objects.filter(name=intervention_name).first()
        model.intervention.add(intervention)
    for data_type_name, description in data_types.items():
        data_type_list = InputDataType.objects.filter(name=data_type_name)
        if not data_type_list:
            print(
                f"===> Data type list for {data_type_name} was empty! Creating InputDataType <==="
            )
            InputDataType.objects.update_or_create(
                name=data_type_name, description=description
            )
        data_type = InputDataType.objects.filter(name=data_type_name).first()
        model.input_type.add(data_type)

# Ingest deprecated-definitions configuration
for k, v in released_configs.items():
    if "BCO" in v.keys():
        with open(os.path.join(BCO_DIR, v["BCO"]), "r") as fp:
            bco = json.load(fp)
        bco_info = handle_BCO(bco)
        v.pop("BCO")
        # Requires python 3.9+
        v = v | bco_info
        # BCOs previously only provided name, version, and release date
        # These will be automatically parsed on model submission in
        # future iterations of the model submission pipeline
    if not IN_DJANGO:
        continue
    link = "{}".format(v["name"].replace(" ", "-"))

    print(f"XXX Model {config['name']} ::: {link}")

    condition_name = v["condition"]
    intervention_name = v["intervention"]
    input_data_type_name = v["input_data_type"]

    print(f"===> Creating LEGACY model definition for {v['name']}")

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
    condition = Condition.objects.filter(name=condition_name).first()
    intervention = Intervention.objects.filter(name=intervention_name).first()
    input_data_type = InputDataType.objects.filter(name=input_data_type_name).first()
    if not condition or not intervention or not input_data_type:
        # Error handling
        print("+" * 80)
        if not condition:
            print(f"Condition {condition_name} was empty!")
        if not intervention:
            print(f"Intervention {intervention_name} was empty!")
        if not input_data_type:
            print(f"Data type {input_data_type_name} was empty!")
        print("+" * 80)
        print(f"Released model dict was\n{v}")
        print("+" * 80)

    model = ReleasedModel.objects.filter(name=v["name"]).first()
    model.condition.add(condition)
    model.intervention.add(intervention)
    model.input_type.add(input_data_type)

for k, v in pending_configs.items():
    print(f"Creating Model ---> {k}")
    if not IN_DJANGO:
        continue
    link = "{}-anticipated".format(v["name"].replace(" ", "-"))
    PendingModel.objects.create(
        name=v["name"], version=v["version"], data_type=v["data_type"], link=link
    )
