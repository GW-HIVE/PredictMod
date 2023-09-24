// import axiosUtility from "./AxiosUtils";
import axios from "axios";
import Cookies from "js-cookie";

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

    const downloadTarget = `http://middleware:8000${urlDest}`;

    console.log(`Now downloading from ${downloadTarget}`);

    axios.get(downloadTarget)
      .then(response => {
        console.log(response);
        return response;
      })
      .catch(error => {
        console.log("---> ERROR!:\n\t%s", JSON.stringify(error));
      })

    // console.log("Received the following:\n%s", JSON.stringify(response));

    // return axiosUtility.get(urlDest);
  }

}

export default new DownloadFilesService();
