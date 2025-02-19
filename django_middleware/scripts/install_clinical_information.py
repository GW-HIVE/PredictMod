from ui.models import Condition, Intervention, InputDataType

import json
import os
import time
import tomli


with open("./scripts/clinical_information.toml", "rb") as fp:
    clinical_configs = tomli.load(fp)


def handle_interventions(condition: Condition, interventions=None):
    if interventions is None:
        return
    for i_name, i_description in interventions.items():
        print(f"===> Creating intervention for {i_name} --- under {name}")
        Intervention.objects.update_or_create(
            name=i_name,
            description=i_description,
        )
        # Get the intervention and add the condition to it
        intervention = Intervention.objects.filter(name=i_name).first()
        input_data_types = Condition.objects.filter(
            input_data_types__conditions__name__contains=condition.name
        )
        for input_type in input_data_types:
            input_type.interventions.add(input_type.id)
        intervention.conditions.add(condition.id)
        condition.interventions.add(intervention.id)


def handle_data_types(condition: Condition, input_data_types=None):
    if input_data_types is None:
        return
    for d_name, d_description in input_data_types.items():
        print(f"===> Creating data type for {d_name} --- under {name}")
        InputDataType.objects.update_or_create(
            name=d_name,
            description=d_description,
        )
        # Get the data type and add the condition to it
        data_type = InputDataType.objects.filter(name=d_name).first()
        interventions = Condition.objects.filter(
            interventions__conditions__name__contains=condition.name
        )
        for intervention in interventions:
            intervention.input_data_types.add(data_type.id)
        condition.input_data_types.add(data_type.id)
        data_type.conditions.add(condition.id)
        data_type.interventions.add(intervention.id)


print(f"====\tInstalling clinical information\t====")
for name, description in clinical_configs["conditions"].items():
    interventions = (
        None
        if name not in clinical_configs["interventions"]
        else clinical_configs["interventions"][name]
    )
    input_data_types = (
        None
        if name not in clinical_configs["input_data_types"]
        else clinical_configs["input_data_types"][name]
    )

    print(f"===> Creating condition for {name}")
    Condition.objects.update_or_create(
        name=name,
        description=description,
    )
    condition = Condition.objects.filter(name=name).first()
    handle_interventions(condition, interventions)

    handle_data_types(condition, input_data_types)
