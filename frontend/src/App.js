// src/App.js
import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Login from "./components/Login";
import Signup from "./components/Signup";
import FileUpload from "./components/FileUpload";
import Answer from "./components/Answer";
import Welcome from "./components/Welcome";
import Footer from "./components/Footer"; // Import Footer

const App = () => {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [documentId, setDocumentId] = useState(null);

  return (
    <div className="bg-gray-100 min-h-screen">
      <Header token={token} setToken={setToken} setDocumentId={setDocumentId} />

      <main className="py-10">
        <Routes>
          <Route path="/" element={<Welcome isLoggedIn={!!token} />} />
          <Route path="/login" element={<Login setToken={setToken} />} />
          <Route path="/signup" element={<Signup />} />
          <Route
            path="/upload"
            element={<FileUpload setDocumentId={setDocumentId} />}
          />
          <Route path="/answer" element={<Answer documentId={documentId} />} />
        </Routes>
      </main>

      <Footer />
    </div>
  );
};

export default App;
