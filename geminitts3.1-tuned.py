import wave
from google import genai
from google.genai import types

def save_wav_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)

API_KEY = ""
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1alpha'})

# CHANGES MADE: Removed "whispered", "murmured", and "breath catching" 
# descriptions which trigger the AI's whispering behavior.
script_content = """
# AUDIO PROFILE: Calm Documentary Narrator.
A steady, grounded, and professional narrator. The goal is clarity and 
neutrality, not performance.

### DIRECTOR'S NOTES
* Style: Natural and conversational. Read the text as if you are telling a factual story to a friend.
* Vocal Presence: Moderate. Keep a consistent volume throughout; no theatrical projection.
* IMPORTANT: Strictly no over-acting, no dramatic pauses, and no emotional inflections. 
* Tone: Even, clear, and objective. Avoid "cinematic" changes in pitch or intensity.
* Pacing: Consistent, steady rhythm. Avoid long, dramatic silences.
* Technique: "Flat delivery." Focus on diction rather than performance.

#### TRANSCRIPT
The rusted key turned in the lock with a groan of protest, echoing through the hollow silence of the manor. Elias pushed the heavy oak door, revealing a foyer choked by dust motes dancing in the dying sunlight. He hadn't been back in twenty years, not since the day the music stopped.

His father had been a clockmaker, a man who believed time could be captured, refined, and stored in brass gears. As Elias stepped over the threshold, the house seemed to inhale. Clocks lined every wall—cuckoos, grandfathers, pocket watches—all stilled, their hands frozen in a permanent, mournful pose. He walked toward the workshop in the back, the floorboards sighing under his boots.

On the workbench sat the masterpiece: a clock without a face, its gears made of starlight-infused glass. He reached out, his trembling fingers brushing the cool surface. With a soft click, he nudged the main pendulum. A low, hum began to vibrate through the floor, and suddenly, the house erupted into a symphony of ticking. Thousands of clocks resumed their rhythm at once. The past wasn't just a memory; it was a heartbeat, loud and undeniable, filling the void he had carried for decades. He closed his eyes, finally listening to the time he had been running from.
"""

try:
    # Using 'Iapetus' (Clear) or 'Kore' (Firm) is safer than 'Autonoe' (Bright) 
    # to avoid breathy/whispering tones in dramatic scripts.
    response = client.models.generate_content(
        model="gemini-3.1-flash-tts-preview",
        contents=script_content,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Autonoe' 
                    )
                )
            ),
        )
    )

    audio_data = response.candidates[0].content.parts[0].inline_data.data
    
    output_filename = 'professional_drama_output3-Tune3.wav'
    save_wav_file(output_filename, audio_data)
    print(f"Success! Complete audio saved safely to '{output_filename}'.")

except Exception as e:
    print(f"An error occurred: {e}")