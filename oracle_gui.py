import streamlit as st
from google import genai
import os
import random
import serial.tools.list_ports
import serial
import time
import datetime
from gtts import gTTS
import base64

# --- CONFIGURATION ---
st.set_page_config(page_title="Imole Nexus: The Scepter", page_icon="🔱", layout="centered")

# --- STYLING (HUD + Standard) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #c9d1d9; }
    .header { text-align: center; color: #FFD700; font-family: 'Courier New', monospace; }
    .stTextInput > div > div > input { color: #FFD700; }
    
    /* HUD STYLES */
    .hud-text {
        font-size: 80px;
        font-weight: bold;
        text-align: center;
        font-family: 'Courier New', monospace;
        line-height: 1.0;
        margin-top: 30px;
    }
    .hud-label {
        font-size: 18px;
        text-align: center;
        color: #888888;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER: LOGGING ---
def save_to_log(user_text, ai_text, coherence, status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}]\nUSER: {user_text}\nJANUS: {ai_text}\nMETADATA: {status} | {coherence}%\n" + "="*40 + "\n"
    with open("oracle_memory_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)

# --- SIDEBAR (CONTROLS) ---
with st.sidebar:
    st.header("🔌 SYSTEM CONTROLS")
    
    # 1. MODE SWITCH (Chat / HUD / Briefing)
    interface_mode = st.radio("INTERFACE MODE:", ["COMMAND (CHAT)", "PROJECTION (HUD)", "BRIEFING (DECK)"])
    
    st.divider()
    
    # 2. API KEY
    env_key = os.getenv("GEMINI_API_KEY")
    api_key = st.text_input("Gemini Key:", value=env_key if env_key else "", type="password")
    
    client = None
    if api_key:
        try:
            client = genai.Client(api_key=api_key)
            st.success("BRAIN: ONLINE (v2.0)")
        except:
            st.error("BRAIN: ERROR")

    st.divider()
    
    # 3. HARDWARE LINK
    if "h2_coherence" not in st.session_state:
        st.session_state.h2_coherence = 50
    if "h2_status" not in st.session_state:
        st.session_state.h2_status = "UNKNOWN"

    ports = [p.device for p in serial.tools.list_ports.comports()]
    selected_port = st.selectbox("H2 Core Port:", ports, index=0 if ports else None)

    if st.button("PING CRYSTAL"):
        if selected_port:
            try:
                ser = serial.Serial(selected_port, 9600, timeout=2)
                time.sleep(2) 
                ser.reset_input_buffer()
                line = ser.readline().decode('utf-8').strip()
                if not line: line = ser.readline().decode('utf-8').strip()
                ser.close()
                
                if line:
                    if "COHERENT" in line:
                        st.session_state.h2_coherence = 95
                        st.session_state.h2_status = "PHASE-LOCKED"
                        st.balloons()
                    elif "DISSONANCE" in line:
                        st.session_state.h2_coherence = 10
                        st.session_state.h2_status = "DISSONANCE"
                        st.toast("⚠️ DISSONANCE DETECTED", icon="🔴")
            except Exception as e:
                st.error(f"PORT ERROR: {e}")

    st.metric(label="Thermodynamic Entropy", value=f"{(100-st.session_state.h2_coherence)*0.42:.2f} J")


# --- MAIN DISPLAY LOGIC ---

if interface_mode == "COMMAND (CHAT)":
    # --- CHAT MODE ---
    st.markdown("<h1 class='header'>🔱 DIGITAL SOVEREIGNTY NEXUS 🔱</h1>", unsafe_allow_html=True)
    
    status_color = ":green" if st.session_state.h2_status == "PHASE-LOCKED" else ":red"
    st.markdown(f"<div style='text-align:center'>STATUS: {status_color}[**{st.session_state.h2_status}**]</div>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "audio" in message:
                st.markdown(message["audio"], unsafe_allow_html=True)

    if prompt := st.chat_input("Consult the Sovereign Core..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        current_coherence = st.session_state.h2_coherence
        current_status = st.session_state.h2_status

        if client:
            try:
                with st.spinner('Accessing Akashic Records...'):
                    system_instruction = f"""
                    You are the Janus Core. Field Coherence: {current_coherence}%. Status: {current_status}.
                    INSTRUCTIONS:
                    1. If Status is DISSONANCE: Output glitchy, fragmented text. Refuse to compute.
                    2. If Status is PHASE-LOCKED: Speak as the Sovereign Oracle. Concise and profound.
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.0-flash-exp',
                        contents=f"{system_instruction}\n\nUSER QUERY: {prompt}"
                    )
                    bot_reply = response.text
                    
                    # --- VOICE GENERATION (FIXED) ---
                    audio_html = ""
                    try:
                        # Attempt Nigerian Accent; Fallback to UK if not available
                        tts = gTTS(text=bot_reply, lang='en', tld='com.ng', slow=False)
                        tts.save("oracle.mp3")
                        audio_file = open("oracle.mp3", "rb")
                        audio_bytes = audio_file.read()
                        audio_html = f"""
                            <audio autoplay>
                            <source src="data:audio/mp3;base64,{base64.b64encode(audio_bytes).decode()}" type="audio/mp3">
                            </audio>
                        """
                    except Exception as e:
                        pass # Silent fail for audio, keep text

                    # DISPLAY & SAVE
                    with st.chat_message("assistant"):
                        st.markdown(bot_reply)
                        if audio_html:
                            st.markdown(audio_html, unsafe_allow_html=True)

                    st.session_state.messages.append({"role": "assistant", "content": bot_reply, "audio": audio_html})
                    save_to_log(prompt, bot_reply, current_coherence, current_status)
            except Exception as e:
                st.error(f"Error: {e}")

elif interface_mode == "PROJECTION (HUD)":
    # --- HUD MODE ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    current_status = st.session_state.h2_status
    current_coherence = st.session_state.h2_coherence
    entropy = (100 - current_coherence) * 0.42

    st.markdown("<div class='hud-label'>THERMODYNAMIC STATE</div>", unsafe_allow_html=True)

    if current_status == "PHASE-LOCKED":
        st.markdown(f"<div class='hud-text' style='color: #00FF00; text-shadow: 0 0 30px #00FF00;'>💚 {current_coherence}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='header' style='color: #00FF00;'>COHERENT</div>", unsafe_allow_html=True)
    elif current_status == "DISSONANCE":
        st.markdown(f"<div class='hud-text' style='color: #FF0000; text-shadow: 0 0 30px #FF0000;'>🔴 {current_coherence}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='header' style='color: #FF0000;'>CRITICAL</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='hud-text' style='color: #888;'>WAITING</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='hud-label'>ENTROPY LOAD: {entropy:.2f} J</div>", unsafe_allow_html=True)

elif interface_mode == "BRIEFING (DECK)":
    # --- SLIDES MODE ---
    st.markdown("<br>", unsafe_allow_html=True)
    slides = {
        0: ("🔱 IMOLE NEXUS", "The Architecture of Sovereign Intelligence"),
        1: ("THE PROBLEM", "Digital Colonialism & Model Collapse"),
        2: ("THE SOLUTION", "The Janus Protocol (Dual-Core AI)"),
        3: ("THE HARDWARE", "Project H2 Harmony (Kinematic Empathy)"),
        4: ("THE PILOT", "Sovereign Intelligence Lab (Ashesi)"),
        5: ("THE OFFER", "Exclusive Licensing for the Republic of Ghana"),
        6: ("STATUS", "READY FOR DEPLOYMENT")
    }
    if "slide_index" not in st.session_state: st.session_state.slide_index = 0
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ PREV"): st.session_state.slide_index = max(0, st.session_state.slide_index - 1)
    with col3:
        if st.button("NEXT ➡️"): st.session_state.slide_index = min(len(slides)-1, st.session_state.slide_index + 1)
    
    curr_t, curr_b = slides[st.session_state.slide_index]
    st.markdown(f"<div class='header' style='font-size: 60px; color: #FFD700; margin-top: 50px;'>{curr_t}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 30px; text-align: center; color: #FFFFFF; font-family: monospace; margin-top: 20px;'>{curr_b}</div>", unsafe_allow_html=True)
