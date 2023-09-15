import axiosUtility from "./AxiosUtils";
import Cookies from "js-cookie";

class UploadFilesService {
  upload(json, target, onUploadProgress) {
    const formData = new FormData();

    const urlDest = "/".concat(target, "-upload/");

    // const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').ariaValueMax();
    const csrftoken = Cookies.get('csrftoken');
    // console.log("Got a Cookie: %s", JSON.stringify(csrftoken));
    const headers = {
      "Content-type": "application/json",
      "X-CSRFToken": csrftoken,
      // "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value(),
    }

    // XXX
    // console.log("---> Uploading file to %s", urlDest);
    // console.log("---> File contents:\n%s", json);
    // console.log("---> File TYPE:\n%s", typeof(json));
    // console.log("XLS? >>>\n%s", JSON.stringify(xlsFile));

    formData.append("json", json);

    return axiosUtility.post(urlDest, formData, headers, {
      onUploadProgress
    });
  }

}

export default new UploadFilesService();
