from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Exam Revision AI Backend is running!"
    }