import axiosUtility from "./AxiosUtils";

class UploadFilesService {
  upload(json, target, onUploadProgress) {
    const formData = new FormData();

    const urlDest = "/".concat(target, "-upload")

    console.log("---> Uploading file to %s", urlDest);
    console.log("---> File contents:\n%s", json);
    console.log("---> File TYPE:\n%s", typeof(json));

    // const blob = new Blob([file]);
    // const xlsFile = new File([blob], 'sample.xls');

    // console.log("XLS? >>>\n%s", JSON.stringify(xlsFile));

    formData.append("json", json);

    return axiosUtility.post(urlDest, formData, {
      // headers: {
      //   "Content-Type": "multipart/form-data"
      // },
      onUploadProgress
    });
  }

}

export default new UploadFilesService();
