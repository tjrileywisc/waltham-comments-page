
import { useEffect, useState } from "react";

function VideoList() {
    const [speakers, setSpeakers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let cancelled = false;

        async function fetchSpeakers() { 
            try {
                const res = await fetch("./videos");
                if(!res.ok) {
                    throw new Error(`HTTP ${res.status}`);
                }

                const data = await res.json();
                if (!cancelled) {
                    setSpeakers(data)
                }
            } catch (err) {
                if (!cancelled) {
                    setError(err.message);
                }
            } finally {
                if (!cancelled) {
                    setLoading(false);
                }
            }
        }

        fetchSpeakers();

        return () => {
            cancelled = true;
        };
    

    }, []);

    if (loading) return <p>Loading videos...</p>;
    if (error) return <p style={{ color: "red" }}>Error: {error}</p>;

    return (
        <table border="1" cellPadding="8">
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Path</th>
                </tr>
            </thead>
            <tbody>
                {speakers.map((s) => (
                    <tr key={s.video_id}>
                        <td>{s.video_id}</td>
                        <td>{s.path}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default VideoList;