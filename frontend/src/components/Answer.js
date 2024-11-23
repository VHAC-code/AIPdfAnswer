import React from "react";
import { Typography, Box, Card, CardContent } from "@mui/material";
import { motion } from "framer-motion";

const Answer = ({ answer }) => {
  return (
    <Box
      className="flex justify-center items-center bg-gray-100"
      sx={{
        padding: "20px",
        minHeight: "50vh", // Reduce minimum height
      }}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-5xl" // Increased max width
      >
        <Card
          className="shadow-lg hover:shadow-2xl transition-shadow duration-300"
          sx={{
            backgroundColor: "#ffffff",
            borderRadius: "12px",
            overflow: "hidden",
            maxWidth: "100%",
            boxShadow: "0px 8px 20px rgba(0, 0, 0, 0.1)", // Softer shadow for better UI
            padding: "20px",
          }}
        >
          <CardContent>
            <Typography
              variant="h5"
              sx={{
                fontWeight: "bold",
                color: "#4a148c",
                marginBottom: "15px",
                textAlign: "center",
              }}
            >
              AI-Generated Answer
            </Typography>

            {answer ? (
              <Typography
                variant="body1"
                sx={{
                  color: "#424242",
                  whiteSpace: "pre-wrap", // Preserve line breaks
                  lineHeight: 1.6, // Adjust line height for readability
                  padding: "15px",
                  backgroundColor: "#f8f9fa",
                  borderRadius: "8px",
                  boxShadow: "0px 2px 5px rgba(0, 0, 0, 0.1)", // Subtle shadow
                  "&:hover": {
                    backgroundColor: "#e3f2fd", // Highlight on hover
                    cursor: "pointer",
                  },
                  maxHeight: "60vh", // Limit the height for large answers
                  overflowY: "auto", // Add scroll for long answers
                }}
              >
                {answer}
              </Typography>
            ) : (
              <Typography
                variant="body1"
                sx={{
                  color: "#757575",
                  textAlign: "center",
                  fontStyle: "italic",
                }}
              >
                No answer available.
              </Typography>
            )}
          </CardContent>
        </Card>
      </motion.div>
    </Box>
  );
};

export default Answer;
