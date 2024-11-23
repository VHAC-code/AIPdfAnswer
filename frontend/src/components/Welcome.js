// src/components/Welcome.js
import React from "react";
import { motion } from "framer-motion";
import {
  Grid,
  Box,
  Typography,
  Card,
  CardContent,
  Button,
} from "@mui/material";
import { Link } from "react-router-dom";

const Welcome = ({ isLoggedIn }) => {
  if (!isLoggedIn) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="flex flex-col items-center min-h-screen"
        style={{
          background: "url('/pdf.png') no-repeat center center/cover",
          height: "50vh", // Set the image height
          color: "#fff",
        }}
      >
        <Box
          sx={{
            textAlign: "center",
            padding: "20px",
            marginTop: "20vh", // Space content below the image
          }}
        >
          <motion.div
            whileHover={{ scale: 1.1 }}
            transition={{ duration: 0.3 }}
          >
            <Typography
              variant="h2"
              sx={{
                fontWeight: "bold",
                textShadow: "2px 2px 4px rgba(0, 0, 0, 0.7)",
                color: "#f5f5f5",
              }}
            >
              Welcome to the PDF Q&A App
            </Typography>
          </motion.div>
          <motion.div
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.3 }}
          >
            <Typography
              variant="h6"
              sx={{
                marginTop: "20px",
                textShadow: "1px 1px 3px rgba(0, 0, 0, 0.5)",
                fontStyle: "italic",
                fontWeight: "500",
                color: "#cfd8dc",
              }}
            >
              Effortlessly upload PDFs, ask questions, and receive AI-generated
              answers.
            </Typography>
          </motion.div>
          <Button
            variant="contained"
            component={Link}
            to="/login"
            sx={{
              marginTop: "30px",
              backgroundColor: "#0288d1",
              "&:hover": { backgroundColor: "#01579b" },
              color: "#fff",
              padding: "10px 20px",
              fontSize: "18px",
              textTransform: "none",
              borderRadius: "8px",
              boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.3)",
            }}
          >
            Get Started
          </Button>
        </Box>
      </motion.div>
    );
  }

  // Content when logged in
  const featureDetails = [
    {
      title: "What Does This App Do?",
      description:
        "This app allows you to upload PDF files, ask specific questions related to the uploaded document, and get precise answers powered by AI.",
      color: "#f9f9f9",
    },
    {
      title: "How It Works",
      description:
        "1. Upload your PDF document.\n2. Ask a question related to the document's content.\n3. The app processes your question using advanced AI tools and retrieves the most relevant answer.",
      color: "#e3f2fd",
    },
    {
      title: "AI Technology Behind It",
      description:
        "This app uses advanced AI tools like Sentence Transformers and Hugging Face's GPT-2 model to process your questions and generate accurate answers.",
      color: "#fff3e0",
    },
    {
      title: "How to Use This App",
      description:
        "1. Sign up and log in.\n2. Navigate to the 'Upload File' section and upload your PDF.\n3. Go to the 'Ask Question' section and type your query.\n4. Receive instant answers!",
      color: "#ede7f6",
    },
    {
      title: "What Questions Can You Ask?",
      description:
        "You can ask any question related to the uploaded document, such as:\n- Summarize the document.\n- What are the key points?\n- Explain a specific section.",
      color: "#f1f8e9",
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col items-center min-h-screen"
      style={{
        backgroundColor: "#f5f5f5",
        padding: "20px",
      }}
    >
      <Box
        sx={{
          width: "100%",
          textAlign: "center",
          marginBottom: "40px",
        }}
      >
        <motion.div whileHover={{ scale: 1.05 }} transition={{ duration: 0.3 }}>
          <Typography
            variant="h2"
            sx={{
              fontWeight: "bold",
              color: "#1a237e",
            }}
          >
            Welcome Back!
          </Typography>
          <Typography
            variant="subtitle1"
            sx={{
              fontSize: "18px",
              color: "#455a64",
            }}
          >
            Upload PDFs, ask questions, and explore your answers!
          </Typography>
        </motion.div>
      </Box>

      <Grid container spacing={4} justifyContent="center">
        {featureDetails.map((feature, index) => (
          <Grid
            item
            xs={12}
            sm={6}
            md={4}
            key={index}
            component={motion.div}
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.3 }}
          >
            <Card
              sx={{
                backgroundColor: feature.color,
                boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
                borderRadius: "10px",
                transition: "transform 0.3s",
                "&:hover": {
                  boxShadow: "0 6px 16px rgba(0, 0, 0, 0.4)",
                },
              }}
            >
              <CardContent>
                <Typography
                  variant="h5"
                  sx={{
                    fontWeight: "bold",
                    color: "#37474f",
                    marginBottom: "10px",
                  }}
                >
                  {feature.title}
                </Typography>
                <Typography
                  variant="body1"
                  sx={{
                    color: "#607d8b",
                    whiteSpace: "pre-line",
                  }}
                >
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </motion.div>
  );
};

export default Welcome;
