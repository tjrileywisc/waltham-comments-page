
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pydantic import BaseModel
import pickle
import os
import pathlib
from pathlib import Path

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory="./frontend/build/static"),
    name="static"
)

VIDEO_DB = list()

@app.get("/")
def root():
    return FileResponse("./frontend/build/index.html")

@app.get("/video/{video_id}")
def get_video(video_id: str):
    pass

@app.get("/videos")
def get_videos():
    files = os.listdir(os.environ["VIDEO_DIR"])
    VIDEO_DB = [{"video_id": i, "path": path} for i, path in enumerate(files)]
    return VIDEO_DB

@app.get("/transcriptions/{video_id}")
def get_video_transcription(video_id: str) -> Path:
    return pathlib.Path(os.environ["TRANSCRIPTION_DIR"]) / video_id