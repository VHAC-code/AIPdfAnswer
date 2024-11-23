import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // Backend URL
});

export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/upload/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const loginUser = (email, password) => {
  return api.post("/login/", { email, password });
};

export const signupUser = (email, password) => {
  return api.post("/signup/", { email, password });
};
