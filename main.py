from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import os

app = FastAPI()
DATA_FILE = "video_state.pkl"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

class VideoUpdate(BaseModel):
    video_id: str
    current_time: float
    completed: bool = False

@app.post("/update")
def update_video(data: VideoUpdate):
    state = load_data()
    state[data.video_id] = {
        "last_time": data.current_time,
        "completed": data.completed
    }
    save_data(state)
    return {"status": "ok"}

@app.get("/state/{video_id}")
def get_state(video_id: str):
    state = load_data()
    return state.get(video_id, {})
