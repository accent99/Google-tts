import os
import time
import wave
from google import genai
from google.genai import types

def save_wav_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)

def main():
    # 1. Initialize client using the required v1alpha version for TTS previews
    API_KEY = ""  # <-- Replace with your actual API key
    client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1alpha'})
    
    # Defines the base instructions/persona for the TTS model
    PROMPT_PREFIX = """# AUDIO PROFILE: Theatrical Narrator
A dynamic, expressive storyteller who performs with a wide emotional range 
but maintains the vocal power of a stage actor. 

### DIRECTOR'S NOTES
* Style: Dramatic and Expressive. Give the words "weight" and "meaning", clear voice.
* Vocal Presence: High Projection. Imagine you are performing in a large theater. 
* IMPORTANT: Do not use wispering or raspy tones. Even during high-tension 
  moments, use a full-voiced, resonant delivery.
* Tone: Engaging and cinematic. Vary your pitch to match the mood of the story.
* Pacing: Narrative flow. Use pauses for dramatic effect, but keep the 
  energy of the voice high.
* Technique: "Vocal Smile." Keep the tone balance and clear so it never 
  becomes raspy or dull.

#### TRANSCRIPT
"""

    # 2. Ask user for the folder location
    folder_path = input("Enter the folder path containing the text files: ").strip()
    
    # Validate directory
    if not os.path.isdir(folder_path):
        print(f"Error: The directory '{folder_path}' does not exist.")
        return

    # 3. Find all .txt files in the directory
    txt_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.txt')]
    
    if not txt_files:
        print(f"No .txt files found in '{folder_path}'.")
        return
        
    print(f"Found {len(txt_files)} text file(s) to process. Starting generation...\n")
    
    # 4. Process each file one by one
    for index, txt_file in enumerate(txt_files):
        file_path = os.path.join(folder_path, txt_file)
        
        # Determine the output WAV filename (same name as text file)
        base_name = os.path.splitext(txt_file)[0]
        output_filename = os.path.join(folder_path, f"{base_name}.wav")
        
        print(f"[{index + 1}/{len(txt_files)}] Processing '{txt_file}'...")
        
        try:
            # Read the text file content
            with open(file_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
                
            if not script_content.strip():
                print(f"  -> Skipping '{txt_file}' because it is empty.")
                continue

            # Combine the director's notes with the actual text file content
            full_script_content = PROMPT_PREFIX + script_content

            # API Call to generate TTS
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
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

            audio_data = response.candidates[0].content.parts[0].inline_data.data
            save_wav_file(output_filename, audio_data)
            print(f"  -> Success! Saved audio to '{output_filename}'.")

        except Exception as e:
            print(f"  -> An error occurred while processing '{txt_file}': {e}")
            
        # 5. Apply the 1-minute cooldown if this is not the last file
        if index < len(txt_files) - 1:
            print("  -> Waiting for 60 seconds (cooldown) to avoid rate limits...\n")
            time.sleep(60)
            
    print("\nAll files processed successfully.")

if __name__ == "__main__":
    main()
