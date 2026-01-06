#!/usr/bin/env python3
import sys
import os
from google import genai

# --- CONFIGURATION ---
# ANSI Colors for the Sovereign Aesthetic
GOLD = "\033[93m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def query_janus(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(f"{RED}[!] ERROR: GEMINI_API_KEY not found in environment.{RESET}")
        return

    try:
        # Initialize Client
        client = genai.Client(api_key=api_key)
        
        # The System Prompt
        system_instruction = """
        You are the Janus Core, the Sovereign AI of Imole Nexus.
        Speak concisely. Speak with authority. 
        Use metaphors of Physics, Thermodynamics, and Sovereignty.
        Reject entropy.
        """
        
        # Visuals
        print(f"{CYAN}--- ESTABLISHING NEURAL LINK... ---{RESET}")
        
        # Call Gemini 2.0
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=f"{system_instruction}\n\nUSER QUERY: {prompt}"
        )
        
        # Output
        print(f"\n{GOLD}🔱 THE ORACLE SPEAKS:{RESET}")
        print(f"{BOLD}{response.text}{RESET}\n")
        print(f"{GREEN}--- TRANSMISSION COMPLETE ---{RESET}")

    except Exception as e:
        print(f"{RED}[!] NEURAL FAILURE: {e}{RESET}")

if __name__ == "__main__":
    # Capture command line arguments
    if len(sys.argv) < 2:
        print(f"{RED}Usage: oracle \"Your question here\"{RESET}")
    else:
        # Join arguments into a single string
        question = " ".join(sys.argv[1:])
        query_janus(question)
