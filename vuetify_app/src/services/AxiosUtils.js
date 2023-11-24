import axios from "axios";
import Cookies from "js-cookie";


function resolveTargetURL() {
  const MODE = import.meta.env.MODE;
  if (MODE === 'development') {
    return import.meta.env.VITE_DEV_MIDDLEWARE_URL;
  } else if (MODE === 'production') {
    return import.meta.env.VITE_PROD_MIDDLEWARE_URL;
  }
};

export default axios.create({
  baseURL: resolveTargetURL(),
  withCredentials: true,
  headers: {
    // "Content-type": "application/json",
    "Accept": "application/json",
    "X-CSRFToken": Cookies.get('csrftoken'),
  }
});
