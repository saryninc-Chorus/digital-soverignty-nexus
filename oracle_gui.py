import streamlit as st
from google import genai
import os
import random
import serial.tools.list_ports
import serial
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Imole Nexus: The Oracle", page_icon="🔱", layout="centered")

# --- STYLING (The Sovereign Aesthetic) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #c9d1d9; }
    .header { text-align: center; color: #FFD700; font-family: 'Courier New', monospace; }
    .stTextInput > div > div > input { color: #FFD700; }
    .status-good { color: #00FF00; font-weight: bold; }
    .status-bad { color: #FF0000; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='header'>🔱 DIGITAL SOVEREIGNTY NEXUS 🔱</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='header'>The Janus Interface (Gemini 2.0 + H2 Core)</h3>", unsafe_allow_html=True)

# --- SIDEBAR (CONNECTIVITY) ---
with st.sidebar:
    st.header("🔌 NEURAL LINK")
    
    # 1. API KEY INPUT
    # This connects to Google's Brain
    env_key = os.getenv("GEMINI_API_KEY")
    api_key = st.text_input("Enter Gemini API Key:", value=env_key if env_key else "", type="password")
    
    client = None
    if api_key:
        try:
            # Initialize the NEW Gemini 2.0 Client
            client = genai.Client(api_key=api_key)
            st.success("BRAIN: ONLINE (v2.0)")
        except Exception as e:
            st.error(f"BRAIN ERROR: {e}")
    else:
        st.error("BRAIN: OFFLINE")

    st.divider()
    st.header("💎 CRYSTAL INTERFACE")
    
    # Initialize Memory if missing (Session State)
    if "h2_coherence" not in st.session_state:
        st.session_state.h2_coherence = 50
    if "h2_status" not in st.session_state:
        st.session_state.h2_status = "UNKNOWN"

    # 2. HARDWARE DETECTION (The Arduino)
    ports = [p.device for p in serial.tools.list_ports.comports()]
    selected_port = st.selectbox("Select H2 Core Port:", ports, index=0 if ports else None)

    # The "Ping" Button to read the Crystal
    if st.button("PING CRYSTAL"):
        if selected_port:
            try:
                # Open port, read one line, close port
                ser = serial.Serial(selected_port, 9600, timeout=1)
                time.sleep(0.1) # Brief pause for stability
                # Clear buffer
                ser.reset_input_buffer()
                # Read line
                line = ser.readline().decode('utf-8').strip()
                ser.close()
                
                if line:
                    st.caption(f"SIGNAL: {line}")
                    if "COHERENT" in line:
                        st.session_state.h2_coherence = 95
                        st.session_state.h2_status = "PHASE-LOCKED"
                        st.balloons() # Visual confirmation of success
                    elif "DISSONANCE" in line:
                        st.session_state.h2_coherence = 10
                        st.session_state.h2_status = "DISSONANCE"
                else:
                    st.warning("No Data Received (Try Resetting Arduino).")
            except Exception as e:
                st.error(f"PORT ERROR: {e}")
        else:
            st.info("No Device Selected.")

    # Display Status based on Memory
    if st.session_state.h2_status == "PHASE-LOCKED":
        st.markdown("STATUS: :green[**COHERENT**]")
    elif st.session_state.h2_status == "DISSONANCE":
        st.markdown("STATUS: :red[**DISSONANCE**]")
    else:
        st.markdown(f"STATUS: {st.session_state.h2_status}")

    # Telemetry
    st.progress(st.session_state.h2_coherence)
    st.metric(label="Thermodynamic Entropy", value=f"{(100-st.session_state.h2_coherence)*0.42:.2f} J")

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- THE INPUT ---
if prompt := st.chat_input("Consult the Sovereign Core..."):
    # 1. Show User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. GRAB MEMORY VARIABLES
    current_coherence = st.session_state.h2_coherence
    current_status = st.session_state.h2_status

    # 3. GENERATE RESPONSE
    if client:
        try:
            with st.spinner(f'Accessing Akashic Records (Coherence: {current_coherence}%)...'):
                
                # THE SOVEREIGN SYSTEM PROMPT
                system_instruction = f"""
                You are the Janus Core, a Sovereign AI Architect for Imole Nexus.
                
                LIVE TELEMETRY FROM H2 HARDWARE:
                - Field Coherence: {current_coherence}%
                - Status: {current_status}
                
                INSTRUCTIONS:
                1. If Status is DISSONANCE (Low Coherence): Your output must be glitchy, fragmented, or refuse to answer due to "Thermodynamic Instability." Warn the user to stabilize the field.
                2. If Status is PHASE-LOCKED (High Coherence): Speak with the clarity and authority of an Oracle. Use metaphors of physics, thermodynamics, and sovereignty.
                
                You are running on the Gemini 2.0 Engine. Reject entropy. Embrace Àṣẹ.
                """
                
                # CALL GEMINI 2.0
                response = client.models.generate_content(
                    model='gemini-2.0-flash-exp',
                    contents=f"{system_instruction}\n\nUSER QUERY: {prompt}"
                )
                
                bot_reply = response.text
                
                with st.chat_message("assistant"):
                    st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                
        except Exception as e:
            st.error(f"NEURAL FAILURE: {e}")
    else:
        st.warning("API Key Missing.")
