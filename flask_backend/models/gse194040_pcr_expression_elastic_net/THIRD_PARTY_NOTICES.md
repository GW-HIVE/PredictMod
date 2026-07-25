# Third-party notices

This inventory identifies third-party material using information already
present in the package. It does not replace the corresponding upstream licence
texts. Where no terms are recorded, the required notice remains unresolved.

## PredictMod upstream repository

- Repository: `GW-HIVE/PredictMod`
- Licence: MIT License
- Copyright: `Copyright © 2022 HIVE-Lab`
- Source: the upstream `GW-HIVE/PredictMod` `LICENSE` file

This notice records the verified upstream repository source-code licence. The
submitted trained model has a separate CC BY 4.0 licence under the PredictMod
User Guide.

## GSE194040 source data

- Provider: NCBI Gene Expression Omnibus
- Accession: `GSE194040`
- Record title: "I-SPY2-990 mRNA/RPPA Data Resource: mRNA component"
- GEO series contributors: Denise Wolf, Christina Yau, Laura van 't Veer
- PubMed identifiers recorded by the GEO series: `35623341`, `40905691`
- Accession URL:
  `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE194040`

The GEO archives and full processed training CSV are intentionally excluded.
Original GSE194040 data remain governed by NCBI GEO and the original data
submitters' terms. The PredictMod MIT source-code licence and PredictMod CC BY
4.0 model/database-set terms are not asserted to cover the original GEO data.

## PredictMod model and database-set licensing references

- PredictMod User Guide:
  `https://hivelab.biochemistry.gwu.edu/predictmod/help`
- User-guide source:
  `https://github.com/GW-HIVE/PredictMod/blob/main/vuetify_app/src/docs/help_content/help.md`
- HIVE PredictMod website:
  `https://hivelab.biochemistry.gwu.edu/predictmod/`
- Website licence-component source:
  `https://github.com/GW-HIVE/PredictMod/blob/main/vuetify_app/src/views/LicenseShow.vue`

The User Guide applies CC BY 4.0 to shared models. The website licence
component applies CC BY 4.0 to PredictMod database sets.

## IEEE 2791 v1.4 schema snapshot

The files under `schemas/ieee-2791-v1.4/` were retrieved on 2026-07-19 from:

`https://github.com/biocompute-objects/BCO_Documentation/tree/main/ieee-2791-schema`

They are included for offline BCO validation. No schema licence or
redistribution notice is included in the package; those terms must be confirmed.

## Python dependencies

The directly pinned Python dependencies are:

- joblib 1.5.3
- jsonschema 4.26.0
- matplotlib 3.11.1
- NumPy 2.5.1
- pandas 2.2.2
- pytest 9.1.1
- referencing 0.37.0
- scikit-learn 1.9.0
- SciPy 1.18.0

`requirements-lock.txt` records the full transitive environment. The package
does not contain dependency licence texts, so this notice does not assert their
licence terms. Required upstream notices must be collected before distributing
a bundled environment or container image.

## Container base image

The Dockerfile uses `python:3.12.13-slim`. No base-image licence notice is
included in this package. Its applicable terms and required notices must be
confirmed before distributing a built image.
