import React, { useState } from "react";
import { TextField, Button, Typography, Box } from "@mui/material";
import { useNavigate } from "react-router-dom"; // Import useNavigate hook
import api from "../apiService"; // Using centralized apiService

const Login = ({ setToken }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate(); // Initialize navigate function

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // API call to login
      const response = await api.post("/auth/login/", { email, password });
      const token = response.data.access_token;

      // Save token to localStorage and App state
      saveToken(token);

      alert("Login successful!");

      // Redirect to home page after successful login
      navigate("/");
    } catch (error) {
      console.error("Login failed:", error);
      alert(
        error.response?.data?.detail || "Invalid credentials. Please try again."
      );
    }
  };

  // Function to save the token in both state and localStorage
  const saveToken = (token) => {
    localStorage.setItem("token", token); // Save to localStorage
    setToken(token); // Set in App state
  };

  return (
    <Box
      className="flex flex-col items-center justify-center min-h-screen bg-gray-50"
      boxShadow={3}
      p={4}
      borderRadius={2}
      maxWidth={400}
      mx="auto"
    >
      <Typography
        variant="h4"
        className="text-blue-500 font-bold mb-6 text-center"
      >
        Login
      </Typography>
      <form onSubmit={handleSubmit} className="flex flex-col w-full gap-4">
        <TextField
          label="Email"
          variant="outlined"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          fullWidth
          required
        />
        <TextField
          label="Password"
          variant="outlined"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          fullWidth
          required
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          size="large"
          className="mt-4 hover:bg-blue-600 transition-transform transform hover:scale-105"
        >
          Login
        </Button>
      </form>
    </Box>
  );
};

export default Login;
