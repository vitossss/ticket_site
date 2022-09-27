import axios from "axios";

export const API_URL = "http://127.0.0.1:8000/api/v1/"

const instance = axios.create({
    baseURL: API_URL
});

// instance.interceptors.request.use((config) => {
//     const token = localStorage.getItem('token');
//     if (token) {config.headers.Authorization = `Token ${token}`}
//     return config;
// })

export default instance;