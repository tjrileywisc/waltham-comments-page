
import { useState } from "react";

import VideoPlayer from "./VideoPlayer";
import VideoList from "./VideoList";
import "./styles.css";

function App() {

  const [videoId, setVideoId] = useState(null);

  return (
    <div className="app-container">
      <div className="left-pane">
        <VideoPlayer videoId={videoId} />
      </div>

      <div className="right-pane">
        <VideoList onSelectVideo={setVideoId} />
      </div>
    </div>
  );
}

export default App;