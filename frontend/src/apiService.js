// import axios from "axios";

// const api = axios.create({
//   baseURL: "http://127.0.0.1:8000/", // Django backend base URL
//   headers: {
//     "Content-Type": "application/json",
//   },
// });

// // Attach token to headers for authenticated requests
// api.interceptors.request.use((config) => {
//   const token = localStorage.getItem("token");
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`;
//   }
//   return config;
// });

// export default api;

import axios from "axios";

// Base configuration for Axios
const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:8000", // Update base URL as required
});

// Attach the token to the Authorization header for all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Logout function
export const logout = async () => {
  try {
    // Call the logout endpoint
    const response = await api.post("/logout/");
    // Clear token from localStorage
    localStorage.removeItem("token");
    return response.data;
  } catch (error) {
    console.error("Logout failed:", error);
    throw error.response?.data || "Logout failed. Please try again.";
  }
};

export default api;
