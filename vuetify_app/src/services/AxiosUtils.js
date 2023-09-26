import axios from "axios";
import Cookies from "js-cookie";

export default axios.create({
  baseURL: "https://hivelab.tst.biochemistry.gwu.edu/predictmod-beta",
  headers: {
    "Content-type": "application/json",
    "X-CSRFToken": Cookies.get('csrftoken'),
  }
});
