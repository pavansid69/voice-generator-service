# src/services/audio_service.py
from elevenlabs.client import ElevenLabs
from src.utils.config import settings

class AudioService:

    def __init__(self):
        self.client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)


    def generate_audio(self, script: str, voice_id: str | None = None) -> bytes:
        selected_voice = voice_id or settings.ELEVENLABS_VOICE_ID

        audio_bytes = self.client.text_to_speech.convert(
            text=script,
            voice_id=selected_voice,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )

        return audio_bytes
    def generate_dialogue(self, inputs: list | None = None) -> bytes:

        try:
            # --------------------------
            # 1. Require inputs
            # --------------------------
            if inputs is None or len(inputs) == 0:
                raise ValueError("No dialogue input provided. 'inputs' list is required.")

            if not isinstance(inputs, list):
                raise ValueError("'inputs' must be a list of items with text and voice_id.")

            validated_inputs = []

            # --------------------------
            # 2. Validate each entry
            # --------------------------
            for idx, item in enumerate(inputs):
                if not isinstance(item, dict):
                    item = item.dict()

                text = item.get("text")
                voice_id = item.get("voice_id")

                if not text or not isinstance(text, str) or text.strip() == "":
                    raise ValueError(f"`text` is required for dialogue entry {idx}.")

                # # Auto-assign voice if missing
                # if not voice_id:
                #     voice_id = self.default_voices[idx % len(self.default_voices)]

                validated_inputs.append({
                    "text": text.strip(),
                    "voice_id": voice_id
                })

            # --------------------------
            # 3. Call ElevenLabs Dialogue API
            # --------------------------
            try:
                print("Calling ElevenLabs with:", validated_inputs)
                audio_stream = self.client.text_to_dialogue.convert(
                    inputs=validated_inputs,
                    output_format="mp3_44100_128"
                )
                print("ElevenLabs returned:", type(audio_stream))
            except Exception as api_error:
                print("ElevenLabs API error:", str(api_error))
                raise 
            # --------------------------
            # 4. Combine streamed chunks
            # --------------------------
            try:
                audio_bytes = b"".join(chunk for chunk in audio_stream)
            except Exception as stream_error:
                raise RuntimeError(f"Failed to process audio stream: {str(stream_error)}")

            if not audio_bytes or len(audio_bytes) < 20:
                raise RuntimeError("Dialogue generation returned empty or invalid audio.")

            return audio_bytes

        except Exception as e:
            raise RuntimeError(f"Dialogue generation failed: {str(e)}")
