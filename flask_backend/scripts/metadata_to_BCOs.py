import json
import os

from pathlib import Path


MODEL_DIR = os.path.join(Path(__file__).parent.parent, "models/")

models = {
    "Diabetes_EHR_v1": "BCO_raw_Diabetes_EHR_Classifier.json",
    "Epilepsy_microbiome_v1": "BCO_raw_Epilepsy_classifier.json",
    "MDClone_Diet_Counseling_v1.1": "BCO/mdclone_diet_counseling.json",
    "MG_Exercise_v1.1": "BCO/literature_exercise_mg.json",
    "PredictMod_EHR_Keto_v1.0": "BCO/temp_PEHR.json",
    "mdclone_exercise": "BCO.json",
    "mdclone_semaglutide": "BCO.json",
    "ovarian_cancer_methylation": "BCO.json",
    "ovarian_rnaseq": "BCO.json",
    "prediabetes_proteomics": "BCO/prediabetes_proteomics.json",
    "gwu-internal/karina_martinez/Diabetes_glycomic": "BCO_Diabetes_Glycomic.json",
    "gwu-internal/karina_martinez/ccRCC_glycoproteomic": "BCO_ccRCC_Glycoproteomic.json",
    }

for model_root, bco_file in models.items():
    model_path = os.path.join(MODEL_DIR, model_root)
    metadata_path = os.path.join(model_path, "metadata.json")
    bco_path = os.path.join(model_path, bco_file)
    if not os.path.isfile(metadata_path):
        if "EHR_Keto" in metadata_path:
            # No metadata was extractable
            continue
        print(f"Model {model_path} missing metadata!")
    if not os.path.isfile(bco_path):
        print(f"Model {bco_file} missing BCO!")

    # Get the new metadata
    with open(metadata_path, "r") as input_json:
        metadata = json.load(input_json)
    with open(bco_path, "r") as original_bco:
        bco = json.load(original_bco)

    for key in metadata.keys():
        bco["description_domain"][key] = metadata[key]
    with open(bco_path, "w") as output_fp:
        json.dump(bco, output_fp, indent=2)

