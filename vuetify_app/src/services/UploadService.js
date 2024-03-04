import axiosUtility from "./AxiosUtils";

import { useUserStore } from "@/store/user";
class UploadFilesService {

  async upload(json, target, onUploadProgress) {
    const userStore = useUserStore();
    const baseURL = import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api': "/predictmod/api";
    // const formData = new FormData();

    const urlDest = "/".concat(target, "-upload/");
    const fullURL = baseURL.concat(urlDest);
    // const headers = {
    //   "Content-type": "application/json",
    //   "X-CSRFToken": userStore.token,
      // "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value(),
    // }

    // XXX
    // console.log("---> Uploading file to %s", urlDest);
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
