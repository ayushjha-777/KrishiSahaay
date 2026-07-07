import axios from "axios";
import { API_CONFIG } from "../config/api";

const api = axios.create({
  baseURL: "https://krishisahaay.onrender.com/api",
  timeout: 30000,
  headers: {
    "Content-Type": "multipart/form-data",
  },
});

export default api;