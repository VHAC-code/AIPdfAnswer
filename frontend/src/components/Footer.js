import React from "react";
import { Typography, Box } from "@mui/material";

const Footer = () => {
  return (
    <Box
      sx={{
        backgroundColor: "rgba(0, 0, 0, 0.6)",
        color: "#fff",
        textAlign: "center",
        padding: "10px 0",
        position: "relative", // Ensure it sticks at the bottom for non-fullscreen pages
        bottom: 0,
        width: "100%",
      }}
    >
      <Typography
        variant="body2"
        sx={{
          fontWeight: "500",
          "&:hover": {
            color: "#0288d1", // Add hover effect for footer text
          },
        }}
      >
        &copy; {new Date().getFullYear()} PDF Q&A App. All Rights Reserved.
      </Typography>
    </Box>
  );
};

export default Footer;
