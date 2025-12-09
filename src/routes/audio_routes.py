# src/routes/audio_routes.py
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse

from src.models.request_models import DialogueRequest, ScriptRequest
from src.services.audio_service import AudioService
from src.utils.helpers import sanitize_script

router = APIRouter()
audio_service = AudioService()

@router.post("/generate")
async def generate_audio(request: ScriptRequest):

    try:
        script = sanitize_script(request.script)
        audio_bytes = audio_service.generate_audio(
            script=script,
            voice_id=request.voice_id
        )

        return StreamingResponse(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=generated.mp3"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/dialogue")
async def generate_dialogue(request: DialogueRequest):
    try:
        audio_bytes = audio_service.generate_dialogue(request.inputs)

        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=dialogue.mp3"}
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dialogue")
async def generate_dialogue(request: DialogueRequest):
    try:
        # Generate bytes directly (no saving)
        audio_bytes = audio_service.generate_dialogue(request.inputs)

        # Return the raw MP3 bytes
        return StreamingResponse(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=dialogue.mp3"
            }
        )

    except Exception as e:
        print("Dialogue generation error:", e)
        raise HTTPException(status_code=500, detail=str(e))