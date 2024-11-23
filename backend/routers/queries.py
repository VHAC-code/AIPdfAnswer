from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from models import Document, Question, User
from database import get_db
from auth import get_current_user
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("routers.queries")

router = APIRouter(prefix="/queries", tags=["Queries"])

# Initialize SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize GPT-2 model and tokenizer from Hugging Face
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")

# Add padding token for GPT-2 compatibility
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token  # Use eos_token as pad_token if not defined

# Normalize and preprocess text
def preprocess_and_split(text, chunk_size=200):
    text = re.sub(r"[^\w\s,.]", "", text)  # Keep punctuation
    text = re.sub(r"\s+", " ", text).strip()  # Normalize whitespace
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Build FAISS index with cosine similarity
def build_faiss_index(chunks):
    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)  # Normalize

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Use cosine similarity
    index.add(embeddings)

    return index, chunks

# Generate an answer with GPT-2 from Hugging Face
def generate_answer(question, index, chunks, full_text, max_chunks=3, relevance_threshold=0.5):
    try:
        logger.info("Starting FAISS retrieval and GPT-2 generation...")

        # Step 1: Retrieve relevant chunks
        question_embedding = model.encode([question]).astype("float32")
        question_embedding = question_embedding / np.linalg.norm(question_embedding)

        distances, indices = index.search(question_embedding, k=max_chunks)
        relevant_chunks = [
            chunks[idx] for idx, distance in zip(indices[0], distances[0])
            if idx < len(chunks) and distance >= relevance_threshold
        ]

        # Step 2: Decide the context for GPT-2
        if relevant_chunks:
            logger.info("Relevant context found for the question.")
            context = " ".join(relevant_chunks[:max_chunks])
            input_text = (
                f"The following is an excerpt from a document:\n\n{context}\n\n"
                f"Question: {question}\n\nAnswer:"
            )
        else:
            logger.warning("No relevant chunks found. Using general context.")
            input_text = (
                f"The document provided the following content:\n\n{full_text[:1000]}...\n\n"
                f"Question: {question}\n\nAnswer:"
            )

        # Step 3: Tokenize input and generate response
        inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=500)
        output = gpt2_model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=150,
            num_return_sequences=1,
            no_repeat_ngram_size=3,
            temperature=0.6,
            top_p=0.9,
            top_k=50,
            do_sample=True,
            early_stopping=True,
        )

        # Step 4: Clean up the answer
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        if "Answer:" in generated_text:
            answer = generated_text.split("Answer:")[1].strip()
        else:
            answer = generated_text.strip()

        logger.info(f"Generated Answer: {answer}")
        return answer

    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return "Error generating a detailed answer."

@router.post("/ask")
async def ask_question(
    document_id: int = Body(...),
    question: str = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Fetch document and validate ownership
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id,
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found or not owned by the user")

    document_content = document.meta_info
    if not document_content:
        raise HTTPException(status_code=404, detail="Document content not available")

    # Preprocess and split `meta_info` into chunks
    document_chunks = preprocess_and_split(document_content)

    # Build FAISS index
    try:
        index, chunks = build_faiss_index(document_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building FAISS index: {str(e)}")

    # Query the FAISS index and generate an answer
    try:
        answer = generate_answer(question, index, document_chunks, document_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")

    # Save the question and answer in the database
    try:
        new_question = Question(
            user_id=current_user.id,
            document_id=document_id,
            question=question,
            answer=answer,
        )
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving question: {str(e)}")

    return {
        "message": "Question answered successfully",
        "question": question,
        "answer": answer,
    }
