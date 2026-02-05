
import VideoPlayer from "./VideoPlayer";
import VideoList from "./VideoList";
import "./styles.css";

function App() {
  return (
    <div className="app-container">
      <div className="left-pane">
        <VideoPlayer />
      </div>

      <div className="right-pane">
        <VideoList />
      </div>
    </div>
  );
}

export default App;