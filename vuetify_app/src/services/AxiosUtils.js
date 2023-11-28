import axios from "axios";
import Cookies from "js-cookie";

export default axios.create({
  baseURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api': "/predictmod/api",
  withCredentials: true,
  headers: {
    // "Content-type": "application/json",
    "Accept": "application/json",
    "X-CSRFToken": Cookies.get('csrftoken'),
  }
});
