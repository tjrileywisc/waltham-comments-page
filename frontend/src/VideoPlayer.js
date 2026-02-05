
import { useRef } from "react";

async function getVideos() {
    await fetch("./")
}

function VideoPlayer({videoId}) {
    const videoRef = useRef(null);

    return (
        <video
            ref={videoRef}
            src="/video.mp4"
            controls
            width="800"
            height="800"
        />
    );
}

export default VideoPlayer;