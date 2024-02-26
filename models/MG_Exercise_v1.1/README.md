### MG Python Predict - Workflow
The python prediction module has been separated to allow creation & training of the decision tree, followed by "pickling" (ie, storing long term or "preserving" the tree). The pickle is then read & restored to a python object in a separate script, which uses the tree to perform prediction. The workflow is as follows:
1. Create a tree: `python create_tree.py`
2. Use the tree to perform a prediction: `python use_tree.py`

Use/updates by the PredictMod interface requires manually copying the pickled object to the `matlab-interface` directory. 

# NB
In general, binary objects (including Excel files, pdfs, etc.) should not be stored in GitHub. In line with that, the pickle must be created locally using `create_tree.py`. The `.gitignore` file has been updated to ignore `*.pickle` files, generally.
