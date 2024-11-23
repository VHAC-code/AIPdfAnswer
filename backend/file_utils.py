import os
import pdfplumber

# Directory to save uploaded files
UPLOAD_DIRECTORY = "uploads"

# Ensure the directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

async def save_file(upload_file, filename: str) -> str:
    """
    Save the uploaded file to the upload directory.
    Args:
        upload_file: The file object to save.
        filename (str): Name of the file to save.
    Returns:
        str: The path to the saved file.
    """
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    
    try:
        with open(file_path, "wb") as f:
            f.write(await upload_file.read())  # Save the uploaded file contents
    except Exception as e:
        raise ValueError(f"Error while saving the file: {e}")

    return file_path

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file using pdfplumber.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")

    try:
        with pdfplumber.open(file_path) as pdf:
            extracted_text = " ".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")

    return extracted_text.strip()

