// import axiosUtility from "./AxiosUtils";
import axios from "axios";
import Cookies from "js-cookie";

// import * as XLSX from 'xlsx';

class DownloadFilesService {
  async download(target) {

    const baseURL = import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api': "/predictmod/api";

    const fullURL = baseURL + `/download/?q=${target}`;

    console.log(`Now downloading from ${fullURL}`);

    const response = await axios.get(fullURL);
    // console.log("Axios: Returned %s", response.data);
    return response.data;

  }
}

export default new DownloadFilesService();
