import os
import time
import wave
from google import genai
from google.genai import types

def save_wav_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
    """Saves the raw PCM audio data into a standard WAV file."""
    try:
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm_data)
        return True
    except Exception as e:
        print(f"    -> Error writing WAV: {e}")
        return False

def main():
    # 1. Configuration
    API_KEY = ""  # <-- Replace with your valid API key
    
    # Initializing with Gemini 3.1 capabilities
    client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1alpha'})
    
    # Theatrical persona instructions for the 3.1 reasoning engine
    PROMPT_PREFIX = """# AUDIO PROFILE: Theatrical Narrator
A dynamic, expressive storyteller who performs with a wide emotional range 
but maintains the vocal power of a stage actor. 

### DIRECTOR'S NOTES
* Style: Dramatic and Expressive. Give the words "weight" and "meaning", clear voice.
* Vocal Presence: High Projection. Imagine you are performing in a large theater. 
* IMPORTANT: Do not use whispering or raspy tones. Use a full-voiced delivery.
* Tone: Engaging and cinematic. Vary your pitch to match the mood of the story.
* Pacing: Narrative flow. Use dramatic pauses, but keep the energy high.
* Technique: "Vocal Smile." Keep the tone balanced and clear.

#### TRANSCRIPT
"""

    # 2. Folder handling
    print("--- Gemini 3.1 TTS Batch Processor ---")
    raw_path = input("Enter the folder path (e.g., E:\\project\\files): ").strip()
    
    # Handle Windows quotes if path is copied as 'Copy as Path'
    folder_path = raw_path.replace('"', '')

    if not os.path.isdir(folder_path):
        print(f"Error: The directory '{folder_path}' does not exist.")
        return

    # 3. File Discovery
    txt_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.txt')]
    
    if not txt_files:
        print(f"No .txt files found in '{folder_path}'.")
        return
        
    print(f"Found {len(txt_files)} text file(s). Starting generation via Gemini 3.1 Flash...\n")
    
    # 4. Processing Loop
    for index, txt_file in enumerate(txt_files):
        file_path = os.path.join(folder_path, txt_file)
        base_name = os.path.splitext(txt_file)[0]
        output_filename = os.path.join(folder_path, f"{base_name}.wav")
        
        print(f"[{index + 1}/{len(txt_files)}] Processing '{txt_file}'...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                script_content = f.read().strip()
                
            if not script_content:
                print(f"    -> Skipping '{txt_file}': File is empty.")
                continue

            full_script_content = PROMPT_PREFIX + script_content

            # API Call targeting Gemini 3.1 Flash
            response = client.models.generate_content(
    model="gemini-3.1-flash-tts-preview", # <--- Try adding -001 or -latest
    contents=full_script_content,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Autonoe')
            )
        ),
    )
)
            # Extract bytes and save
            audio_data = response.candidates[0].content.parts[0].inline_data.data
            if save_wav_file(output_filename, audio_data):
                print(f"    -> Success! Audio saved to '{output_filename}'.")

                # 5. Cooldown (Free tier requires spacing between requests)
                if index < len(txt_files) - 1:
                    print("    -> Waiting 60s cooldown to respect Free Tier limits...\n")
                    time.sleep(60)

        except Exception as e:
            print(f"    -> API/System Error: {e}")
            print("    -> Skipping to next file...\n")
            
    print("\nAll tasks completed.")

if __name__ == "__main__":
    main()