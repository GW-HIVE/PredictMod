import axios from "axios";
import Cookies from "js-cookie";

export default axios.create({
  baseURL: "http://middleware:8000/",
  headers: {
    "Content-type": "application/json",
    "X-CSRFToken": Cookies.get('csrftoken'),
  }
});
