import axios from "axios";
import axiosUtility from "./AxiosUtils";

import { useUserStore } from "@/store/user";

const userStore = useUserStore()

axios.defaults.headers.common['X-CSRFToken'] = userStore.token

class UploadFilesService {

  // Old signature
  // async upload(file, target, onUploadProgress, labelColumn, columnsToDrop, mode, modelName) {
  // New signature
  async upload(uploadFile, target, axiosConfig, actionConfig) {
    const userStore = useUserStore();
    let baseURL = ""
    if (import.meta.env.DEV) {
      baseURL = import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api'
    } else if (import.meta.env.PROD) {
      if (import.meta.env.VITE_PRODUCTION_HOST == 'local'){
        baseURL = import.meta.env.VITE_DOCKER_MIDDLEWARE_BASE + '/api'
      } else {
        baseURL = import.meta.env.VITE_PROD_MIDDLEWARE_BASE + '/api'
      }
    }
    console.log("---> Got a file, with name " + uploadFile.name)
    console.log("---> Using baseURL: " + baseURL)
    let fullURL = baseURL + `/upload/?q=${target}&name=${uploadFile.name}`;
    if (actionConfig) {
      console.log("Running action with config " + JSON.stringify(actionConfig))
      const mode = actionConfig.action
      if (!actionConfig.modelName) {
          alert("Error: modelName not completed when using `mode` toggle")
          return {"Error": "modelName not completed when using `mode` toggle"}
        }
      switch (mode) {
        case 'training':
          fullURL += `&method=${mode}&data_name=${actionConfig.modelName}&label=${actionConfig.labelColumn}`
          const arrayArg = actionConfig.columnsToDrop.split(",")
          fullURL = fullURL + `&drop=${arrayArg}`
          break;
        case 'newSample':
          fullURL += `&method=${mode}&data_name=${actionConfig.modelName}&model_ids=${JSON.stringify(actionConfig.modelIDs)}`
      }
    }
    console.log("---> Uploading file to %s", fullURL);
    console.log("---> File contents:\n%s", uploadFile);
    console.log("---> File TYPE:\n%s", typeof(uploadFile));
    console.log("---> Token: " + userStore.token)

    // const res = await axios.post(fullURL, uploadFile, {headers: 
    //   {
    //     "Content-Type": "multipart/form-data",
    //     "X-CSRFToken": userStore.token,
    //   }
    // });

    // const file = uploadFile.files[0]
    // const formData = new FormData()
    // formData.append('file', file)

    console.log("Issuing request to URL" + fullURL)

    const res = await fetch(fullURL, {
      method: "POST",
      credentials: "include",
      headers: {
        // "Accept": "application/json",
        // "Content-Type": "multipart/form-data",
        "X-CSRFToken": userStore.token,
      },
      body: uploadFile,
    })

    if (!res.ok) {
      // Error handling
      console.log("Is this where I am....?")
      return {
        networkError: "Error " + res.status + ":" + res.statusText,
      }
    }

    const response = await res.json();
  
    // console.log("---> Got response %s", JSON.stringify(response));

    return response

  }

}

export default new UploadFilesService();
