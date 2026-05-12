import wave
from google import genai
from google.genai import types

def save_wav_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)

API_KEY = "key"
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1alpha'})

# CHANGES MADE: Removed "whispered", "murmured", and "breath catching" 
# descriptions which trigger the AI's whispering behavior.
script_content = """
# AUDIO PROFILE: Theatrical Narrator
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
The hum of the city usually died down by two in the morning, leaving Mark and Sarah in a cocoon of artificial light and expensive coffee. They were the architects of their own digital world. But tonight, the silence of their apartment felt occupied.

Mark sat at the mahogany desk. 'Sarah,' he said, his voice steady. 'Stop moving. Look at the screen... just look at it. Tell me I’m seeing things. Please, just tell me it’s some kind of sick glitch.'

Sarah leaned over his shoulder. On the screen, a progress bar was sprinting toward one hundred percent. It was a liquidation. 

'Tell me I’m seeing things,' Mark said, his fingers hovering over the keys. 'Please, just tell me it’s some kind of sick glitch.'

Sarah’s voice was sharp. 'Oh god. No. No, no, no... it says the transfer is finished. Mark, that’s everything. Our entire savings. It’s all... it’s just gone.'

Mark’s hands finally slammed onto the desk. 'How?! How did this even happen? I didn't touch a single thing! I only opened the email from the firm! I didn't click any links! I swear I didn't click!'

'Okay... okay,' Sarah said. 'Just—just breathe. Don't panic. I’m calling the bank right now. My hands... I can't get them to stop shaking. Come on, pick up... please pick up...'

She paced the length of the rug. But Mark wasn't looking at her anymore. He was looking at the terminal window. 

'The bank?' Mark said with a hollow sound. 'Sarah, it’s three in the morning. Look at the code... the transaction ID... it’s already been routed through three different servers in the Cayman Islands. It’s gone. We're staring at an empty ghost of an account.'

'I’m trying to log in on my phone but...' Sarah stopped mid-sentence. 'The app... it won't let me in. It keeps kicking me back to the start. It says... User Not Found. Mark, why does it say User Not Found?'

Mark began typing frantically, trying to trace the phantom that had invaded their home. 

'User not found? What? Sarah, they didn't just take the money... they’re wiping us out.


"""

try:
    # Using 'Iapetus' (Clear) or 'Kore' (Firm) is safer than 'Autonoe' (Bright) 
    # to avoid breathy/whispering tones in dramatic scripts.
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
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
    
    output_filename = 'professional_drama_output2000.wav'
    save_wav_file(output_filename, audio_data)
    print(f"Success! Complete audio saved safely to '{output_filename}'.")

except Exception as e:
    print(f"An error occurred: {e}")