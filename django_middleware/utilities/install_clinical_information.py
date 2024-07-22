from ui.models import Condition, Intervention, InputDataType

import json
import os
import time
import tomli


with open("./utilities/clinical_information.toml", "rb") as fp:
    clinical_configs = tomli.load(fp)

DRY_RUN = True

for name, description in clinical_configs["conditions"].items():
    interventions = clinical_configs["interventions"][name]
    input_data_types = clinical_configs["input_data_types"][name]

    print(f"===> Creating condition for {name}")
    Condition.objects.update_or_create(
        name=name,
        description=description,
    )
    condition = Condition.objects.filter(name=name).first()
    for i_name, i_description in interventions.items():
        print(f"===> Creating intervention for {i_name} --- under {name}")
        Intervention.objects.update_or_create(
            name=i_name,
            description=i_description,
        )
        # Get the intervention and add the condition to it
        intervention = Intervention.objects.filter(name=i_name).first()
        intervention.conditions.add(condition.id)
        condition.interventions.add(intervention.id)

        for d_name, d_description in input_data_types.items():
            print(f"===> Creating data type for {d_name} --- under {name}")
            InputDataType.objects.update_or_create(
                name=d_name,
                description=d_description,
            )
            # Get the data type and add the condition to it
            data_type = InputDataType.objects.filter(name=d_name).first()
            intervention.input_data_type.add(data_type.id)
            condition.input_data_types.add(data_type.id)
            data_type.conditions.add(condition.id)
            data_type.interventions.add(intervention.id)
