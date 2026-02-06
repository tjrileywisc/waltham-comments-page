import { useEffect, useState } from "react";

function TranscriptDisplay({ videoId, currentTime }) {
  const [segments, setSegments] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (videoId == null) return;

    async function loadTranscript() {
      try {
        const res = await fetch(`/transcript/${videoId}`);
        if(!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }
        const data = await res.json();
        setSegments(data);
      } catch (err) {
        setError(err.message);
      }
    }

    loadTranscript();
  }, [videoId]);

  if (error) return <p>Error loading transcript</p>;
  if (!segments.length) return null;

  const active = segments.find(
    seg => currentTime >= seg.start && currentTime <= seg.end
  );

  if (!active) return null;

  return (
    <div className="transcript-line">
      <strong>{active.speaker}</strong>: {active.text}
    </div>
  );
}

export default TranscriptDisplay;
