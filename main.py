from fastapi import FastAPI, HTTPException, Request, logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse

import os
import pathlib
import csv
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

@app.get("/transcript/{video_id}")
def get_transcript(video_id: int):
    name = VIDEO_DB[video_id]["name"]
    
    path = f"{os.environ['TRANSCRIPTION_DIR']}/{name}.csv"
    
    if not path or not os.path.exists(path):
        logger.logger.error(f"can't find {path}")
        raise HTTPException(404)
    
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return [
            {
                "id": int(row["id"]),
                "start": float(row["start"]),
                "end": float(row["end"]),
                "text": row["text"],
                "speaker": row["speaker"],
            }
            for row in reader
        ]

@app.get("/video/{video_id}")
def get_video(video_id: int, request: Request):
    path = os.environ['VIDEO_DIR'] + "/" + VIDEO_DB[video_id]["name"] + ".mp4"
    if not path or not os.path.exists(path):
        raise HTTPException(404)

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

    files = [file.replace(".mp4", "").rsplit("/")[-1] for file in files]
    
    VIDEO_DB = [
        {"video_id": i, "name": path}
        for i, path in enumerate(files)
    ]
    return VIDEO_DB

@app.get("/transcriptions/{video_id}")
def get_video_transcription(video_id: str) -> Path:
    return pathlib.Path(os.environ["TRANSCRIPTION_DIR"]) / video_id
