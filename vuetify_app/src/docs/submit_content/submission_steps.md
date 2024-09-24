# Model submission guidelines
You've recently created a fantastic new AI/ML model. Congratulations! We will be happy to help you share it throughout 
the broader clinical practice and research communities. There are just a few more steps to follow before we get
to that goal.

## Required components
There are a few things we require in order to host any new models in our ecosystem.
### 1. Dependencies.
We will host your model in it's very own `docker` container, isolated from all of its noisy neighbors. In order 
to facilitate that, we need to know everything about the software your model runs, including major software and 
any package specifications that come along with it. For example, we need to know not just `python` and `scikit-learn`, 
but specifically major and minor revisions, e.g. `python 3.10` or `scikit-learn==1.2.3`. 
### 2. Inputs, the model, an example of the model running, and expected outputs
When we implement your model, we all need to know if it is working as expected or if there has been an unexpected 
"update" that prevents it from working. So, we need to have:  
    <br>
    **1.** One or more example input(s): Examples where the expected outcome is known _a priori_ to validate that your 
model is working as expected  
    **2.** A `pickle`, or other model-persistence object, that allows models to be loaded directly from disk to memory.  
    **2.1** - In absence of a `pickle` or similar, we require the appropriate training data and training script(s) for 
your model so that we can train & persist the model _in situ_.  
    **3.** An example: An end-to-end, concrete instance of working code that loads an input, loads the model, performs 
the computation, and generates the prediction.  
    **4.** Outputs; the list of expected outcomes from the provided input data point(s).  
    <br>
### 3. A complete BioCompute Object (BCO) describing the model provenance, data, and other pertinent information
BCOs are an IEEE standardized means of tracking the provenance of Bioinformatics Analyses 
(cf [the paper introducing BCOs](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5510742/), doi: 10.5731/pdajpst.2016.006734). 
Though BCOs can be written manually, we provide a tool to help simplify creation at the 
[BCO Portal](https://www.biocomputeobject.org/). Broadly, PredictMod uses BCOs to ensure fidelity of the models to what 
users expect the correct output *ought* to be.  
<br>
Correctly constructed BCOs for model submission to PredictMod minimally contain the identifying information about the 
data used to train a model, the process(es) used in training and/or optimizing the model, and expected outputs from 
the model. An ideal BCO contains the all provenance data, or links to it, and is sufficient to fully recreate the model 
from the data to reproduce the expected outputs. 

## Next steps
Once all you have all of the required components in hand, reach out to us at mazumder_lab@gwu.edu and we will be happy 
to begin onboarding your new model into our platform!

## Questions?
Check out our [help](/predictmod/help) or [FAQs](/predictmod/faq) for reference material. 
Still have questions? Please email us at mazumder_lab@gwu.edu with questions you may have about the process. 
