// src/components/Header.js
import React from "react";
import { AppBar, Toolbar, Button } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import AddCircleIcon from "@mui/icons-material/AddCircle";

const Header = ({ token, setToken, setDocumentId }) => {
  const navigate = useNavigate();

  // Logout function
  const handleLogout = async () => {
    try {
      if (!token) {
        alert("You are already logged out.");
        return;
      }

      // Clear token from local storage and state
      localStorage.removeItem("token");
      setToken(null);

      alert("Logged out successfully!");
      navigate("/");
    } catch (error) {
      console.error("Logout failed:", error);
      alert("Failed to log out. Please try again.");
    }
  };

  return (
    <AppBar position="sticky" color="primary" elevation={4}>
      <Toolbar className="flex justify-between">
        <motion.div
          whileHover={{ scale: 1.1 }}
          className="text-white font-bold text-xl"
        >
          <img
            src="/aiplanet.png"
            alt="Airplane"
            className="w-[100px] md:w-[120px] h-[80px]"
          />
        </motion.div>
        <div>
          <Button
            component={Link}
            to="/"
            color="inherit"
            className="hover:underline"
          >
            Home
          </Button>
          {token ? (
            <>
              <Button
                component={Link}
                to="/upload"
                color="inherit"
                className="hover:underline"
                startIcon={<AddCircleIcon />}
              >
                Upload File
              </Button>
              <Button
                onClick={handleLogout}
                color="inherit"
                className="hover:underline"
              >
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button
                component={Link}
                to="/login"
                color="inherit"
                className="hover:underline"
              >
                Login
              </Button>
              <Button
                component={Link}
                to="/signup"
                color="inherit"
                className="hover:underline"
              >
                Sign Up
              </Button>
            </>
          )}
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
