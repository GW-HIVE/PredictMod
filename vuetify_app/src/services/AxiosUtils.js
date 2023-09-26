import axios from "axios";
import Cookies from "js-cookie";

export default axios.create({
  baseURL: "https://hivelab.biochemistry.gwu.edu/predictmod",
  headers: {
    "Content-type": "application/json",
    "X-CSRFToken": Cookies.get('csrftoken'),
  }
});
