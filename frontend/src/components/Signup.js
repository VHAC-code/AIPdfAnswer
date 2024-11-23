import React, { useState } from "react";
import { TextField, Button, Typography, Box } from "@mui/material";
import { useNavigate } from "react-router-dom"; // Import useNavigate hook
import api from "../apiService"; // Using centralized apiService

const Signup = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate(); // Initialize navigate function

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // API call to register
      await api.post("/auth/register/", { name, email, password });
      alert("User registered successfully!");

      // Redirect to home page after successful signup
      navigate("/");
    } catch (error) {
      console.error("Signup failed:", error);
      alert(
        error.response?.data?.detail || "Unable to register. Please try again."
      );
    }
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
        className="text-green-500 font-bold mb-6 text-center"
      >
        Sign Up
      </Typography>
      <form onSubmit={handleSubmit} className="flex flex-col w-full gap-4">
        <TextField
          label="Name"
          variant="outlined"
          value={name}
          onChange={(e) => setName(e.target.value)}
          fullWidth
          required
        />
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
          color="success"
          size="large"
          className="mt-4 hover:bg-green-600 transition-transform transform hover:scale-105"
        >
          Sign Up
        </Button>
      </form>
    </Box>
  );
};

export default Signup;
