from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz
import re

app = FastAPI()


# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def clean_text(text):

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces at the beginning and end
    text = text.strip()

    return text


def split_into_chunks(text, chunk_size=2000):

    chunks = []
    start = 0

    while start < len(text):

        end = start + chunk_size

        if end >= len(text):
            chunks.append(text[start:])
            break

        # Find the nearest line break
        split_position = text.rfind("\n", start, end)

        # If no line break is found, use the original position
        if split_position == -1:
            split_position = end

        chunk = text[start:split_position].strip()

        if chunk:
            chunks.append(chunk)

        start = split_position + 1

    return chunks


@app.get("/")
def home():

    return {
        "message": "Exam Revision AI Backend is running!"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    contents = await file.read()

    pdf = fitz.open(stream=contents, filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    text = clean_text(text)

    if not text:

        return {
            "filename": file.filename,
            "message": "No extractable text found in this PDF.",
            "text": ""
        }

    chunks = split_into_chunks(text)

    return {
        "filename": file.filename,
        "message": "PDF uploaded, text cleaned, and split into chunks successfully.",
        "total_characters": len(text),
        "total_chunks": len(chunks),
        "chunks": chunks
    }