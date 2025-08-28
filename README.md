# PredictMod
## Introduction
Our goal is to provide clinicians with a powerful decision making tool that enhances clinical understanding of patient-level data. The PredictMod platform utilizes machine learning tools and complex datasets based on electronic health records, gut microbiome, and -omics data to forecast patient outcomes, often in response to treatment for a particular condition. While our primary condition of interest is Prediabetes, the tool is designed to be used for a variety of conditions, interventions, and data types.

The PredictMod web app was designed using [Figma](https://www.figma.com/about/) and implemented using several frameworks, spanning primarily the Python and JavaScript languages.

## Requirements
To run the PredictMod system locally, Python and JavaScript runtimes must be available:  
`node`: >= 10.8.2  
`python3`: >= 3.10.2  

Additionally, to run PredictMod as Docker containers, `docker` (>= 26.1.3) must also be available.

## Setup
#### Cloning the repository
This repository can be cloned directly using the following command: 

```
git clone https://github.com/GW-HIVE/PredictMod.git
```

### Docker installation (production/general use)
Ensure you have docker running in your environment. Then, navigate to the PredictMod directory and use the following commands to:  
1 - Create an approriate docker newtork  
2 - Install the necessary dependencies  
3 - Compile the frontend  
4 - Create and run the dockerized frontend  
5 - Create and run the dockerized middleware  
6 - Create and run the dockerized backend  

#### Create a docker network to serve traffic between containers
```
$ docker network create predictmod
```

#### Install JavaScript dependencies
```
$ cd vuetify_app
$ npm install
```

#### Build and run the frontend docker container
```
$ ./build_frontend.sh
$ ./run_frontend.sh
```

#### Build the middleware and create the initial database
```
$ ./build_middleware
$ ./run_middleware
$ docker exec -it middleware bash
<docker># cd scripts
<docker># ./initialize_db.sh
<docker># exit
$
```
#### Build the backend(s)

```
$ ./build_backend.sh
$ ./run_backend.sh
$ python3 build_backends.py
$ python3 run_backends.py
```

Then open a browser and navigate to `http://localhost:4244/` to begin interacting with the dockerized application.

### Local installation

#### Virtual Environment
Prepare your own virtually environment using the requirement.txt file then activate your environment. Virtual environments are _highly_ recommended when running modern python stacks (i.e. since at least 2015).
See [virtualenvwrapper docs](https://virtualenvwrapper.readthedocs.io/en/latest/) for a primer on creating virtual environments.

#### Installation
Navigate to the PredictMod directory and use the following commands to:  
1 - Install the necessary JavaScript dependencies and start the user interface  
2 - Install the necessary middleware dependencies and start the middleware  
3 - Install the necessary analytical dependencies and start the backend   

**NB**: Running locally will require launching 3 separate processes: 1 node, 1 flask, and 1 django. To have logs visible from all 3, use separate shell instances.

#### Navigate to the `PredictMod` code location (all three shell instances)
```
$ cd <path/to/repo/>
$ cd PredictMod
```
#### Install JavaScript requirements and start the development server (Shell instance 1)
```
$ cd vuetify_app
$ npm install
$ npm run dev
```
#### Install middleware requirements, initialize the database, and start the development server (Shell instance 2)
```
$ cd django_server
$ # Install requirements
$ pip install -r requirements.txt
$ # Initialize the database
$ pushd scripts; ./initialize_db.sh; popd;
$ # Start the server
$ python manage.py runserver
```
#### Install backend requirements and start the development server (Shell instance 3)
```
$ cd flask_backend
$ pip install -r requirements.txt
$ flask --app flask_python_interface.py run
```

#### "Hidden" Dependencies
The sheetJS (CE) library (currently v0.20.0) should be installed manually, as so:
`npm i --save https://cdn.sheetjs.com/xlsx-0.20.0/xlsx-0.20.0.tgz`
See [SheetJS documentation](https://docs.sheetjs.com/docs/getting-started/installation/nodejs) for additional details.

With the three processes running, open a browser window an navigate to localhost:3000 to begin using the local instance.

### Creating your own (dockerized) model
See documentation in `flask_backend/models/new_model_examples/` for additional details.

## Description of Main Folders and Content

#### Archive
Holds files that are currently not in use, but may be useful to reference at a later time. 

#### django_middleware
Contains all resources related to running the Django webserver middleware.

#### flask_backend
Contains all resources required to run the Flask webserver and analysis backend.

#### frontend 
Docker requirements for serving the user interface via `nginx` process. Also establishes reverse proxy activity for middleware access.  

#### models 
Documentation, scripts, BCOs, and datasets for all models. 

#### scripts
Convenience scripts to compile/transpile the frontend and to launch the application.

#### vuetify_app
Contains all resources required to create & run the frontend.

