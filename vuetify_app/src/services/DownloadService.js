// import axiosUtility from "./AxiosUtils";
import axios from "axios";
import Cookies from "js-cookie";

import * as XLSX from 'xlsx';

class DownloadFilesService {
  download(target) {
    // const formData = new FormData();

    const urlDest = "/".concat(target, "-sample/");

    // const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').ariaValueMax();
    // const csrftoken = Cookies.get('csrftoken');
    // console.log("Got a Cookie: %s", JSON.stringify(csrftoken));
    // const headers = {
    //   "Content-type": "application/json",
    //   "X-CSRFToken": csrftoken,
    //   // "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value(),
    // }

    // XXX
    console.log("---> Downloading file from %s", urlDest);
    // console.log("---> File contents:\n%s", json);
    // console.log("---> File TYPE:\n%s", typeof(json));
    // console.log("XLS? >>>\n%s", JSON.stringify(xlsFile));

    // formData.append("json", json);

    const downloadTarget = `http://hivelab.tst.biochemistry.gwu.edu/predictmod${urlDest}`;
    // const downloadTarget = `http://hivelab.biochemistry.gwu.edu/predictmod${urlDest}`;
    // const downloadTarget = `http://localhost:8000/predictmod/api${urlDest}`;

    console.log(`Now downloading from ${downloadTarget}`);

    axios.get(downloadTarget)
      .then(response => {
        const sampleName = target + "_example_data.xlsx";
        const data = JSON.parse(response.data);
        console.log("Received the following:\n%s", response.data);
        console.log("---> Type of received:\n%s", typeof(data));
        console.log("---> Attempting to write to %s", sampleName);
        // Write the response to a file
        console.log("Creating sheet!")
        const worksheet = XLSX.utils.json_to_sheet(data);
        console.log("Creating workbook!")
        const workbook = XLSX.utils.book_new();
        console.log("Appending sheet!")
        XLSX.utils.book_append_sheet(workbook, worksheet);
        console.log("Writing file!")
        XLSX.writeFile(workbook, sampleName, { compression: true });
        console.log("Complete...?")
      })
      .catch(error => {
        console.log("---> ERROR!:\n\t%s", JSON.stringify(error));
      })

    // return axiosUtility.get(urlDest);
  }
}

export default new DownloadFilesService();
