import axios from "axios";

const api = axios.create({
  baseURL: "http://192.168.1.6:8000/api",
  timeout: 30000,
  headers: {
    "Content-Type": "multipart/form-data",
  },
});

export default api;