// import React, { useState } from "react";
// import { Button, TextField, Typography, Box } from "@mui/material";
// import CloudUpload from "@mui/icons-material/CloudUpload";
// import api from "../apiService"; // Centralized API service

// function QuestionForm({ documentId, userId }) {
//   const [question, setQuestion] = useState("");
//   const [answer, setAnswer] = useState("");

//   const handleAskQuestion = async () => {
//     if (!question.trim()) {
//       alert("Please enter a question!");
//       return;
//     }

//     if (!documentId || !userId) {
//       alert("No document uploaded. Please upload a document first.");
//       return;
//     }

//     try {

//       const response = await api.post("/queries/ask", {
//         question,
//         document_id: documentId,
//         user_id: userId,
//       });
//       setAnswer(response.data.answer);
//     } catch (error) {
//       console.error("Error fetching answer:", error);
//       setAnswer("Error getting answer. Please try again.");
//     }
//   };

//   return (
//     <Box className="mt-4">
//       <Typography variant="h6" className="text-gray-700 font-semibold mb-2">
//         Ask a Question about the uploaded file
//       </Typography>
//       <TextField
//         label="Your Question"
//         variant="outlined"
//         value={question}
//         onChange={(e) => setQuestion(e.target.value)}
//         fullWidth
//         className="mb-4"
//       />
//       <Button
//         variant="contained"
//         onClick={handleAskQuestion}
//         className="bg-green-500 hover:bg-green-600"
//       >
//         Ask
//       </Button>
//       {answer && (
//         <Typography
//           variant="body1"
//           className="mt-4 text-blue-500 font-semibold"
//         >
//           Answer: {answer}
//         </Typography>
//       )}
//     </Box>
//   );
// }

// const FileUpload = () => {
//   const [file, setFile] = useState(null);
//   const [documentId, setDocumentId] = useState(null);
//   const [userId, setUserId] = useState(null);

//   const onFileChange = (e) => {
//     setFile(e.target.files[0]);
//   };

//   const onFileUpload = async () => {
//     if (!file) {
//       alert("Please choose a file first!");
//       return;
//     }

//     const formData = new FormData();
//     formData.append("file", file);

//     try {

//       const response = await api.post("/documents/upload", formData, {
//         headers: { "Content-Type": "multipart/form-data" },
//       });

//       const { document_id, user_id } = response.data;
//       if (document_id && user_id) {
//         setDocumentId(document_id);
//         setUserId(user_id);
//         alert("File uploaded successfully");
//       } else {
//         alert("Failed to upload document.");
//       }
//     } catch (error) {
//       console.error("Error uploading file:", error);
//       alert("Failed to upload file. Please try again.");
//     }
//   };

//   return (
//     <Box
//       className="flex flex-col items-center justify-start p-10 bg-gray-50 rounded-lg shadow-md max-w-full h-full"
//       sx={{
//         minHeight: "100vh",
//         paddingBottom: "100px",
//         display: "flex",
//         flexDirection: "column",
//         justifyContent: "flex-start",
//         alignItems: "center",
//         overflowY: "auto",
//         transition: "box-shadow 0.3s ease-in-out",
//         "&:hover": {
//           boxShadow: "0px 6px 16px rgba(0, 0, 0, 0.2)",
//         },
//       }}
//     >
//       <Typography variant="h5" className="text-blue-500 font-bold mb-4">
//         Upload a PDF
//       </Typography>
//       <TextField
//         type="file"
//         onChange={onFileChange}
//         fullWidth
//         InputProps={{
//           inputProps: { accept: "application/pdf" },
//         }}
//         className="mb-4"
//         sx={{
//           backgroundColor: "#f9fafb",
//           padding: "12px",
//           borderRadius: "8px",
//         }}
//       />
//       <Button
//         variant="contained"
//         startIcon={<CloudUpload />}
//         onClick={onFileUpload}
//         className="bg-blue-500 hover:bg-blue-600 transition-colors"
//         sx={{
//           width: "100%",
//           fontSize: "16px",
//           padding: "12px",
//           textTransform: "none",
//           "&:hover": {
//             backgroundColor: "#1d4ed8",
//           },
//         }}
//       >
//         Upload
//       </Button>
//       {/* Only show the question form when a document is uploaded */}
//       {documentId && userId && (
//         <QuestionForm documentId={documentId} userId={userId} />
//       )}
//     </Box>
//   );
// };

// export default FileUpload;

import React, { useState } from "react";
import { Button, TextField, Box, Typography } from "@mui/material";
import CloudUpload from "@mui/icons-material/CloudUpload";
import api from "../apiService"; // Centralized API service
import Answer from "./Answer"; // Import the Answer component

function QuestionForm({ documentId, userId }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAskQuestion = async () => {
    if (!question.trim()) {
      alert("Please enter a question!");
      return;
    }

    if (!documentId || !userId) {
      alert("No document uploaded. Please upload a document first.");
      return;
    }

    try {
      const response = await api.post("/queries/ask", {
        question,
        document_id: documentId,
        user_id: userId,
      });
      setAnswer(response.data.answer);
    } catch (error) {
      console.error("Error fetching answer:", error);
      setAnswer("Error getting answer. Please try again.");
    }
  };

  return (
    <Box className="mt-4 space-y-6 w-full max-w-md mx-auto">
      <Typography
        variant="h6"
        className="text-gray-700 font-semibold mb-2 text-center"
      >
        Ask a Question about the uploaded file
      </Typography>
      <TextField
        label="Your Question"
        variant="outlined"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        fullWidth
        className="mb-4"
      />
      <Button
        variant="contained"
        onClick={handleAskQuestion}
        className="bg-green-500 hover:bg-green-600 w-full"
      >
        Ask
      </Button>

      {/* Display the answer if it exists */}
      {answer && <Answer answer={answer} />}
    </Box>
  );
}

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [documentId, setDocumentId] = useState(null);
  const [userId, setUserId] = useState(null);

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const onFileUpload = async () => {
    if (!file) {
      alert("Please choose a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/documents/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const { document_id, user_id } = response.data;
      if (document_id && user_id) {
        setDocumentId(document_id);
        setUserId(user_id);
        alert("File uploaded successfully");
      } else {
        alert("Failed to upload document.");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to upload file. Please try again.");
    }
  };

  return (
    <Box className="flex flex-col items-center justify-start p-10 bg-gray-50 rounded-lg shadow-md max-w-full h-full">
      <Typography variant="h5" className="text-blue-500 font-bold mb-4">
        Upload a PDF
      </Typography>
      <TextField
        type="file"
        onChange={onFileChange}
        fullWidth
        InputProps={{
          inputProps: { accept: "application/pdf" },
        }}
        className="mb-4"
        sx={{
          backgroundColor: "#f9fafb",
          padding: "12px",
          borderRadius: "8px",
        }}
      />
      <Button
        variant="contained"
        startIcon={<CloudUpload />}
        onClick={onFileUpload}
        className="bg-blue-500 hover:bg-blue-600 transition-colors w-full"
        sx={{
          fontSize: "16px",
          padding: "12px",
          textTransform: "none",
        }}
      >
        Upload
      </Button>

      {/* Only show the question form when a document is uploaded */}
      {documentId && userId && (
        <QuestionForm documentId={documentId} userId={userId} />
      )}
    </Box>
  );
};

export default FileUpload;
