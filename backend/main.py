import shutil
import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import Document, Question
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.chains import load_qa_chain
from langchain_community.llms import OpenAI
from auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from routers import documents,queries  # Import the documents router
from routers.queries import preprocess_and_split, build_faiss_index, generate_answer
app = FastAPI()

# Include the auth router to register its routes (e.g., register, login, etc.)
app.include_router(auth_router, prefix="/auth", tags=["auth"])


# Include the documents router (this will include /documents/upload and any other routes in documents.py)
app.include_router(documents.router)  # Make sure to import and include this router

app.include_router(queries.router)  # Include the queries router

# Ensure the upload directory exists
upload_dir = "uploads"
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# File upload endpoint
@app.post("/upload/")  # This route should work, ensure you're hitting the correct endpoint in Postman
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Save the uploaded file locally
        file_path = os.path.join(upload_dir, file.filename)
        print(f"Saving file to: {file_path}")  # Debugging line

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Save file metadata to the database
        doc = Document(user_id=current_user["id"], file_path=file_path, metadata="Uploaded document")
        db.add(doc)
        db.commit()

        return {"message": "File uploaded successfully!", "file_path": file_path}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

# Ensure proper CORS handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing, restrict to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Ask question endpoint
# @app.post("/ask/")
# async def ask_question(
#     question: str,
#     document_id: int,
#     current_user: dict = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Fetch the document
#         document = db.query(Document).filter(
#             Document.id == document_id, 
#             Document.user_id == current_user["id"]
#         ).first()

#         if not document:
#             print(f"Document {document_id} not found or unauthorized access for user {current_user['id']}")
#             raise HTTPException(status_code=404, detail="Document not found or unauthorized access")

#         # Load document content
#         loader = PyPDFLoader(document.file_path)
#         docs = loader.load()

#         # Process the question using LangChain
#         chain = load_qa_chain(OpenAI(temperature=0))
#         answer = chain.run(input_documents=docs, question=question)

#         # Save the question and answer
#         new_question = Question(
#             user_id=current_user["id"],
#             document_id=document.id,
#             question=question,
#             answer=answer
#         )
#         db.add(new_question)
#         db.commit()

#         return {"question": question, "answer": answer}
#     except Exception as e:
#         print(f"Error in ask_question endpoint: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")



@app.post("/ask/")
async def ask_question(
    question: str,
    document_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Fetch the document
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == current_user["id"]
        ).first()

        if not document:
            raise HTTPException(status_code=404, detail="Document not found or unauthorized access")

        # Extract content from the document (use meta_info instead of PDF path if available)
        document_content = document.meta_info
        if not document_content:
            raise HTTPException(status_code=404, detail="Document content not available")

        # Split the content into chunks
        chunks = preprocess_and_split(document_content)

        # Build FAISS index
        index, chunk_list = build_faiss_index(chunks)

        # Generate answer using FAISS
        faiss_answer = generate_answer(question, index, chunk_list)

        # If FAISS provides no relevant answer, fallback to GPT-based answer
        if faiss_answer == "No relevant answer found.":
            print("Fallback to GPT model for answer generation")
            llm = OpenAI(model="text-davinci-003", temperature=0)
            gpt_answer = llm(f"Answer the question based on this context:\n\n{document_content}\n\nQuestion: {question}")
            final_answer = gpt_answer.strip()
        else:
            final_answer = faiss_answer

        # Save the question and answer to the database
        new_question = Question(
            user_id=current_user["id"],
            document_id=document_id,
            question=question,
            answer=final_answer
        )
        db.add(new_question)
        db.commit()

        return {"question": question, "answer": final_answer}

    except Exception as e:
        print(f"Error in ask_question endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")
