import axios from "axios";
import Cookies from "js-cookie";

export default axios.create({
  baseURL: "/predictmod/api",
  withCredentials: true,
  headers: {
    // "Content-type": "application/json",
    "Accept": "application/json",
    "X-CSRFToken": Cookies.get('csrftoken'),
  }
});
