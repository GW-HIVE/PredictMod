import axios from "axios";

export default axios.create({
  baseURL: "http://hivelab.tst.biochemistry.gwu.edu:4245",
  headers: {
    "Content-type": "application/json"
  }
});
