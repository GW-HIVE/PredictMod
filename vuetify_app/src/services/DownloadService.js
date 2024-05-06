// import axiosUtility from "./AxiosUtils";
import axios from "axios";
import Cookies from "js-cookie";

// import * as XLSX from 'xlsx';

class DownloadFilesService {
  async download(target) {
    // const formData = new FormData();

    // const urlDest = "/".concat(target, "-sample/");
    const baseURL = import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api': "/predictmod/api";

    const fullURL = baseURL + `/download/?q=${target}`;

    // const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').ariaValueMax();
    // const csrftoken = Cookies.get('csrftoken');
    // console.log("Got a Cookie: %s", JSON.stringify(csrftoken));
    // const headers = {
    //   "Content-type": "application/json",
    //   "X-CSRFToken": csrftoken,
    //   // "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value(),
    // }

    // XXX
    // console.log("---> Downloading file from %s", urlDest);
    // console.log("---> File contents:\n%s", json);
    // console.log("---> File TYPE:\n%s", typeof(json));
    // console.log("XLS? >>>\n%s", JSON.stringify(xlsFile));

    // formData.append("json", json);

    // const downloadTarget = `https://hivelab.tst.biochemistry.gwu.edu/predictmod/api${urlDest}`;
    // const downloadTarget = `http://hivelab.biochemistry.gwu.edu/predictmod/api${urlDest}`;
    // const downloadTarget = `http://localhost:8000/predictmod/api/download/q=${urlDest}`;

    console.log(`Now downloading from ${fullURL}`);

    const response = await axios.get(fullURL);
    // console.log("Axios: Returned %s", response.data);
    return response.data;

    // axios.get(fullURL)
    //   .then(response => {
    //     const sampleName = target + "_example_data.xlsx";
    //     const data = JSON.parse(response.data);
    //     console.log("Received the following: (type %s)\n%s", typeof(response.data), response.data);
    //     return response.data;
    //   })
    //   .catch(error => {
    //     console.log("---> ERROR!:\n\t%s", JSON.stringify(error));
    //   })

    // return axiosUtility.get(urlDest);
  }
}

export default new DownloadFilesService();
