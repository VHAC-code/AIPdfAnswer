# from langchain.llms import OpenAI
# from langchain.document_loaders import PyPDFLoader
# from database import SessionLocal
# from models import Document
# from routers import queries
# from backend import file_utils

# from langchain.llms import OpenAI

# def process_query(document_id: int, question: str):
#     """
#     Processes a query by fetching a document, running FAISS, and querying OpenAI.
#     """
#     db = SessionLocal()
#     try:
#         # Fetch the document from the database
#         document = db.query(Document).filter(Document.id == document_id).first()
#         if not document:
#             print(f"Document with ID {document_id} not found in the database.")
#             return "Document not found."

#         # Extract text from the PDF
#         document_text = file_utils.extract_text_from_pdf(document.file_path)
#         if not document_text:
#             print(f"Failed to extract text from document at path: {document.file_path}")
#             return "Failed to extract text from the document."

#         # Build FAISS index
#         try:
#             documents = [document_text]  # For now, single document
#             index, embeddings = queries.build_faiss_index(documents)
#         except Exception as e:
#             print(f"Error building FAISS index: {e}")
#             return "Error building FAISS index."

#         # Query FAISS
#         try:
#             relevant_text = queries.generate_answer(question, index, embeddings, documents)
#             if relevant_text == "No relevant answer found.":
#                 return relevant_text
#         except Exception as e:
#             print(f"Error querying FAISS index: {e}")
#             return "Error querying FAISS index."

#         # Use OpenAI to generate a more detailed response
#         llm = OpenAI(model="text-davinci-003", temperature=0)
#         response = llm(f"Answer the question based on this text:\n\n{relevant_text}\n\nQuestion: {question}")

#         return response
#     except Exception as e:
#         print(f"Error processing the query: {e}")
#         return f"Error processing the query: {str(e)}"
#     finally:
#         db.close()




from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from database import SessionLocal
from models import Document
from routers.queries import split_text, build_faiss_index, generate_answer

def process_query(document_id: int, question: str):
    """
    Processes a query by fetching a document, running FAISS, and querying OpenAI.
    """
    db = SessionLocal()
    try:
        # Fetch the document from the database
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            print(f"Document with ID {document_id} not found in the database.")
            return "Document not found."

        # Extract text from the document
        document_content = document.meta_info
        if not document_content:
            print(f"No content found for document ID {document_id}.")
            return "No content available for the document."

        # Split text into chunks and build FAISS index
        try:
            chunks = split_text(document_content)
            index, _ = build_faiss_index(chunks)
        except Exception as e:
            print(f"Error building FAISS index: {e}")
            return "Error building FAISS index."

        # Query FAISS to find the most relevant text chunk
        try:
            relevant_text = generate_answer(question, index, chunks)
            if relevant_text == "No relevant answer found.":
                return relevant_text
        except Exception as e:
            print(f"Error querying FAISS index: {e}")
            return "Error querying FAISS index."

        # Use OpenAI to generate a more detailed response
        llm = OpenAI(model="text-davinci-003", temperature=0)
        response = llm(f"Use the following text to answer the question:\n\n{relevant_text}\n\nQuestion: {question}")
        return response
    except Exception as e:
        print(f"Error processing the query: {e}")
        return f"Error processing the query: {str(e)}"
    finally:
        db.close()
