# PredictMod
## Introduction
PredictMod is a web app created to inform physicians' decisions. PredictMod takes metagenomic gastrointestinal (GI) microbiome and electronic health record (EHR) data as input and uses a machine learning algorithm to form predictions of whether the ketogenic diet may be successful. 

The PredictMod web app was designed using Figma and implemented using a JavaScript Vue/Vuetify/Vite framework. For more information on these, see the links below:

[VueJS Repository](https://github.com/vuejs/core)

[VueJS Tutorial](https://code.visualstudio.com/docs/nodejs/vuejs-tutorial)

[Vuetify Home](https://vuetifyjs.com/en/)

[Vite Home](https://vitejs.dev/)

[Figma About Page](https://www.figma.com/about/)


## Setup
#### Cloning the repository
This repository can be cloned directly using the following command: 

```
git clone https://github.com/GW-HIVE/PredictMod.git
```

### Docker installation (production/general use)
Ensure you have docker running in your environment. Then, navigate to the PredictMod directory and use the following commands to:
1 - Install the necessary dependencies
2 - Transpile/Compile the frontend
3 - Create the dockerized frontend
4 - Create the dockerized backend
5 - Launch the service

```
$ cd vuetify_app
$ npm install
$ cd ../scripts
$ ./compile_frontend.sh
$ ./build_frontend.sh
$ docker network create predictmod
$ ./run_frontend.sh
$ ./run_backend.sh
```
Then open a browser and navigate to `http://localhost:4244/` to begin interacting with the dockerized application.
### Local installation

#### Virtual Environment
Prepare your own virtually environment using the requirement.txt file then activate your environment.
See [virtualenvwrapper docs](https://virtualenvwrapper.readthedocs.io/en/latest/) for a primer on creating virtual environments.

#### Installation
Navigate to the PredictMod directory and use the following commands to:
1 - Install the necessary dependencies
2 - Transpile/Compile the frontend
3 - Run the server locally
```
$ pwd
<path/to/repo/>/PredictMod
$ cd vuetify_app
$ npm install
$ cd ../scripts
$ ./compile_frontend.sh
$ cd ../django_server
$ python manage.py runserver
```
Then navigate to `http://localhost:8000/` and to begin working with the interface.

#### "Hidden" Dependencies
The most current version of the sheetJS (CE) library (currently 0.20.0) should be installed manually, as so:
`npm i --save https://cdn.sheetjs.com/xlsx-0.20.0/xlsx-0.20.0.tgz`
See [SheetJS documentation](https://docs.sheetjs.com/docs/getting-started/installation/nodejs) for additional details.

#### Running the app

Navigate to the upload-api directory and execute the following command to start the server:

```
npm start
```
Navigate to the vue-upload directory and execute the following command to start the app:
```
npm run serve
```
Now a link should appear, which you can follow to see the client side of the app

**NB**: The application will not have an analytical backend supporting it if run through `npm`, so no Python analysis will take place in this mode. 

## Description of Main Folders and Content

#### Archive
Holds files that are currently not in use, but may be useful to reference at a later time. 

#### django_server
Contains all resources related to running the Django webserver middleware.
#### EHR_predict
Work related to Electronic Health Records (EHR) prediction.

#### flask-backend
Contains all resources required to run the Flask webserver and analysis backend.

#### Metagenomic_predict 
Work related to metgenomics prediction conducted in MATLAB. 

#### MG_python
Work related to Metagenomics predictions conducted in Python. 

#### EHR_python
Work related to EHR predictions conducted in Python. 

#### scripts
Convenience scripts to compile/transpile the frontend and to launch the application.

#### vuetify_app
Contains all resources required to create & run the frontend.

