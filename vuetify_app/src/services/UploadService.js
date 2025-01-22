import axiosUtility from "./AxiosUtils";

import { useUserStore } from "@/store/user";
class UploadFilesService {

  async upload(json, target, onUploadProgress, labelColumn, columnsToDrop, mode) {
    const userStore = useUserStore();
    const baseURL = import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api': "/predictmod/api";
    // const formData = new FormData();
    // console.log("...Uploading?")
    // const urlDest = "/".concat(target, "-upload/");
    let fullURL = baseURL + `/upload/?q=${target}`;
    // console.log("Target: " + fullURL)
    if (labelColumn) {
      fullURL = fullURL + `&label=${labelColumn}`
    }
    if (mode) {
      fullURL += `&method=${mode}`
    }
    // console.log("Target: " + fullURL)

    if (columnsToDrop) {
      const arrayArg = columnsToDrop.split(",")
      fullURL = fullURL + `&drop=${arrayArg}`
    }
    // console.log("Target: " + fullURL)
    // const headers = {
    //   "Content-type": "application/json",
    //   "X-CSRFToken": userStore.token,
      // "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value(),
    // }

    // XXX
    // console.log("---> Uploading file to %s", fullURL);
    // console.log("---> File contents:\n%s", json);
    // console.log("---> File TYPE:\n%s", typeof(json));
    // console.log("XLS? >>>\n%s", JSON.stringify(xlsFile));

    // formData.append("json", json);

    const res = await fetch(fullURL, {
      method: "POST",
      credentials: "include",
      headers: {
        "Accept": "application/json",
        "X-CSRFToken": userStore.token,
      },
      body: json,
    })

    if (!res.ok) {
      // Error handling
    }

    const response = await res.json();
  
    console.log("---> Got response %s", JSON.stringify(response));

    return response;

    // return axiosUtlity.post(urlDest, formData, headers, {
    //   onUploadProgress
    // });
  }

}

export default new UploadFilesService();
