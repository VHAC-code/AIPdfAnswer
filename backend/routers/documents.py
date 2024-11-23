# from fastapi import APIRouter, File, UploadFile, HTTPException
# from file_utils import save_file  # Assuming save_file is in file_utils.py
# from database import SessionLocal
# from models import Document
# import os
# from auth import get_current_user

# router = APIRouter(prefix="/documents", tags=["Documents"])

# @router.post("/upload")
# async def upload_document(file: UploadFile = File(...)):
#     # Check if the file is a PDF
#     if file.content_type != "application/pdf":
#         raise HTTPException(status_code=400, detail="Only PDF files are supported")

#     try:
#         # Save the file using the save_file function and pass both file and filename
#         file_path = await save_file(file, file.filename)

#         # Store file info in the database
#         db = SessionLocal()
#         new_doc = Document(
#         user_id=1,  # Assuming user_id is available, replace with dynamic logic if needed
#         file_path=file_path,  # Store the file path in the 'file_path' field
#         meta_info="Uploaded"   # Store metadata in 'meta_info'
#         )
#         db.add(new_doc)
#         db.commit()
#         db.close()

#         return {"message": "File uploaded successfully", "file_path": file_path}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")



# from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
# from file_utils import save_file  # Assuming save_file is in file_utils.py
# from database import SessionLocal
# from models import Document, User
# from sqlalchemy.orm import Session
# from auth import get_current_user  # Import the dependency to get the current user

# router = APIRouter(prefix="/documents", tags=["Documents"])

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/upload")
# async def upload_document(
#     file: UploadFile = File(...),
#     current_user: User = Depends(get_current_user),  # Get the authenticated user
#     db: Session = Depends(get_db)  # Use dependency to manage the database session
# ):
#     # Check if the file is a PDF
#     if file.content_type != "application/pdf":
#         raise HTTPException(status_code=400, detail="Only PDF files are supported")

#     try:
#         # Save the file using the save_file function and pass both file and filename
#         file_path = await save_file(file, file.filename)

#         # Store file info in the database
#         new_doc = Document(
#             user_id=current_user.id,  # Dynamically set the user ID from the authenticated user
#             file_path=file_path,  # Store the file path in the 'file_path' field
#             meta_info="Uploaded"   # Store metadata in 'meta_info'
#         )
#         db.add(new_doc)
#         db.commit()
#         db.refresh(new_doc)  # Ensure the new document has been added

#         return {"message": "File uploaded successfully", "file_path": file_path}

#     except Exception as e:
#         db.rollback()  # Rollback the transaction in case of error
#         raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
    
#     finally:
#         db.close()  # Close the session



from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from file_utils import save_file, extract_text_from_pdf  # Assuming these utilities are defined
from database import get_db
from models import Document, User
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from auth import get_current_user
import time
import os

router = APIRouter(prefix="/documents", tags=["Documents"])

# Ensure the uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if the file is a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Save the file to disk
    try:
        file_path = await save_file(file, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Extract text from the PDF for meta_info
    try:
        extracted_text = extract_text_from_pdf(file_path)
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Failed to extract text from the uploaded PDF")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from PDF: {str(e)}")

    # Retry database operations
    retries = 5
    for attempt in range(retries):
        try:
            new_doc = Document(
                user_id=current_user.id,
                file_path=file_path,
                meta_info=extracted_text
            )
            db.add(new_doc)
            db.commit()
            db.refresh(new_doc)

            return {
                "message": "File uploaded successfully",
                 "document_id": new_doc.id,  # Return the document_id
                "user_id": current_user.id,  # Return the user_id (owner of the document)
                "file_path": file_path,
                "meta_info_preview": extracted_text[:200],  # Limit preview to the first 200 characters
            }
        except OperationalError as e:
            db.rollback()  # Proper rollback for failed transaction
            if "database is locked" in str(e):
                print(f"Database is locked. Retrying ({attempt + 1}/{retries})...")
                time.sleep(2)  # Wait before retrying
            else:
                raise HTTPException(status_code=500, detail=f"Database operation failed: {str(e)}")
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
        finally:
            db.close()  # Ensure session is closed for each attempt

    raise HTTPException(status_code=500, detail="Failed to upload file after multiple retries.")
