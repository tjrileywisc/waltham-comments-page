from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse

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
def get_video(video_id: int, request: Request):
    path = VIDEO_DB[video_id]["path"]
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404)

    file_size = os.path.getsize(path)
    range_header = request.headers.get("range")

    if range_header:
        start, end = range_header.replace("bytes=", "").split("-")
        start = int(start)
        end = int(end) if end else file_size - 1
    else:
        start, end = 0, file_size - 1

    def iterfile():
        with open(path, "rb") as f:
            f.seek(start)
            yield f.read(end - start + 1)

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(end - start + 1),
    }

    return StreamingResponse(
        iterfile(),
        status_code=206 if range_header else 200,
        headers=headers,
        media_type="video/mp4",
    )

@app.get("/videos")
def get_videos():
    global VIDEO_DB

    files = os.listdir(os.environ["VIDEO_DIR"])
    VIDEO_DB = [
        {"video_id": i, "path": f"{os.environ['VIDEO_DIR']}/{path}"}
        for i, path in enumerate(files)
    ]
    return VIDEO_DB

@app.get("/transcriptions/{video_id}")
def get_video_transcription(video_id: str) -> Path:
    return pathlib.Path(os.environ["TRANSCRIPTION_DIR"]) / video_id
