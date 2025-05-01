import streamlit as st
import streamlit.components.v1 as components
import librosa
import numpy as np
import joblib


st.set_page_config(
    page_title="Alexis Honors Project",
    page_icon="🎵",
    layout="centered",
)

# ====== TITLE AND STYLE ======
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(to bottom, #5d37a4 -10%, #1A123C);
    background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("🎶 Feel the Music: AI Emotion Detection 🎶")
st.caption("Take a look at music's feeling through AI!")

st.markdown("---")
st.subheader("🎶Record your own song!")
st.caption("You can record your own song and then upload it for AI analysis.")




# ====== RECORDING AUDIO ======
components.html(
    """
    <style>
    .custom-button {
        background-color: #131720;
        color: white;
        padding: 0.25rem 0.75rem;
        min-height: 2.5rem;
        border: 1px solid transparent;
        border-radius: 0.5rem;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 10px;
        width: 12rem;
    }
    .custom-button:hover {
        color: #FF4B4B;
        border: 1px solid #FF4B4B;
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 20px;
    }
    #listening-text {
        display: none;
        color: #FF4B4B;
    }
    #listening-text > div:first-child {
        animation: blink 1.5s infinite;

    }
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }
    .Upper-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        font-family: 'Segoe UI', sans-serif;
        background-color: #31323F;
        border-radius: 0.4rem;
        padding: 0.5rem;
    }
    #record-text {
        margin-right: 1rem;
    }
    </style>



    <div class="Upper-container" onclick="toggleRecording()">
        <button id="recordBtn" class="custom-button" onclick="toggleRecording()">
            🎤 Capture Audio
        </button>

        <div id="record-text">
            <div style="color: #CCCCCC; font-size: 1rem;">Record any sound you want</div>
            <div style="color: #888888; font-size: 0.85rem;">It's not granted full precision</div>
        </div>
        <div id="listening-text">
            <div style="color: #CCCCCC; font-size: 1rem;">🎧 Listening very carefully...</div>
            <div id="timer-text" style="color: #888888; font-size: 0.85rem;"></div>
        </div>
        
    </div>
    
    <script>
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    let timerInterval;
    let secondsLeft = 15;

    function toggleRecording() {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    }

    function startRecording() {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                document.getElementById("listening-text").style.display = "block";
                document.getElementById("timer-text").style.display = "block";
                document.getElementById("record-text").style.display = "none";
                document.getElementById("recordBtn").innerText = "Press to Stop 🎤";

                secondsLeft = 15;
                document.getElementById("timer-text").innerText = "Please record for at least: " + secondsLeft;

                // COUNTDOWN TIMER
                timerInterval = setInterval(() => {
                    secondsLeft--;
                    if (secondsLeft >= 0) {
                        document.getElementById("timer-text").innerText = "Please record for at least: " + secondsLeft;
                    }
                    if (secondsLeft <= 0) {
                        clearInterval(timerInterval);
                        document.getElementById("timer-text").style.display = "none";
                    }
                }, 1000);

                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.addEventListener("dataavailable", event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.start();
                isRecording = true;
            })
            .catch(error => {
                alert("Error accessing microphone: " + error);
            });
    }

    function stopRecording() {
        if (mediaRecorder && isRecording) {
            mediaRecorder.stop();
            clearInterval(timerInterval);
            document.getElementById("listening-text").style.display = "none";
            document.getElementById("timer-text").style.display = "none";
            document.getElementById("record-text").style.display = "block";
            document.getElementById("recordBtn").innerText = "🎤 Capture Audio 🎤";
            isRecording = false;

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                const audioUrl = URL.createObjectURL(audioBlob);

                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = audioUrl;
                a.download = 'recording.wav';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(audioUrl);
            });
        }
    }

    // HANDLE FILE UPLOAD AND PLAY THE AUDIO
    function handleFileUpload(input) {
        const file = input.files[0];
        if (!file) return;

        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const reader = new FileReader();

        reader.onload = function(e) {
            const arrayBuffer = e.target.result;

            audioContext.decodeAudioData(arrayBuffer, function(buffer) {
                const source = audioContext.createBufferSource();
                source.buffer = buffer;

                const gainNode = audioContext.createGain();

                const now = audioContext.currentTime;
                const duration = 15;

                // Fade in (4 SECS)
                gainNode.gain.setValueAtTime(0, now);
                gainNode.gain.linearRampToValueAtTime(1, now + 4);

                // Fade out (5 SECS)
                gainNode.gain.setValueAtTime(1, now + duration - 5);
                gainNode.gain.linearRampToValueAtTime(0, now + duration);

                source.connect(gainNode).connect(audioContext.destination);
                source.start(0);
                source.stop(audioContext.currentTime + duration);

            }, function(error) {
                alert("Could not decode audio: " + error);
            });
        };

        reader.readAsArrayBuffer(file);
    }
    </script>
    """,
    height = 100,
)


st.markdown("---")
st.subheader("🎧 Upload your song for AI analysis")

uploaded_file = st.file_uploader("📂 Choose your file (.mp3 or .wav)", type=["mp3", "wav"])

if uploaded_file is not None:
    audio_bytes = uploaded_file.read()


    @st.cache_resource
    def load_model():
        return joblib.load('music_emotion_model.pkl')

    model = load_model()

    import base64

    audio_base64 = base64.b64encode(audio_bytes).decode()

    components.html(f"""
    <audio id="audioPlayer" style="display:none;" controls>
        <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
    </audio>

    <script>
    const audio = document.getElementById('audioPlayer');
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    let source, gainNode;

    fetch(audio.querySelector('source').src)
        .then(response => response.arrayBuffer())
        .then(arrayBuffer => audioContext.decodeAudioData(arrayBuffer))
        .then(buffer => {{
            source = audioContext.createBufferSource();
            source.buffer = buffer;

            gainNode = audioContext.createGain();
            source.connect(gainNode).connect(audioContext.destination);

            const now = audioContext.currentTime;
            const duration = 15;

            gainNode.gain.setValueAtTime(0, now);
            gainNode.gain.linearRampToValueAtTime(1, now + 3); // Fade in
            gainNode.gain.setValueAtTime(1, now + duration - 5);
            gainNode.gain.linearRampToValueAtTime(0, now + duration); // Fade out

            source.start(0);
            source.stop(audioContext.currentTime + duration);
        }});
    </script>
    """, height=0)

    def extract_features_from_y(y, sr):
        mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20), axis=1)
        chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1)
        spec_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
        zero_crossings = float(np.mean(librosa.feature.zero_crossing_rate(y)))
        rms = float(np.mean(librosa.feature.rms(y=y)))
        rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))
        bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo = float(tempo)

        chroma_cq = librosa.feature.chroma_cqt(y=y, sr=sr)
        key_idx = int(np.argmax(np.mean(chroma_cq, axis=1)))

        feature_array = np.hstack((
            mfccs,
            chroma,
            np.array([spec_centroid, zero_crossings, rms, rolloff, bandwidth, tempo, key_idx])
        )).reshape(1, -1)

        readable_features = {
            "Tempo": f"{tempo:.1f} BPM",
            "Chroma Richness": f"{np.mean(chroma):.3f}",
            "Spectral Centroid": f"{spec_centroid:.1f} Hz",
            "Zero Crossing Rate": f"{zero_crossings:.4f}",
            "RMS Energy": f"{rms:.4f}",
            "Spectral Rolloff": f"{rolloff:.1f} Hz",
            "Spectral Bandwidth": f"{bandwidth:.1f} Hz",
            "Key Index": key_idx
        }

        return feature_array, readable_features

    try:
        import io

        y, sr = librosa.load(io.BytesIO(audio_bytes), duration=30, sr=None)

        # AI ANALYSIS
        features_array, readable_features = extract_features_from_y(y, sr)
        prediction = model.predict(features_array)[0]

        st.subheader("🎵 Detected Emotion:")
        st.success(f"**{prediction}**")

        st.subheader("Analysis Details")

        with st.expander("📊 Show Technical and Public Details 📊"):
            st.markdown("**Technical Features & Public Explanation:**")
            st.markdown(f"- **Tempo (Speed of the song):** {readable_features['Tempo']}")
            st.markdown(f"- **Chroma Richness (Musical note spread):** {readable_features['Chroma Richness']}")
            st.markdown(f"- **Spectral Centroid (Brightness):** {readable_features['Spectral Centroid']}")
            st.markdown(f"- **Zero Crossing Rate (Vibration):** {readable_features['Zero Crossing Rate']}")
            st.markdown(f"- **RMS Energy (Intensity):** {readable_features['RMS Energy']}")
            st.markdown(f"- **Spectral Rolloff (Edge of energy):** {readable_features['Spectral Rolloff']}")
            st.markdown(f"- **Spectral Bandwidth (Width of sound):** {readable_features['Spectral Bandwidth']}")
            st.markdown(f"- **Key Detection (Dominant tone):** {readable_features['Key Index']}")

        

    except Exception as e:
        st.error(f"Error analyzing the file: {e}")

# ========== FOOTER ==========
st.markdown("---")
st.caption("Developed by Alexis Rojas for the Sinclair Honors Project Symposium 2025 🎵")