from fastapi import FastAPI, File, UploadFile
import os
import shutil
from pathlib import Path

from app.services.stt_google import STT

from dotenv import load_dotenv
load_dotenv()

app=FastAPI()

UPLOAD_DIR=Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/voice")
async def voice(audio: UploadFile=File(...)):
  if audio.filename=="":
    raise HTTPException(status_code=400, details="No file uploaded")
  
  allowed_extensions={".wav", ".mp3", ".m4a"}
  ext=Path(audio.filename).suffix.lower()

  if ext not in allowed_extensions:
    raise HTTPException(status_code="400", details=f"Unsupported file type: {ext}")
  
  save_path=UPLOAD_DIR/audio.filename
  with save_path.open("wb") as buffer:
    shutil.copyfileobj(audio.file, buffer)

  file_size=save_path.stat().st_size
  
  text=STT(save_path)

  return {
    "filename": audio.filename,
    "size": file_size,
    "message": "audio received",
    "transcript": text
  }


@app.get("/health")
def health():
  return {"status":"ok"}